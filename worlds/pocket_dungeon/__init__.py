from typing import Any, Mapping
from BaseClasses import Item, Tutorial
from ..AutoWorld import World, WebWorld
from .Items import SKPDItem, skpd_items, get_item_from_category
from .Locations import skpd_locations, create_locations
from .Regions import create_regions, dungeon_amount
from .Options import SKPDOptions
from Options import OptionError
from .Rules import set_rules
import math
from worlds.LauncherComponents import Component, components, launch as launch_component, Type
import json

def run_client(*args: str):
    print("Running Pocket Dungeon Client")
    from .PocketDungeonClient import launch
    launch_component(launch, name="SKPDClient", args=args)

components.append(Component("Pocket Dungeon Client", "SKPDClient", func=run_client, component_type=Type.CLIENT))

def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, "data/" + file_name)

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
    Help them escape by collecting 4 key fragments and facing the Enchantress at the Tower of Fate in this roguelike puzzle game.
    """
    game = "Shovel Knight Pocket Dungeon"
    web = SKPDWeb()
    topology_present = False

    options_dataclass = SKPDOptions
    options: SKPDOptions # type: ignore

    item_name_to_id = {name: data.code for name, data in skpd_items.items()}
    create_locations()
    location_name_to_id = {name: data.code for name, data in skpd_locations.items()}

    def generate_mod_mappings(self) -> None:
        mappings = {}
        mappings["item_id_to_name"] = {}
        mappings["characters"] = {}
        for key in skpd_items.keys():
            code = skpd_items[key].code
            mappings["item_id_to_name"].update({code: {"name": key}})
            if skpd_items[key].internal_name != None:
                mappings["item_id_to_name"][code]["internal_name"] = skpd_items[key].internal_name
            if skpd_items[key].category == "Character" or skpd_items[key].category == "Refract Character":
                mappings["characters"].update({skpd_items[key].internal_name: key})
        mappings["location_name_to_id"] = self.location_name_to_id
        with open("skpd_mappings.json", "w") as file:
            json.dump(mappings, file)

    def generate_early(self) -> None:
        self.characters = get_item_from_category("Character")
        self.starting_character = self.options.starting_character.value
        for char in self.options.excluded_characters.value:
            self.characters.remove(char)
        self.characters.remove(self.options.starting_character.value)

        #remove random characters from the character list
        char_amount = math.floor(len(self.characters) * (self.options.total_characters.value / 100))
        to_remove = len(self.characters) - char_amount
        for i in range(to_remove):
            index = self.random.randint(0, len(self.characters) - 1)
            self.characters.pop(index)
        self.characters.append(self.options.starting_character.value)
        
        #add refract variants
        if self.options.shuffle_refract_characters:
            refract_list = []
            for char in self.characters:
                refract_char = f"{char} B"
                if refract_char in skpd_items:
                    refract_list.append(f"{char} B")
            self.characters += refract_list
        if self.options.starting_character_is_refract:
            refract_char = f"{self.starting_character} B"
            if refract_char in skpd_items:
                self.starting_character = refract_char
        
        #self.generate_mod_mappings()
    
    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player, self.options, self.characters)
    
    def create_item(self, name: str) -> Item:
        data = skpd_items[name]
        return SKPDItem(name, data.classification, data.code, self.player)
    
    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player, self.options)
        if(self.options.end_goal == 0):
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("Puzzle Knight Defeated", self.player)
        elif(self.options.end_goal == 1):
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("Enchantress Defeated", self.player)

    def create_items(self) -> None:
        skpd_itempool = []
        locations_to_fill = len(self.multiworld.get_unfilled_locations(self.player))

        #key pieces are only needed for true ending
        if(self.options.end_goal == 1):
            for i in range(4):
                skpd_itempool.append(self.create_item("Key Fragment"))
        for i in range(self.options.hub_shop_restock_count):
            skpd_itempool.append(self.create_item("Shop Restock"))
        if self.options.progression_type == 0:
            for i in range(3):
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
        
        if self.options.shuffle_hats:
            for hat in get_item_from_category("Hat"):
                if hat not in self.options.excluded_hats.value:
                    skpd_itempool.append(self.create_item(hat))
        
        total_filler = locations_to_fill - len(skpd_itempool)
        traps_to_place = math.floor(total_filler * (self.options.trap_fill_percent / 100))
        for i in range(traps_to_place):
            skpd_itempool.append(self.create_item("Garbage"))
        
        for filler in self.options.filler_weights:
            filler_to_place = math.floor((total_filler - traps_to_place) * (self.options.filler_weights[filler] / 100))
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
            "StartingChar": self.starting_character,
            "StageOrder": levelorder,
            "HatExpiration": self.options.hat_expiration_action.value,
            "MaxHats": self.options.hat_stack_amount.value,
            "EndGoal": self.options.end_goal.value,
            "ProgressionType": self.options.progression_type.value
        }