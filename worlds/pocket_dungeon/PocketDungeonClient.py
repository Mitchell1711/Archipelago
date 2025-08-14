import asyncio
from Utils import async_start
from NetUtils import NetworkItem, ClientStatus
from CommonClient import ClientCommandProcessor, CommonContext, server_loop, gui_enabled, get_base_parser, handle_url_arg
import logging
import sys
import os
import json
import pkgutil

class SKPDCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)
    
    def _cmd_savepath(self, directory: str):
        """Change the directory where your savefile is located"""
        if isinstance(self.ctx, SKPDContext):
            self.ctx.save_game_folder = directory
            self.output("Changed to the following directory: " + self.ctx.save_game_folder)
    
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
        self.server_packets_file = os.path.join(self.game_folder, "mods/Archipelago/data/server_packets.txt")
        self.client_packets_file = os.path.join(self.game_folder, "mods/Archipelago/data/client_packets.txt")
        self.server_packets = 0
        self.apsession = ""
        self.curr_seed = ""

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

def process_package(ctx: SKPDContext, cmd: str, args: dict):
    print(args)
    if cmd == "RoomInfo":
        ctx.curr_seed = args["seed_name"]
    elif cmd == "Connected":
        handle_savedata(ctx, args)
    elif cmd == "ReceivedItems":
        with open(ctx.server_file, "r") as file:
            data = json.load(file)
            if "received_items" not in data:
                data["received_items"] = []
            for item in args["items"]:
                data["received_items"].append({
                    "item": ctx.item_names.lookup_in_game(item.item),
                    "player": ctx.player_names[item.player]
                })
            data["item_index"] = args["index"]
        with open(ctx.server_file, "w") as file:
            json.dump(data, file)
    
    with open(ctx.server_packets_file, "w") as file:
        ctx.server_packets += 1
        file.write(str(ctx.server_packets))

def handle_savedata(ctx: SKPDContext, args: dict):
    #reset communication files
    with open(ctx.server_file, "w") as file:
        json.dump({"slot_data": args["slot_data"]}, file)
    with open(ctx.client_file, "w") as file:
        file.write("{}")
    
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

def launch(*args):
    async def _main(args):
        parser = get_base_parser()
        args = parser.parse_args(args)
        ctx = SKPDContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

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