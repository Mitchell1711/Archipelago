from typing import NamedTuple, Any
from BaseClasses import Location
from .Items import get_item_from_category, SKPDItemCategory
from enum import Enum

class SKPDLocationCategory(Enum):
    Boss_Defeated = 0
    Shrine = 1
    Dungeon_Shop = 2
    Chester_Camp_Shop = 3
    Run_Complete = 4

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
        "King Knight Defeated":         SKPDLocationData(100, SKPDLocationCategory.Boss_Defeated, "King Knight"),
        "Specter Knight Defeated":      SKPDLocationData(101, SKPDLocationCategory.Boss_Defeated, "Specter Knight"),
        "Plague Knight Defeated":       SKPDLocationData(102, SKPDLocationCategory.Boss_Defeated, "Plague Knight"),
        "Treasure Knight Defeated":     SKPDLocationData(103, SKPDLocationCategory.Boss_Defeated, "Treasure Knight"),
        "Tinker Knight Defeated":       SKPDLocationData(104, SKPDLocationCategory.Boss_Defeated, "Tinker Knight"),
        "Mole Knight Defeated":         SKPDLocationData(105, SKPDLocationCategory.Boss_Defeated, "Mole Knight"),
        "Scrap Knight Defeated":        SKPDLocationData(106, SKPDLocationCategory.Boss_Defeated, "Scrap Knight"),
        "Propeller Knight Defeated":    SKPDLocationData(107, SKPDLocationCategory.Boss_Defeated, "Propeller Knight"),
        "Polar Knight Defeated":        SKPDLocationData(108, SKPDLocationCategory.Boss_Defeated, "Polar Knight"),
        "Prism Knight Defeated":        SKPDLocationData(109, SKPDLocationCategory.Boss_Defeated, "Prism Knight"),
        "Puzzle Knight Defeated":       SKPDLocationData(110, SKPDLocationCategory.Boss_Defeated, "Puzzle Knight"),
        "Enchantress Defeated":         SKPDLocationData(111, SKPDLocationCategory.Boss_Defeated, "Enchantress"),
        "Black Knight Defeated":        SKPDLocationData(112, SKPDLocationCategory.Boss_Defeated, "Black Knight"),
        "Shovel Knight Defeated":       SKPDLocationData(113, SKPDLocationCategory.Boss_Defeated, "Shovel Knight"),
        "Chester Defeated":             SKPDLocationData(114, SKPDLocationCategory.Boss_Defeated, "Chester"),
        "Mr. Hat Defeated":             SKPDLocationData(115, SKPDLocationCategory.Boss_Defeated),
        "Baz Defeated":                 SKPDLocationData(116, SKPDLocationCategory.Boss_Defeated),
        "Reize Defeated":               SKPDLocationData(117, SKPDLocationCategory.Boss_Defeated),
        "First Shrine":                 SKPDLocationData(118, SKPDLocationCategory.Shrine),
        "Second Shrine":                SKPDLocationData(119, SKPDLocationCategory.Shrine),
        "Third Shrine":                 SKPDLocationData(120, SKPDLocationCategory.Shrine),
        "Fourth Shrine":                SKPDLocationData(121, SKPDLocationCategory.Shrine),
    })
    
    location_index = 122

    def add_dungeon_shop_locations(location: str, characters: list):
        nonlocal location_index
        for character in characters:
            if(character != "Quandary Sage"):
                skpd_locations.update({f"{location} - {character}": SKPDLocationData(location_index, SKPDLocationCategory.Dungeon_Shop, character)})
                location_index += 1

    #add chester camp upgrade locations
    stock_size = 5
    max_restocks = 20
    for i in range(max_restocks):
        stock = i+1
        for j in range(stock_size):
            item = j+1
            skpd_locations.update({f"Chester Camp Shop - Stock {stock} - Item {item}": 
                                SKPDLocationData(location_index, SKPDLocationCategory.Chester_Camp_Shop, stock)})
            location_index += 1
    
    #add dungeon shop locations, each character has an unique location
    characters = get_item_from_category(SKPDItemCategory.Character)

    for i in range(8):
        add_dungeon_shop_locations(f"Dungeon {i+2} Shop", characters)
    add_dungeon_shop_locations("Scholar Sanctum Shop", characters)
    for character in characters:
        skpd_locations.update({f"Run Complete - {character}": SKPDLocationData(location_index, SKPDLocationCategory.Run_Complete, character)})
        location_index += 1
    #special chester dungeon shop location since only he can enter a shop on the first stage
    skpd_locations.update({"Dungeon 1 Shop - Chester": SKPDLocationData(location_index, SKPDLocationCategory.Dungeon_Shop, "Chester")})
    location_index += 1