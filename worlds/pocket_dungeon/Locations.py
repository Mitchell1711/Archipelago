from typing import NamedTuple, Any
from BaseClasses import Location
from .Items import get_item_from_category
import math

class SKPDLocation(Location):
    game: str = "Shovel Knight Pocket Dungeon"

class SKPDLocationData(NamedTuple):
    code: int
    category: str
    data: Any = None

def get_location_from_category(category: str) -> list:
    locationlist = []
    for loc in skpd_locations:
        if skpd_locations[loc].category == category:
            locationlist.append(loc)
    return locationlist

skpd_locations: dict[str, SKPDLocationData] = { }

def create_locations():
    skpd_locations.update({
        "King Knight Defeated":         SKPDLocationData(101, "Boss Defeated"),
        "Specter Knight Defeated":      SKPDLocationData(102, "Boss Defeated"),
        "Plague Knight Defeated":       SKPDLocationData(103, "Boss Defeated"),
        "Treasure Knight Defeated":     SKPDLocationData(104, "Boss Defeated"),
        "Tinker Knight Defeated":       SKPDLocationData(105, "Boss Defeated"),
        "Mole Knight Defeated":         SKPDLocationData(106, "Boss Defeated"),
        "Scrap Knight Defeated":        SKPDLocationData(107, "Boss Defeated"),
        "Propeller Knight Defeated":    SKPDLocationData(108, "Boss Defeated"),
        "Polar Knight Defeated":        SKPDLocationData(109, "Boss Defeated"),
        "Prism Knight Defeated":        SKPDLocationData(110, "Boss Defeated"),
        "Puzzle Knight Defeated":       SKPDLocationData(111, "Boss Defeated"),
        "Enchantress Defeated":         SKPDLocationData(112, "Boss Defeated"),
        "Black Knight Defeated":        SKPDLocationData(113, "Boss Defeated"),
        "Shovel Knight Defeated":       SKPDLocationData(114, "Boss Defeated"),
        "Chester Defeated":             SKPDLocationData(115, "Boss Defeated"),
        "Mr. Hat Defeated":             SKPDLocationData(116, "Boss Defeated"),
        "Baz Defeated":                 SKPDLocationData(117, "Boss Defeated"),
        "Reize Defeated":               SKPDLocationData(118, "Boss Defeated"),
        "First Shrine":                 SKPDLocationData(125, "Shrine"),
        "Second Shrine":                SKPDLocationData(126, "Shrine"),
        "Third Shrine":                 SKPDLocationData(127, "Shrine"),
        "Fourth Shrine":                SKPDLocationData(128, "Shrine"),
    })
    
    location_index = 200

    #add chester camp upgrade locations
    stock_size = 6
    max_restocks = 20
    for i in range(max_restocks):
        stock = i+1
        for j in range(stock_size):
            item = j+1
            skpd_locations.update({f"Chester Camp Shop - Stock {stock} - Item {item}": 
                                SKPDLocationData(location_index, "Chester Camp Shop", stock)})
        location_index += 1
    
    #add dungeon shop locations, each character has an unique location
    characters = get_item_from_category("Character")
    print(characters)

    for i in range(8):
        location_index = add_dungeon_shop_locations(f"Dungeon {i+2} Shop", characters, location_index)
    location_index = add_dungeon_shop_locations("Scholar Sanctum Shop", characters, location_index)
    location_index = add_dungeon_shop_locations("Tower of Fate Shop", characters, location_index)

def add_dungeon_shop_locations(location: str, characters: list, location_index: int) -> int:
    for character in characters:
        skpd_locations.update({f"{location} - {character}": SKPDLocationData(location_index, "Dungeon Shop", character)})
        location_index += 1
    return location_index