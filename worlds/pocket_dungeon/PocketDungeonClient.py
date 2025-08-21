import asyncio
from Utils import open_directory, open_file, async_start
from NetUtils import JSONMessagePart, JSONtoTextParser, color_code
from CommonClient import ClientCommandProcessor, CommonContext, server_loop, gui_enabled, get_base_parser, handle_url_arg
from worlds import network_data_package
import logging
import sys
import os
import json
import pkgutil

class SKPDCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)
    
    def _cmd_savepath(self):
        """Change the directory where your savefile is located"""
        if isinstance(self.ctx, SKPDContext):
            open_directory("Save Path", self.ctx.game_folder)
            self.output("Changed to the following directory: " + self.ctx.game_folder)

class SKPDJSONToTextParser(JSONtoTextParser):
    color_codes = {
        "black": "[#000000]",
        "red": "[#EE0000]",
        "green": "[#00FF7F]",
        "yellow": "[#FAFAD2]",
        "blue": "[#6495ED]",
        "magenta": "[#EE00EE]",
        "cyan": "[#00EEEE]",
        "slateblue": "[#6D8BE8]",
        "plum": "[#AF99EF]",
        "salmon": "[#FA8072]",
        "white": "[#FFFFFF]",
        "orange": "[#FF7700]",
    }

    def _handle_color(self, node: JSONMessagePart):
        codes = node.get("color").split(";")
        buffer = "".join(self.color_codes[code] for code in codes if code in self.color_codes)
        return buffer + self._handle_text(node) + "[/c]"
    
class SKPDContext(CommonContext):
    game = "Shovel Knight Pocket Dungeon"
    command_processor = SKPDCommandProcessor

    def __init__(self, server_address: str | None = None, password: str | None = None) -> None:
        super().__init__(server_address, password)
        self.items_handling = 0b111
        self.game_folder = os.path.expandvars(r"%APPDATA%/Yacht Club Games/Shovel Knight Pocket Dungeon")
        self.save_file = os.path.join(self.game_folder, "save")
        self.server_file = os.path.join(self.game_folder, "mods/Archipelago/data/server_data.json")
        self.client_file = os.path.join(self.game_folder, "mods/Archipelago/data/client_data.json")
        self.server_packets_file = os.path.join(self.game_folder, "mods/Archipelago/data/server_packets.json")
        self.client_packets_file = os.path.join(self.game_folder, "mods/Archipelago/data/client_packets.json")
        self.server_packets = {}
        self.client_packets = {}
        self.client_data = {}
        self.server_data = {}
        self.hint_data = []
        self.apsession = ""
        self.curr_seed = ""
        self.loc_name_to_id = network_data_package["games"][self.game]["location_name_to_id"] # type: ignore
        self.gamejsontotext = SKPDJSONToTextParser(self)

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

    def on_print_json(self, args: dict):
        super().on_print_json(args)
        relevant = args.get("type") in ["ItemSend", "ItemCheat", "Chat", "Goal"]
        if relevant:
            #filter out item sending not relevant to our slot and items sent to ourselves
            if "item" in args and not self.slot_concerns_self(args["item"].player):
                relevant = False
            if "item" in args and self.slot_concerns_self(args["item"].player and self.slot_concerns_self(args["receiving"])):
                relevant = False
            if relevant:
                self.server_data["PrintJSON"] = self.gamejsontotext(args["data"])
                with open(self.server_file, "w") as file:
                    json.dump(self.server_data, file)
                
                with open(self.server_packets_file, "w") as file:
                    index = 0
                    if "PrintJSON" in self.server_packets:
                        index = self.server_packets["PrintJSON"]
                    self.server_packets["PrintJSON"] = index + 1
                    json.dump(self.server_packets, file)

def process_package(ctx: SKPDContext, cmd: str, args: dict):
    #print(args)
    newpacket = False
    if cmd == "RoomInfo":
        ctx.curr_seed = args["seed_name"]
    elif cmd == "Connected":
        handle_savedata(ctx, args)
    elif cmd == "ReceivedItems":
        if "ReceivedItems" not in ctx.server_data:
            ctx.server_data["ReceivedItems"] = []
        for item in args["items"]:
            ctx.server_data["ReceivedItems"].append({
                "item": ctx.item_names.lookup_in_game(item.item),
                "player": ctx.player_names[item.player],
                "flags": item.flags
            })
            ctx.server_data["item_index"] = args["index"]
        newpacket = True
    elif cmd == "LocationInfo":
        if "LocationInfo" not in ctx.server_data:
            ctx.server_data["LocationInfo"] = {}
        for loc in args["locations"]:
            ctx.server_data["LocationInfo"][ctx.location_names.lookup_in_game(loc.location)] = {
                "item": ctx.item_names.lookup_in_game(loc.item, ctx.slot_info[loc.player].game),
                "player": ctx.player_names[loc.player],
                "flags": loc.flags
            }
            newpacket = True
    elif cmd == "RoomUpdate":
        if "checked_locations" in args:
            ctx.server_data["CheckedLocations"] = args["checked_locations"]
            newpacket = True
    
    if(newpacket):
        with open(ctx.server_file, "w") as file:
            json.dump(ctx.server_data, file)
        with open(ctx.server_packets_file, "w") as file:
            index = 0
            if cmd in ctx.server_packets:
                index = ctx.server_packets[cmd]
            ctx.server_packets[cmd] = index + 1
            json.dump(ctx.server_packets, file)

def handle_savedata(ctx: SKPDContext, args: dict):
    #reset communication files
    ctx.server_data = {"slot_data": args["slot_data"]}
    with open(ctx.server_file, "w") as file:
        json.dump(ctx.server_data, file)
    with open(ctx.server_packets_file, "w") as file:
        json.dump(ctx.server_packets, file)
    
    #identifier for this archipelago session
    ctx.apsession = str(ctx.slot) + ctx.curr_seed
    savefile_list = os.listdir(ctx.game_folder)

    if "save"+ctx.apsession in savefile_list:
        do_copy = backup_savedata(ctx)
        #the current apsession isn't loaded as the save yet so we need to copy the contents over from its seperate file
        if do_copy:
            with open(ctx.save_file+ctx.apsession, "r") as file:
                filestr = file.read()
            with open(ctx.save_file, "w") as file:
                file.write(filestr)
    else:
        backup_savedata(ctx)
        #create a new savefile if one isn't present
        with open(ctx.save_file, "w") as file:
            ctx.base_savedata["__mod:Archipelago__"]["ap_session"] = ctx.apsession
            #set starting character
            ctx.base_savedata["0"]["last_pindex3"] = ctx.char_id_map[args["slot_data"]["StartingChar"]]
            json.dump(ctx.base_savedata, file)
        #create the seperate backup savefile
        with open(ctx.save_file+ctx.apsession, "w") as file:
            json.dump(ctx.base_savedata, file)
        

def backup_savedata(ctx: SKPDContext) -> bool:
    #check if a savefile even exists
    if os.path.exists(ctx.save_file) == False:
        return True
    
    #open up currently loaded savefile and parse data inside
    with open(ctx.save_file, "r") as file:
        filestr = file.read()
        #json data of savefiles processed by the game arent properly formatted at the end
        if filestr[len(filestr) - 1] != "}":
            filestr = filestr[:len(filestr) - 4] + "}"
        data = json.loads(filestr)
    #check if the currently loaded savefile isn't already using the current ap session
    #if it isn't copy the contents over to its own seperate save file
    if "__mod:Archipelago__" in data and "ap_session" in data["__mod:Archipelago__"]:
        save_apsession = data["__mod:Archipelago__"]["ap_session"]
        if save_apsession != ctx.apsession:
            with open(ctx.save_file+save_apsession, "w") as file_2:
                file_2.write(filestr)
            return True
    #savefiles without the archipelago data are non-archipelago savefiles, back those up safely
    else:
        with open(ctx.save_file+"Backup", "w") as file_2:
            file_2.write(filestr)
        return True
    return False

async def game_watcher(ctx: SKPDContext):
    while not ctx.exit_event.is_set():
        #check for updates
        with open(ctx.client_packets_file, "r") as file:
            curr_packets = json.load(file)
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
                    checked_locations.append(ctx.loc_name_to_id[loc])
                    #delete the locationscout for aquired location from dict
                    if "LocationInfo" in ctx.server_data and loc in ctx.server_data["LocationInfo"]:
                        del ctx.server_data["LocationInfo"][loc]
                with open(ctx.server_file, "w") as file:
                    json.dump(ctx.server_data, file)
                packet.append({
                    "cmd": "LocationChecks",
                    "locations": checked_locations
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
                for loc in cli_data["LocationScouts"]:
                    #check if hint is already present in hintdata
                    send_scout_packet = True
                    for hint in hintdata:
                        if ctx.loc_name_to_id[loc] == hint["location"] and hint["finding_player"] == ctx.slot:
                            ctx.server_data["LocationInfo"][ctx.location_names.lookup_in_game(hint["location"])] = {
                                "item": ctx.item_names.lookup_in_game(hint["item"], ctx.slot_info[hint["receiving_player"]].game),
                                "player": ctx.player_names[hint["receiving_player"]],
                                "flags": hint["item_flags"]
                                }
                            send_scout_packet = False
                    #else add a location scouts packet
                    if send_scout_packet:
                        location_scouts.append(ctx.loc_name_to_id[loc])
                    with open(ctx.server_file, "w") as file:
                        json.dump(ctx.server_data, file)
                packet.append({
                    "cmd": "LocationScouts",
                    "locations": location_scouts,
                    "create_as_hint": 1
                })
            #send clientstatus
            if("ClientStatus" in packets_to_check):
                packet.append({
                    "cmd": "ClientStatus",
                    "status": cli_data["ClientStatus"]
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