from typing import NamedTuple, Any
from BaseClasses import Location
from .Items import get_item_from_category, SKPDItemCategory
from enum import Enum

class SKPDLocationCategory(Enum):
    BOSS_DEFEATED = 0
    SHRINE = 1
    DUNGEON_SHOP = 2
    CHESTER_CAMP_SHOP = 3
    RUN_COMPLETE = 4

class SKPDLocation(Location):
    game: str = "Shovel Knight Pocket Dungeon"

class SKPDLocationData(NamedTuple):
    code: int
    category: SKPDLocationCategory
    data: Any = None

location_categories: dict[SKPDLocationCategory, list[str]] = {}

def create_location_categories():
    for loc in skpd_locations:
        category = skpd_locations[loc].category
        if category not in location_categories:
            location_categories[category] = list()
        location_categories[category].append(loc)

def get_location_from_category(category: SKPDLocationCategory) -> list[str]:
    return location_categories[category]

skpd_locations: dict[str, SKPDLocationData] = { }

def create_locations():
    skpd_locations.update({
        "King Knight Defeated":         SKPDLocationData(100, SKPDLocationCategory.BOSS_DEFEATED, "King Knight"),
        "Specter Knight Defeated":      SKPDLocationData(101, SKPDLocationCategory.BOSS_DEFEATED, "Specter Knight"),
        "Plague Knight Defeated":       SKPDLocationData(102, SKPDLocationCategory.BOSS_DEFEATED, "Plague Knight"),
        "Treasure Knight Defeated":     SKPDLocationData(103, SKPDLocationCategory.BOSS_DEFEATED, "Treasure Knight"),
        "Tinker Knight Defeated":       SKPDLocationData(104, SKPDLocationCategory.BOSS_DEFEATED, "Tinker Knight"),
        "Mole Knight Defeated":         SKPDLocationData(105, SKPDLocationCategory.BOSS_DEFEATED, "Mole Knight"),
        "Scrap Knight Defeated":        SKPDLocationData(106, SKPDLocationCategory.BOSS_DEFEATED, "Scrap Knight"),
        "Propeller Knight Defeated":    SKPDLocationData(107, SKPDLocationCategory.BOSS_DEFEATED, "Propeller Knight"),
        "Polar Knight Defeated":        SKPDLocationData(108, SKPDLocationCategory.BOSS_DEFEATED, "Polar Knight"),
        "Prism Knight Defeated":        SKPDLocationData(109, SKPDLocationCategory.BOSS_DEFEATED, "Prism Knight"),
        "Puzzle Knight Defeated":       SKPDLocationData(110, SKPDLocationCategory.BOSS_DEFEATED, "Puzzle Knight"),
        "Enchantress Defeated":         SKPDLocationData(111, SKPDLocationCategory.BOSS_DEFEATED, "Enchantress"),
        "Black Knight Defeated":        SKPDLocationData(112, SKPDLocationCategory.BOSS_DEFEATED, "Black Knight"),
        "Shovel Knight Defeated":       SKPDLocationData(113, SKPDLocationCategory.BOSS_DEFEATED, "Shovel Knight"),
        "Chester Defeated":             SKPDLocationData(114, SKPDLocationCategory.BOSS_DEFEATED, "Chester"),
        "Mr. Hat Defeated":             SKPDLocationData(115, SKPDLocationCategory.BOSS_DEFEATED),
        "Baz Defeated":                 SKPDLocationData(116, SKPDLocationCategory.BOSS_DEFEATED),
        "Reize Defeated":               SKPDLocationData(117, SKPDLocationCategory.BOSS_DEFEATED),
        "First Shrine":                 SKPDLocationData(118, SKPDLocationCategory.SHRINE),
        "Second Shrine":                SKPDLocationData(119, SKPDLocationCategory.SHRINE),
        "Third Shrine":                 SKPDLocationData(120, SKPDLocationCategory.SHRINE),
        "Fourth Shrine":                SKPDLocationData(121, SKPDLocationCategory.SHRINE),
    })
    
    location_index = 122

    def add_dungeon_shop_locations(location: str, characters: list):
        nonlocal location_index
        for character in characters:
            if(character != "Quandary Sage"):
                skpd_locations.update({f"{location} - {character}": SKPDLocationData(location_index, SKPDLocationCategory.DUNGEON_SHOP, character)})
                location_index += 1

    #add chester camp upgrade locations
    stock_size = 5
    max_restocks = 20
    for i in range(max_restocks):
        stock = i+1
        for j in range(stock_size):
            item = j+1
            skpd_locations.update({f"Chester Camp Shop - Stock {stock} - Item {item}": 
                                SKPDLocationData(location_index, SKPDLocationCategory.CHESTER_CAMP_SHOP, stock)})
            location_index += 1
    
    #add dungeon shop locations, each character has an unique location
    characters = get_item_from_category(SKPDItemCategory.CHARACTER)

    for i in range(8):
        add_dungeon_shop_locations(f"Dungeon {i+2} Shop", characters)
    add_dungeon_shop_locations("Scholar Sanctum Shop", characters)
    for character in characters:
        skpd_locations.update({f"Run Complete - {character}": SKPDLocationData(location_index, SKPDLocationCategory.RUN_COMPLETE, character)})
        location_index += 1
    #special chester dungeon shop location since only he can enter a shop on the first stage
    skpd_locations.update({"Dungeon 1 Shop - Chester": SKPDLocationData(location_index, SKPDLocationCategory.DUNGEON_SHOP, "Chester")})
    location_index += 1