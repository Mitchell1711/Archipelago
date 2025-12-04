import asyncio
import time
from Utils import open_directory, local_path
from NetUtils import JSONMessagePart, JSONtoTextParser, color_code
from CommonClient import ClientCommandProcessor, CommonContext, server_loop, gui_enabled, get_base_parser, handle_url_arg, logger
from worlds import network_data_package
import logging
import sys
import os
import json
import math
import atexit
import subprocess
import pkgutil

class SKPDCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)
    
    def _cmd_savepath(self):
        """Change the directory where your savefile is located"""
        if isinstance(self.ctx, SKPDContext):
            dir = open_directory("Save Folder", self.ctx.save_folder)
            if dir:
                self.ctx.save_folder = dir
                self.output("Changed to the following directory: " + self.ctx.save_folder)
            else:
                self.output("Didn't change directory.")
    
    def _cmd_gamepath(self):
        """Change the directory where the game is located"""
        if isinstance(self.ctx, SKPDContext):
            dir = open_directory("Game Folder", self.ctx.game_folder)
            if dir:
                self.ctx.game_folder = dir
                self.output("Changed to the following directory: " + self.ctx.game_folder)
            else:
                self.output("Didn't change directory.")
    
    def _cmd_launch_game(self):
        """Launch Shovel Knight Pocket Dungeon manually"""
        if isinstance(self.ctx, SKPDContext):
            run_game(self.ctx)
    
class SKPDContext(CommonContext):
    game = "Shovel Knight Pocket Dungeon"
    command_processor = SKPDCommandProcessor

    def __init__(self, server_address: str | None = None, password: str | None = None) -> None:
        super().__init__(server_address, password)
        self.items_handling = 0b111
        self.save_folder = os.path.expandvars(r"%APPDATA%/Yacht Club Games/Shovel Knight Pocket Dungeon")
        self.mod_folder = os.path.join(self.save_folder, "mods/Archipelago")
        self.game_folder = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Shovel Knight Pocket Dungeon"
        self.save_file = os.path.join(self.save_folder, "save")
        self.data_folder = os.path.join(self.mod_folder, "data")

        # self.server_file = os.path.join(self.mod_folder, "data/server_data.json")
        self.client_file = os.path.join(self.mod_folder, "data/client_data.json")
        self.server_packets_file = os.path.join(self.data_folder, "server_packets.json")
        self.client_packets_file = os.path.join(self.data_folder, "client_packets.json")
        self.stage_order_script = os.path.join(self.mod_folder, "stage_order.gml")
        self.server_packets = {}
        self.client_packets = {}
        self.client_data = {}
        self.server_data = {}
        self.hint_data = []
        self.apsession = ""
        self.curr_seed = ""
        self.loc_name_to_id = network_data_package["games"][self.game]["location_name_to_id"] # type: ignore
        self.game_subprocess: subprocess.Popen = None
        atexit.register(self.enable_steamworks)

        #load in default savedata
        self.base_savedata = json.loads(pkgutil.get_data(__name__, "data/base_savedata.json").decode())
        self.char_id_map = json.loads(pkgutil.get_data(__name__, "data/knight_indexes.json").decode())
    
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
    
    def run_gui(self):
        from kvui import GameManager

        class SKPDManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Pocket Dungeon Client"

        self.ui = SKPDManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI") # type: ignore
    
    async def connect(self, address: str | None = None) -> None:
        await super().connect(address)
    
    def on_package(self, cmd: str, args: dict):
        process_package(self, cmd, args)
    
    def disable_steamworks(self):
        try:
            os.rename(os.path.join(self.game_folder, "steam_api64.dll"), os.path.join(self.game_folder, "steam_api64_disabled.dll"))
            os.rename(os.path.join(self.game_folder, "Steamworks_x64.dll"), os.path.join(self.game_folder, "Steamworks_x64_disabled.dll"))
        except FileNotFoundError:
            if os.path.exists(os.path.join(self.game_folder, "steam_api64_disabled.dll")):
                print(logger.info("Steamworks .dll files have already been disabled."))
            else:
                print(logger.error("Couldn't find Steamworks .dll files, please check if the gamepath is correct."))

    def enable_steamworks(self):
        try:
            os.rename(os.path.join(self.game_folder, "steam_api64_disabled.dll"), os.path.join(self.game_folder, "steam_api64.dll"))
            os.rename(os.path.join(self.game_folder, "Steamworks_x64_disabled.dll"), os.path.join(self.game_folder, "Steamworks_x64.dll"))
        except FileNotFoundError:
            if os.path.exists(os.path.join(self.game_folder, "steam_api64.dll")):
                print(logger.info("Steamworks .dll files have already been enabled."))
            else:
                print(logger.error("Couldn't find Steamworks .dll files, please check if the gamepath is correct."))

def process_package(ctx: SKPDContext, cmd: str, args: dict):
    #print(args)
    if cmd == "RoomInfo":
        ctx.curr_seed = args["seed_name"]
    elif cmd == "Connected":
        if ctx.apsession != str(ctx.slot) + ctx.curr_seed:
            #reset communication files
            reset_packets(ctx)
            ctx.server_data = {}
            ctx.server_data["ConnectionInfo"] = {
                "slot_data": args["slot_data"], 
                "player_names": ctx.player_names
                }
            handle_savedata(ctx)
            create_stage_order(ctx, args["slot_data"]["StageOrder"], args["slot_data"]["BossOrder"])
            write_server_packets(ctx, "ConnectionInfo")
            ctx.disable_steamworks()
        write_connection_status(ctx, True)
        run_game(ctx)
        ctx.server_data["CheckedLocations"] = args["checked_locations"]
        write_server_packets(ctx, "CheckedLocations")
    elif cmd == "ReceivedItems":
        itemlist = []
        for item in ctx.items_received:
            itemlist.append({
                "item": item.item,
                "player": item.player,
                "flags": item.flags
            })
        ctx.server_data["ReceivedItems"] = itemlist
        write_server_packets(ctx, "ReceivedItems")
    elif cmd == "LocationInfo":
        if "LocationInfo" not in ctx.server_data:
            ctx.server_data["LocationInfo"] = {}
        for loc in args["locations"]:
            ctx.server_data["LocationInfo"][loc.location] = {
                "item": ctx.item_names.lookup_in_game(loc.item, ctx.slot_info[loc.player].game),
                "player": loc.player,
                "flags": loc.flags
            }
            write_server_packets(ctx, "LocationInfo")
    elif cmd == "RoomUpdate":
        if "checked_locations" in args:
            ctx.server_data["CheckedLocations"] = args["checked_locations"]
            write_server_packets(ctx, "CheckedLocations")
    elif cmd == "PrintJSON":
        printjsondata = {}
        if args.get("type") == "ItemSend" or args.get("type") == "ItemCheat":
            if ctx.slot_concerns_self(args["item"].player) and not ctx.slot_concerns_self(args["receiving"]):
                printjsondata = {
                    "type": "ItemSend",
                    "item": ctx.item_names.lookup_in_game(args["item"].item, ctx.slot_info[args["receiving"]].game),
                    "player": args["receiving"],
                    "flags": args["item"].flags
                }
        elif args.get("type") == "Chat" or args.get("type") == "ServerChat":
            printjsondata = {
                "type": "Chat",
                "text": args["message"],
                "source": ctx.player_names[args["slot"]]
            }
        else:
            textmessage = ""
            if args.get("type") == "Goal":
                textmessage = f"{ctx.player_names[args["slot"]]} reached their goal!"
            elif args.get("type") == "Release":
                textmessage = f"{ctx.player_names[args["slot"]]} released all items from their world!"
            elif args.get("type") == "Collect":
                textmessage = f"{ctx.player_names[args["slot"]]} collected all of their items!",
            if textmessage != "":
                printjsondata = {
                    "type": "Chat",
                    "text": textmessage,
                    "source": "Archipelago"
                }
        if printjsondata:
            ctx.server_data["PrintJSON"] = printjsondata
            write_server_packets(ctx, "PrintJSON")
            

def write_server_packets(ctx: SKPDContext, cmd: str):
    file_path = os.path.join(ctx.data_folder, f"server_{cmd}.json")
    with open(file_path, "w") as file:
        json.dump(ctx.server_data[cmd], file)
    with open(ctx.server_packets_file, "w") as file:
        ctx.server_packets[cmd] = time.time()
        json.dump(ctx.server_packets, file)

def reset_packets(ctx: SKPDContext):
    with open(ctx.server_packets_file, "r") as file:
        ctx.server_packets = json.load(file)
    for cmd in ctx.server_packets.keys():
        file_path = os.path.join(ctx.data_folder, f"server_{cmd}.json")
        with open(file_path, "w") as file:
            file.write("{}")

def write_connection_status(ctx: SKPDContext, status: bool):
    with open(ctx.server_packets_file, "w") as file:
        ctx.server_packets["ConnectionStatus"] = status
        json.dump(ctx.server_packets, file)

def handle_savedata(ctx: SKPDContext):
    ctx.apsession = str(ctx.slot) + ctx.curr_seed
    savedata = {}

    #open up currently loaded savefile and parse data inside
    try:
        with open(ctx.save_file, "r") as file:
            filestr = file.read()
            #json data of savefiles processed by the game arent properly formatted at the end
            if filestr[len(filestr) - 1] != "}":
                filestr = filestr[:len(filestr) - 4] + "}"
            savedata = json.loads(filestr)
    except:
        print(logger.info("No existing savefile found! Creating new file..."))
    
    if "__mod:Archipelago__" in savedata and "ap_session" in savedata["__mod:Archipelago__"]:
        save_apsession = savedata["__mod:Archipelago__"]["ap_session"]
        #if apsession changed copy specific bits of data over to seperate file
        if save_apsession != ctx.apsession:
            main_sdata: dict = savedata["0"]
            backup_savedata = {
                "0": {
                    "money": main_sdata.get("money"),
                    "bank": main_sdata.get("bank"),
                    "last_pindex3": main_sdata.get("last_pindex3"),
                    "percy_room": main_sdata.get("percy_room")
                },
                "__mod:Archipelago__": {}
            }
            for i in range(13):
                backup_savedata["0"][f"shortcut{i} unlock"] = main_sdata.get(f"shortcut{i} unlock")
            for key in savedata["__mod:Archipelago__"].keys():
                backup_savedata["__mod:Archipelago__"][key] = savedata["__mod:Archipelago__"][key]
            with open(ctx.save_file+save_apsession+".json", "w") as file:
                json.dump(backup_savedata, file)
        #dont need to do anything if savefile is alreadxy prepared
        else:
            return
    #in this case the savedata is either a vanilla file or there's no savefile
    else:
        #if there is data back that up
        if savedata:
            with open(ctx.save_file+"Backup", "w") as file:
                json.dump(savedata, file)
        #prepare base archipelago savedata
        savedata = ctx.base_savedata
    
    #retrieve list of seperate savefiles
    savefile_list = os.listdir(ctx.save_folder)

    #if savefile found in list copy relevant data over
    if "save"+ctx.apsession+".json" in savefile_list:
        with open(ctx.save_file+ctx.apsession+".json", "r") as file:
            filestr = file.read()
        new_savedata: dict = json.loads(filestr)
        for key in new_savedata["__mod:Archipelago__"].keys():
            savedata["__mod:Archipelago__"][key] = new_savedata["__mod:Archipelago__"][key]
        for key in new_savedata["0"].keys():
            savedata["0"][key] = new_savedata["0"][key]
    #prepare empty savefile if current session doesn't have one yet
    else:
        savedata["__mod:Archipelago__"] = {
            "ap_session": ctx.apsession
        }
        savedata["0"]["last_pindex3"] = ctx.char_id_map[ctx.server_data["ConnectionInfo"]["slot_data"]["StartingChar"]]
        savedata["0"]["money"] = 0
        savedata["0"]["bank"] = 0
        for i in range(13):
            savedata["0"][f"shortcut{i} unlock"] = 0
        savedata["0"][f"shortcut0 unlock"] = 1
        savedata["0"]["percy_room"] = "shortcut0"
    
    #write data to file
    with open(ctx.save_file, "w") as file:
        json.dump(savedata, file)

def create_stage_order(ctx: SKPDContext, stage_order: list[str], boss_order: list[str]):
    with open(ctx.stage_order_script, "w") as file:
        script_string = []
        if stage_order:
            formatted_stage_order = []
            for i in range(9):
                formatted_stage_order.append(stage_order[math.floor(i / 3)])
            script_string.append("adaptive_levels = true")
            script_string.append(f"\nlvl_order = {json.dumps(formatted_stage_order)}")
        else:
            file.write("")
        if boss_order[0]:
            formatted_boss_order = []
            curr_bosses = 0
            for i in range(9):
                if (i+1) % 3 == 0:
                    formatted_boss_order.append(boss_order[curr_bosses])
                    curr_bosses += 1
                else:
                    formatted_boss_order.append(-1)
            script_string.append(f"\nlvl_bosses = {json.dumps(formatted_boss_order)}")
        if script_string:
            file.writelines(script_string)
        else:
            file.write("")

def run_game(ctx: SKPDContext):
    if ctx.game_subprocess == None or ctx.game_subprocess.poll() != None:
        try:
            ctx.game_subprocess = subprocess.Popen(os.path.join(ctx.game_folder, "Shovel Knight Pocket Dungeon.exe"))
        except FileNotFoundError:
            logger.error("Couldn't find game executable, please check if the game folder path is set correctly.")

async def game_watcher(ctx: SKPDContext):
    while not ctx.exit_event.is_set():
        #check for updates
        curr_packets = {}
        with open(ctx.client_packets_file, "r") as file:
            try:
                curr_packets = json.load(file)
            except:
                print("Couldn't read packets, trying again...")
        packets_to_check = []
        for packet in list(curr_packets.keys()):
            if packet not in ctx.client_packets or curr_packets[packet] != ctx.client_packets[packet]:
                packets_to_check.append(packet)
        #check for packets if theres new ones
        if packets_to_check:
            ctx.client_packets = curr_packets
            with open(ctx.client_file, "r") as file:
                cli_data = json.load(file)
            #abort if ap sessions dont match
            if(cli_data["ap_session"] != ctx.apsession):
                await asyncio.sleep(0.1)
                continue
                
            packet = []
            #send checked locations
            if("LocationChecks" in packets_to_check):
                checked_locations = []
                for loc in cli_data["LocationChecks"]:
                    if loc not in ctx.locations_checked:
                        checked_locations.append(loc)
                        ctx.locations_checked.add(loc)
                        #delete the locationscout for aquired location from dict
                        if "LocationInfo" in ctx.server_data and loc in ctx.server_data["LocationInfo"]:
                            del ctx.server_data["LocationInfo"][loc]
                if checked_locations:
                    packet.append({
                        "cmd": "LocationChecks",
                        "locations": checked_locations
                    })
            if("LocationSync" in packets_to_check):
                locations_to_sync = []
                for loc in cli_data["LocationSync"]:
                    if loc not in ctx.locations_checked:
                        locations_to_sync.append(loc)
                packet.append({
                    "cmd": "LocationChecks",
                    "locations": locations_to_sync
                })
            #send locationscount request
            if("LocationScouts" in packets_to_check):
                location_scouts = []
                if "LocationInfo" not in ctx.server_data:
                    ctx.server_data["LocationInfo"] = {}
                if f"_read_hints_{ctx.team}_{ctx.slot}" in ctx.stored_data:
                    hintdata = ctx.stored_data[f"_read_hints_{ctx.team}_{ctx.slot}"]
                else:
                    hintdata = []
                cached_info = False
                for loc in cli_data["LocationScouts"]:
                    #check if hint is already present in hintdata
                    send_scout_packet = True
                    for hint in hintdata:
                        if loc == hint["location"] and hint["finding_player"] == ctx.slot:
                            ctx.server_data["LocationInfo"][loc] = {
                                "item": ctx.item_names.lookup_in_game(hint["item"], ctx.slot_info[hint["receiving_player"]].game),
                                "player": hint["receiving_player"],
                                "flags": hint["item_flags"]
                                }
                            cached_info = True
                            send_scout_packet = False
                    #else add a location scouts packet
                    if send_scout_packet:
                        location_scouts.append(loc)
                if cached_info:
                    write_server_packets(ctx, "LocationInfo")
                
                packet.append({
                    "cmd": "LocationScouts",
                    "locations": location_scouts,
                    "create_as_hint": 0
                })
            #send clientstatus
            if("StatusUpdate" in packets_to_check):
                packet.append({
                    "cmd": "StatusUpdate",
                    "status": cli_data["StatusUpdate"]
                })
            #send packet if not empty
            if packet:
                await ctx.send_msgs(packet)
            #update local client data
            ctx.client_data = cli_data
        await asyncio.sleep(0.1)

def launch(*args):
    async def _main(args):
        parser = get_base_parser()
        args = parser.parse_args(args)
        ctx = SKPDContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        asyncio.create_task(game_watcher(ctx), name="SKPDGameWatcher")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()
    
    import colorama # type: ignore

    # use colorama to display colored text highlighting on windows
    colorama.just_fix_windows_console()

    asyncio.run(_main(args))
    colorama.deinit()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    launch(*sys.argv[1:])