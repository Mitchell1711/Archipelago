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

location_categories: dict[str, list[str]] = {}

def create_location_categories():
    for loc in skpd_locations:
        category = skpd_locations[loc].category
        if category not in location_categories:
            location_categories[category] = list()
        location_categories[category].append(loc)

def get_location_from_category(category: str) -> list[str]:
    return location_categories[category]

skpd_locations: dict[str, SKPDLocationData] = { }

def create_locations():
    skpd_locations.update({
        "King Knight Defeated":             SKPDLocationData(100, "Boss Defeated", "King Knight"),
        "Specter Knight Defeated":          SKPDLocationData(101, "Boss Defeated", "Specter Knight"),
        "Plague Knight Defeated":           SKPDLocationData(102, "Boss Defeated", "Plague Knight"),
        "Treasure Knight Defeated":         SKPDLocationData(103, "Boss Defeated", "Treasure Knight"),
        "Tinker Knight Defeated":           SKPDLocationData(104, "Boss Defeated", "Tinker Knight"),
        "Mole Knight Defeated":             SKPDLocationData(105, "Boss Defeated", "Mole Knight"),
        "Scrap Knight Defeated":            SKPDLocationData(106, "Boss Defeated", "Scrap Knight"),
        "Propeller Knight Defeated":        SKPDLocationData(107, "Boss Defeated", "Propeller Knight"),
        "Polar Knight Defeated":            SKPDLocationData(108, "Boss Defeated", "Polar Knight"),
        "Prism Knight Defeated":            SKPDLocationData(109, "Boss Defeated", "Prism Knight"),
        "Puzzle Knight Defeated":           SKPDLocationData(110, "Boss Defeated", "Puzzle Knight"),
        "Enchantress Defeated":             SKPDLocationData(111, "Boss Defeated", "Enchantress"),
        "Black Knight Defeated":            SKPDLocationData(112, "Boss Defeated", "Black Knight"),
        "Shovel Knight Defeated":           SKPDLocationData(113, "Boss Defeated", "Shovel Knight"),
        "First Shrine":                     SKPDLocationData(114, "Shrine"),
        "Second Shrine":                    SKPDLocationData(115, "Shrine"),
        "Third Shrine":                     SKPDLocationData(116, "Shrine"),
        "Fourth Shrine":                    SKPDLocationData(117, "Shrine"),
        "Win Glitzems Game":                SKPDLocationData(118, "Sideroom", "sideroom gamble"),
        "Tiefs Shop":                       SKPDLocationData(119, "Sideroom", "sideroom tief shop"),
        "Save Hedge Farmer":                SKPDLocationData(120, "Sideroom", "sideroom hedge farmer"),
        "Mr. Hat Defeated":                 SKPDLocationData(121, "Sideroom", "sideroom mrhat"),
        "Baz Defeated":                     SKPDLocationData(122, "Sideroom", "sideroom traveler"), #todo make these unique siderooms?
        "Reize Defeated":                   SKPDLocationData(123, "Sideroom", "sideroom traveler"), #yeah
        "Phantom Striker Defeated":         SKPDLocationData(124, "Sideroom", "sideroom traveler"), #idk
        "Chester Defeated":                 SKPDLocationData(125, "Sideroom", "sideroom chester"),
        "Random Sideroom 1 Cleared":        SKPDLocationData(126, "Sideroom", "sideroom2"),
        "Random Sideroom 2 Cleared":        SKPDLocationData(127, "Sideroom", "sideroom4"),
        "Item Bonus Stash":                 SKPDLocationData(128, "Sideroom", "sideroom powerup"),
        "Growth Gem Stash Sideroom Cleared":SKPDLocationData(129, "Sideroom", "sideroom egg stash"),
        "Chest Bonus Stash":                SKPDLocationData(130, "Sideroom", "sideroom chest stash"),
        "Falling Blocks Sideroom Cleared":  SKPDLocationData(131, "Sideroom", "sideroom falling blocks"),
        "Shield Sideroom Cleared":          SKPDLocationData(132, "Sideroom", "sideroom shield"),
        "Invisishade Sideroom Cleared":     SKPDLocationData(133, "Sideroom", "sideroom ghost"),
        "Stranded Ship Sideroom Cleared":   SKPDLocationData(134, "Sideroom", "sideroom ice"),
        "Lost City Sideroom Cleared":       SKPDLocationData(135, "Sideroom", "sideroom fire"),
        "Chronos Coin Sideroom Cleared":    SKPDLocationData(136, "Sideroom", "sideroom chrono coin"),
        "Survive Against Percy":            SKPDLocationData(137, "Sideroom", "sideroom bomb"),
        "Survive Against Goldarmor":        SKPDLocationData(138, "Sideroom", "sideroom cauldron"),
        "Survive Against Hoverhaft":        SKPDLocationData(139, "Sideroom", "sideroom firing"),
        "Glitzemizer Sideroom Cleared":     SKPDLocationData(140, "Sideroom", "sideroom glitzemizer"),
        "Random Puzzle Sideroom Cleared":   SKPDLocationData(150, "Sideroom", "sideroom random puzzle"),
        "Explodatorium Sideroom Cleared":   SKPDLocationData(151, "Sideroom", "sideroom poison"),
        "Sideroom with Miniboss Cleared":   SKPDLocationData(152, "Sideroom", "sideroom miniboss"),
        "Troupple Kings Blessing":          SKPDLocationData(153, "Sideroom", "sideroom troupple"),
        "Armorers Shop":                    SKPDLocationData(154, "Sideroom", "sideroom armorer"),
        "Valentines Card":                  SKPDLocationData(155, "Sideroom", "sideroom valentines")
    })
    
    location_index = 156

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
    for character in characters:
        skpd_locations.update({f"Run Complete - {character}": SKPDLocationData(location_index, "Run Complete", character)})
        location_index += 1
    #special chester dungeon shop location since only he can enter a shop on the first stage
    skpd_locations.update({"Dungeon 1 Shop - Chester": SKPDLocationData(location_index, "Dungeon Shop", "Chester")})
    location_index += 1