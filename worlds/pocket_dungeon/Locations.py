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

def get_location_from_category(category: str) -> list[str]:
    locationlist = []
    for loc in skpd_locations:
        if skpd_locations[loc].category == category:
            locationlist.append(loc)
    return locationlist

skpd_locations: dict[str, SKPDLocationData] = { }

def create_locations():
    skpd_locations.update({
        "King Knight Defeated":         SKPDLocationData(100, "Boss Defeated"),
        "Specter Knight Defeated":      SKPDLocationData(101, "Boss Defeated"),
        "Plague Knight Defeated":       SKPDLocationData(102, "Boss Defeated"),
        "Treasure Knight Defeated":     SKPDLocationData(103, "Boss Defeated"),
        "Tinker Knight Defeated":       SKPDLocationData(104, "Boss Defeated"),
        "Mole Knight Defeated":         SKPDLocationData(105, "Boss Defeated"),
        "Scrap Knight Defeated":        SKPDLocationData(106, "Boss Defeated"),
        "Propeller Knight Defeated":    SKPDLocationData(107, "Boss Defeated"),
        "Polar Knight Defeated":        SKPDLocationData(108, "Boss Defeated"),
        "Prism Knight Defeated":        SKPDLocationData(109, "Boss Defeated"),
        "Puzzle Knight Defeated":       SKPDLocationData(110, "Boss Defeated"),
        "Enchantress Defeated":         SKPDLocationData(111, "Boss Defeated"),
        "Black Knight Defeated":        SKPDLocationData(112, "Boss Defeated"),
        "Shovel Knight Defeated":       SKPDLocationData(113, "Boss Defeated"),
        "Chester Defeated":             SKPDLocationData(114, "Boss Defeated"),
        "Mr. Hat Defeated":             SKPDLocationData(115, "Boss Defeated"),
        "Baz Defeated":                 SKPDLocationData(116, "Boss Defeated"),
        "Reize Defeated":               SKPDLocationData(117, "Boss Defeated"),
        "First Shrine":                 SKPDLocationData(118, "Shrine"),
        "Second Shrine":                SKPDLocationData(119, "Shrine"),
        "Third Shrine":                 SKPDLocationData(120, "Shrine"),
        "Fourth Shrine":                SKPDLocationData(121, "Shrine"),
    })
    
    location_index = 122

    def add_dungeon_shop_locations(location: str, characters: list):
        nonlocal location_index
        for character in characters:
            if(character != "Quandary Sage"):
                skpd_locations.update({f"{location} - {character}": SKPDLocationData(location_index, "Dungeon Shop", character)})
                location_index += 1

    #add chester camp upgrade locations
    stock_size = 5
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

    for i in range(8):
        add_dungeon_shop_locations(f"Dungeon {i+2} Shop", characters)
    add_dungeon_shop_locations("Scholar Sanctum Shop", characters)
    add_dungeon_shop_locations("Tower of Fate Shop", characters)
    #special chester dungeon shop location since only he can enter a shop on the first stage
    skpd_locations.update({"Dungeon 1 Shop - Chester": SKPDLocationData(location_index, "Dungeon Shop", "Chester")})
    location_index += 1