from typing import Any, Mapping
from ..AutoWorld import World, WebWorld
from BaseClasses import Item, Tutorial, ItemClassification, CollectionState, MultiWorld
from .Items import skdig_items, SKDigItem
from .Locations import skdig_locations
from .Options import SKDigOptions, SKDig_option_groups
from .Regions import create_regions

class SKDigWeb(WebWorld):
    theme = "dirt"
    option_groups = SKDig_option_groups
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Shovel Knight Dig randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        [""]
    )

class SKDigWorld(World):
    """
    Shovel Knight Dig info blurb
    """

    game = "Shovel Knight Dig"
    web = SKDigWeb()
    topology_present = False

    item_name_to_id = {name: data.code for name, data in skdig_items.items()}
    location_name_to_id = {name: data.code for name, data in skdig_locations.items()}

    options_dataclass = SKDigOptions
    options: SKDigOptions

    def generate_early(self) -> None:
        return super().generate_early()
    
    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player, self.options)
    
    def create_item(self, name: str) -> Item:
        data = skdig_items[name]
        return SKDigItem(name, data.classification, data.code, self.player)
    
    def create_items(self) -> None:
        skdig_itempool = []
        locations_to_fill = len(self.multiworld.get_unfilled_locations(self.player))

        for i in range(locations_to_fill):
            skdig_itempool.append(self.create_item("Gems"))

        #add items to the global itempool
        self.multiworld.itempool += skdig_itempool
    
    def set_rules(self) -> None:
        super().set_rules()
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("The Enchantress Defeated", self.player)
    
    def get_filler_item_name(self) -> str:
        return "Gems"
    
    def fill_slot_data(self) -> Mapping[str, Any]:
        return {}
    