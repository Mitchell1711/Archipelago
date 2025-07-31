import asyncio
from Utils import async_start
from NetUtils import NetworkItem, ClientStatus
from CommonClient import ClientCommandProcessor, CommonContext, server_loop, gui_enabled, get_base_parser, handle_url_arg
import logging
import sys
import os
import json

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
        self.save_game_folder = os.path.expandvars(r"%APPDATA%/Yacht Club Games/Shovel Knight Pocket Dungeon")
        self.server_file = os.path.join(self.save_game_folder, "server_data.json")
        self.client_file = os.path.join(self.save_game_folder, "client_data.json")
    
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
        #empty files
        with open(self.server_file, "w") as file:
            file.write("{}")
        with open(self.client_file, "w") as file:
            file.write("{}")
        await super().connect(address)
    
    def on_package(self, cmd: str, args: dict):
        process_package(self, cmd, args)

def process_package(ctx: SKPDContext, cmd: str, args: dict):
    print(args)
    if cmd == "Connected":
        with open(ctx.server_file, "r") as file:
            data = json.load(file)
            data["slot_data"] = args["slot_data"]
        with open(ctx.server_file, "w") as file:
            json.dump(data, file)
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
        with open(ctx.server_file, "w") as file:
            json.dump(data, file)
    

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