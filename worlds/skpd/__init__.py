from typing import Any, Mapping
from BaseClasses import Item
from ..AutoWorld import World, WebWorld
from .Items import SKPDItem, skpd_items, get_item_from_category
from .Locations import skpd_locations, create_locations
from .Regions import create_regions, dungeon_amount
from .Options import SKPDOptions
from .Rules import set_rules
import math

class SKPDWeb(WebWorld):
    theme = "grass"

class SKPDWorld(World):
    """
    Shovel Knight and the Order of No Quarter have been trapped inside of the Pocket Dungeon!
    Help them escape by collecting 4 key fragments and facing the Enchantress at the Tower of Fate in this roguelike puzzle game.
    """
    game = "Shovel Knight Pocket Dungeon"
    web = SKPDWeb()
    topology_present = True

    options_dataclass = SKPDOptions
    options: SKPDOptions # type: ignore

    item_name_to_id = {name: data.code for name, data in skpd_items.items()}
    location_name_to_id = {name: data.code for name, data in skpd_locations.items()}
    
    def create_regions(self) -> None:
        create_locations()
        create_regions(self.multiworld, self.player, self.options)
    
    def create_item(self, name: str) -> Item:
        data = skpd_items[name]
        return SKPDItem(name, data.classification, data.code, self.player)
    
    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("Enchantress Defeated", self.player)
    
    def create_items(self) -> None:
        skpd_itempool = []
        locations_to_fill = len(self.multiworld.get_unfilled_locations(self.player))

        for i in range(4):
            skpd_itempool.append(self.create_item("Key Fragment"))
        for i in range(self.options.hub_shop_restock_count):
            skpd_itempool.append(self.create_item("Shop Restock"))
        for i in range(dungeon_amount - 1):
            if self.options.do_progressive_dungeons and self.options.dungeon_start_amount < i:
                skpd_itempool.append(self.create_item("Progressive Dungeon"))
            else:
                self.push_precollected(self.create_item("Progressive Dungeon"))
        
        for character in get_item_from_category("Character"):
            if character != self.options.starting_character:
                skpd_itempool.append(self.create_item(character))
            else:
                self.push_precollected(self.create_item(character))
        
        for relic in get_item_from_category("Relic"):
            skpd_itempool.append(self.create_item(relic))
        
        if self.options.enable_hats:
            for hat in get_item_from_category("Hat"):
                skpd_itempool.append(self.create_item(hat))
        else:
            #these are progression items so shuffle and random knight can get their checks
            skpd_itempool.append(self.create_item("Almond"))
            skpd_itempool.append(self.create_item("Souffle"))
        
        total_filler = locations_to_fill - len(skpd_itempool)
        traps_to_place = math.floor(total_filler * (self.options.trap_fill_percent / 100))
        for i in range(traps_to_place):
            skpd_itempool.append(self.create_item("Junk"))
        for i in range(total_filler - traps_to_place):
            skpd_itempool.append(self.create_item("Gems"))

        self.multiworld.itempool += skpd_itempool

    def get_filler_item_name(self) -> str:
        return "Gems"
    
    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "StartingChar": int(self.options.starting_character.value),
            "DeathLink": bool(self.options.death_link)
        }
    
