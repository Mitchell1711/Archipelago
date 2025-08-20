from typing import Any, Mapping
from BaseClasses import Item
from ..AutoWorld import World, WebWorld
from .Items import SKPDItem, skpd_items, get_item_from_category
from .Locations import skpd_locations, create_locations
from .Regions import create_regions, dungeon_amount
from .Options import SKPDOptions
from .Rules import set_rules
import math
from worlds.LauncherComponents import Component, components, launch as launch_component, Type

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
    
    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player, self.options)
    
    def create_item(self, name: str) -> Item:
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
        for i in range(3):
            if self.options.progression_type == 0:
                skpd_itempool.append(self.create_item("Progressive Dungeon"))
            else:
                self.push_precollected(self.create_item("Progressive Dungeon"))
        
        found_starting_char = False
        for character in get_item_from_category("Character"):
            if character != self.options.starting_character.value:
                skpd_itempool.append(self.create_item(character))
                found_starting_char = True
            else:
                self.push_precollected(self.create_item(character))
        if not found_starting_char:
            raise Exception("[Shovel Knight Pocket Dungeon] Couldn't find starting character, please check if the .yaml is correct.")
        
        if self.options.shuffle_refract_characters:
            for refract_character in get_item_from_category("Refract Character"):
                skpd_itempool.append(self.create_item(refract_character))
        
        for relic in get_item_from_category("Relic"):
            skpd_itempool.append(self.create_item(relic))
        
        if self.options.enable_hats:
            for hat in get_item_from_category("Hat"):
                skpd_itempool.append(self.create_item(hat))
        #deprecated since shuffle/random aren't part of the pool anymore
        # else:
            #these are progression items so shuffle and random knight can get their checks
            # skpd_itempool.append(self.create_item("Almond"))
            # skpd_itempool.append(self.create_item("Souffle"))
        
        total_filler = locations_to_fill - len(skpd_itempool)
        traps_to_place = math.floor(total_filler * (self.options.trap_fill_percent / 100))
        for i in range(traps_to_place):
            skpd_itempool.append(self.create_item("Garbage"))
        for i in range(total_filler - traps_to_place):
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
            "StartingChar": str(self.options.starting_character.value),
            "DeathLink": bool(self.options.death_link),
            "RandomizeLevelOrder": levelorder
        }