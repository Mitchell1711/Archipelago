from typing import Any, Mapping
from BaseClasses import Item, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld
from .Items import SKPDItem, item_dict, get_item_from_category, create_item_categories, skpd_items, item_categories
from .Locations import skpd_locations, create_locations, location_categories, create_location_categories
from .Regions import create_regions
from .Options import SKPDOptions
from .Rules import set_rules
import math
from worlds.LauncherComponents import Component, components, launch as launch_component, Type
import json
import settings
from Options import OptionError

def run_client(*args: str):
    print("Running Pocket Dungeon Client")
    from .PocketDungeonClient import launch
    launch_component(launch, name="SKPDClient", args=args)

components.append(Component("Shovel Knight Pocket Dungeon Client", "SKPDClient", func=run_client, component_type=Type.CLIENT))

def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, "data/" + file_name)

class SKPDSettings(settings.Group):
    class SaveDirectory(settings.UserFolderPath):
        """
        Locates where your SKPD savefile and offline modfiles are found on your system.
        """
        description = "Shovel Knight Pocket Dungeon save directory"

    class GameDirectory(settings.UserFolderPath):
        """
        Locates where your Shovel Knight Pocket Dungeon installation is found on your system.
        """
        description = "Shovel Knight Pocket Dungeon game directory"
    class WorkshopDirectory(settings.UserFolderPath):
        """
        Locates where the Steam workshop Archipelago mod for Shovel Knight Pocket Dungeon is found on your system. 
        """
        description = "Archipelago Workshop mod directory"
    
    save_directory: SaveDirectory = SaveDirectory("%APPDATA%/Yacht Club Games\\Shovel Knight Pocket Dungeon")
    game_directory: GameDirectory = GameDirectory("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Shovel Knight Pocket Dungeon")
    workshop_directory: WorkshopDirectory = WorkshopDirectory("C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\1184760\\3619001702")

class SKPDWeb(WebWorld):
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Shovel Knight Pocket Dungeon randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Mitchell"]
    )

class SKPDWorld(World):
    """
    Shovel Knight and the Order of No Quarter have been trapped inside of the Pocket Dungeon!
    Help them escape by collecting 4 key fragments and facing the Enchantress at the Tower of Fate in this roguelite action-puzzle game.
    """
    game = "Shovel Knight Pocket Dungeon"
    web = SKPDWeb()
    topology_present = False

    options_dataclass = SKPDOptions
    options: SKPDOptions
    settings: SKPDSettings

    create_item_categories()
    create_locations()
    create_location_categories()

    item_name_to_id = item_dict
    location_name_to_id = {name: data.code for name, data in skpd_locations.items()}

    item_name_groups = {category: set(item_categories[category]) for category in item_categories}
    location_name_groups = {category: set(location_categories[category]) for category in location_categories}
    
    #Tell universal tracker we don't need a YAML
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]: #UT support function that causes a re-generation
        return slot_data #we don't need to do any modification to the slot data, so just return it
    
    ut_can_gen_without_yaml = True
    glitches_item_name = "Glitched Logic"

    def generate_mod_mappings(self) -> None:
        mappings = {}
        mappings["item_id_to_name"] = {}
        mappings["characters"] = {}
        for key in skpd_items.keys():
            code = skpd_items[key].code
            mappings["item_id_to_name"].update({code: {"name": key}})
            if skpd_items[key].internal_name != None:
                mappings["item_id_to_name"][code]["internal_name"] = skpd_items[key].internal_name
            if skpd_items[key].category == "Character":
                mappings["characters"].update({skpd_items[key].internal_name: key})
        mappings["location_name_to_id"] = self.location_name_to_id
        with open("skpd_mappings.json", "w") as file:
            json.dump(mappings, file)
    
    def prepare_ut(self) -> None:
        #universal tracker stuff
        re_gen_passthrough = getattr(self.multiworld,"re_gen_passthrough",{})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data = re_gen_passthrough[self.game]
            self.options.progression_type = slot_data["ProgressionType"]
            for option in slot_data["UTOptions"]:
                setattr(self.options, option, slot_data["UTOptions"][option])
    
    def handle_playable_characters(self) -> None:
        #prune excluded and starting character from list
        self.characters = list(get_item_from_category("Character"))
        self.starting_character = self.options.starting_character.charlist[self.options.starting_character.value]
        for char in self.options.excluded_characters:
            if char == self.starting_character:
                raise OptionError("Starting character cannot be set as excluded!")
            else:
                self.characters.remove(char)
        self.characters.remove(self.starting_character)

        #remove random characters from the character list
        char_amount = math.floor(len(self.characters) * (self.options.total_characters / 100))
        to_remove = len(self.characters) - char_amount
        for i in range(to_remove):
            index = self.random.randint(0, len(self.characters) - 1)
            self.characters.pop(index)
        self.characters.append(self.starting_character)
        
        #add refract variants
        if self.options.shuffle_refract_characters:
            refract_list: list[str] = []
            for char in self.characters:
                refract_char = f"{char} B"
                if refract_char in skpd_items:
                    refract_list.append(f"{char} B")
            self.characters += refract_list
        if self.options.starting_character_is_refract:
            refract_char = f"{self.starting_character} B"
            if refract_char in skpd_items:
                self.starting_character = refract_char
    
    def randomize_bosses(self) -> None:
        #boss table are location names for AP, boss_order is internal ids sent through slot data to set the boss order
        self.boss_order: list[list[str]] = [[], [], []]
        self.boss_table: list[list[str]] = [[], [], []]

        if self.options.randomize_bosses:
            bosses = [
                ["King Knight Defeated", "king boss"],
                ["Specter Knight Defeated", "specter boss"],
                ["Plague Knight Defeated", "plague boss"],
                ["Treasure Knight Defeated", "treasure boss"],
                ["Tinker Knight Defeated", "tinker boss"],
                ["Mole Knight Defeated", "mole boss"],
                ["Scrap Knight Defeated", "scrap boss"],
                ["Propeller Knight Defeated", "propeller boss"],
                ["Polar Knight Defeated", "polar boss"],
                ["Prism Knight Defeated", "prism boss"],
                ["Black Knight Defeated", "black knight boss"],
                ["Shovel Knight Defeated","shovel knight boss"]
            ]
            for i in range(3):
                for ii in range(4):
                    rand_boss_data = bosses.pop(self.random.randrange(0, len(bosses)))
                    self.boss_table[i].append(rand_boss_data[0])
                    self.boss_order[i].append(rand_boss_data[1])
        else:
            self.boss_table = [
            ["King Knight Defeated", "Specter Knight Defeated", "Plague Knight Defeated", "Black Knight Defeated"],
            ["Treasure Knight Defeated", "Tinker Knight Defeated", "Mole Knight Defeated", "Scrap Knight Defeated"],
            ["Propeller Knight Defeated", "Polar Knight Defeated", "Prism Knight Defeated"]
        ]

    def generate_early(self) -> None:
        #self.generate_mod_mappings()

        self.prepare_ut()
        self.handle_playable_characters()
        self.randomize_bosses()
        
        #place early meal ticket if enabled
        if self.options.early_meal_ticket:
            self.multiworld.early_items[self.player]["Meal Ticket"] = 1
    
    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player, self.options, self.characters, self.boss_table)
    
    def create_item(self, name: str) -> Item:
        if name == "Glitched Logic":
            return SKPDItem(name, ItemClassification.progression, None, self.player)
        
        data = skpd_items[name]
        return SKPDItem(name, data.classification, data.code, self.player)
    
    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player, self.options)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("Enchantress Defeated", self.player)

    def create_items(self) -> None:
        skpd_itempool = []
        locations_to_fill = len(self.multiworld.get_unfilled_locations(self.player))

        for i in range(4):
            skpd_itempool.append(self.create_item("Key Fragment"))
        for i in range(self.options.hub_shop_restock_count):
            skpd_itempool.append(self.create_item("Shop Restock"))
        if self.options.progression_type == 0:
            for i in range(2):
                skpd_itempool.append(self.create_item("Progressive Dungeon"))

        for character in self.characters:
            if character != self.starting_character:
                skpd_itempool.append(self.create_item(character))
            else:
                self.push_precollected(self.create_item(character))
        
        for relic in get_item_from_category("Relic"):
            if self.options.shuffle_relics:
                skpd_itempool.append(self.create_item(relic))
            else:
                self.push_precollected(self.create_item(relic))
        
        for i in range(self.options.staring_relic_slot_amount.value):
            skpd_itempool.append(self.create_item("Starting Relic Slot"))
        
        if self.options.shuffle_hats:
            for hat in get_item_from_category("Hat"):
                if hat not in self.options.excluded_hats.value:
                    skpd_itempool.append(self.create_item(hat))
        
        #add filler to itempool
        total_filler = locations_to_fill - len(skpd_itempool)
        total_filler_weights = 0
        for filler in self.options.filler_weights:
            total_filler_weights += self.options.filler_weights[filler]
        
        for filler in self.options.filler_weights:
            filler_to_place = math.floor(total_filler * (self.options.filler_weights[filler] / total_filler_weights))
            for i in range(filler_to_place):
                skpd_itempool.append(self.create_item(filler))
        
        #fill last open slots due to rounding with 1000 gems
        for i in range(locations_to_fill - len(skpd_itempool)):
            skpd_itempool.append(self.create_item("1000 Gems"))

        self.multiworld.itempool += skpd_itempool
    
    def partition_even(self, count: int, to_divide: int) -> list:
        lst = []
        loop = to_divide - 1
        for i in range(loop):
            lst.append(math.floor(count * (1 / to_divide)))
            count = math.ceil(count * ((to_divide - 1) / to_divide))
            to_divide -= 1
        lst.append(count)
        return lst
    
    def shuffle_levels(self):
        levelorder = [[], [], []]
        levels = [
            "plains",
            "pridemoor keep",
            "lich yard",
            "magic landfill",
            "iron whale",
            "crystal caverns",
            "clockwork tower",
            "stranded ship",
            "flying machine",
            "explodatorium",
            "lost city"
        ]

        levels += self.options.modded_levels.value
        
        ranges = self.partition_even(len(levels), 3)
        for i in range(3):
            for ii in range(ranges[i]):
                rand_num = self.random.randint(0, len(levels) - 1)
                levelorder[i].append(levels.pop(rand_num))
        return levelorder

    def get_filler_item_name(self) -> str:
        return "1000 Gems"
    
    def fill_slot_data(self) -> Mapping[str, Any]:
        levelorder = []
        if self.options.randomize_level_order:
            levelorder = self.shuffle_levels()
        return {
            "WorldVersion": list(self.world_version),
            "StartingChar": self.starting_character,
            "StageOrder": levelorder,
            "HatExpiration": self.options.hat_expiration_action.value,
            "MaxHats": self.options.hat_stack_amount.value,
            "ProgressionType": self.options.progression_type.value,
            "DungeonShopHints": self.options.dungeon_shop_hints.value,
            "BossOrder": self.boss_order,
            "UTOptions": self.options.as_dict(
                "excluded_characters", 
                "total_characters",
                "randomize_bosses"
                )
        }