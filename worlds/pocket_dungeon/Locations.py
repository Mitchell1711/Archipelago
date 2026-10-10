from typing import NamedTuple, Any
from BaseClasses import Location
from .Items import get_item_from_category, SKPDItemCategory
from enum import Enum
from .Options import DungeonItemAmount, HubShopRestockCount

class SKPDLocationCategory(Enum):
    Boss_Defeated = 0
    Shrine = 1
    Dungeon_Item = 2
    Chester_Camp_Shop = 3
    Run_Complete = 4
    Sideroom = 5

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
    return location_categories[category].copy()

skpd_locations: dict[str, SKPDLocationData] = { }

def create_locations():
    skpd_locations.update({
        "King Knight Defeated":             SKPDLocationData(100, SKPDLocationCategory.Boss_Defeated, "King Knight"),
        "Specter Knight Defeated":          SKPDLocationData(101, SKPDLocationCategory.Boss_Defeated, "Specter Knight"),
        "Plague Knight Defeated":           SKPDLocationData(102, SKPDLocationCategory.Boss_Defeated, "Plague Knight"),
        "Treasure Knight Defeated":         SKPDLocationData(103, SKPDLocationCategory.Boss_Defeated, "Treasure Knight"),
        "Tinker Knight Defeated":           SKPDLocationData(104, SKPDLocationCategory.Boss_Defeated, "Tinker Knight"),
        "Mole Knight Defeated":             SKPDLocationData(105, SKPDLocationCategory.Boss_Defeated, "Mole Knight"),
        "Scrap Knight Defeated":            SKPDLocationData(106, SKPDLocationCategory.Boss_Defeated, "Scrap Knight"),
        "Propeller Knight Defeated":        SKPDLocationData(107, SKPDLocationCategory.Boss_Defeated, "Propeller Knight"),
        "Polar Knight Defeated":            SKPDLocationData(108, SKPDLocationCategory.Boss_Defeated, "Polar Knight"),
        "Prism Knight Defeated":            SKPDLocationData(109, SKPDLocationCategory.Boss_Defeated, "Prism Knight"),
        "Puzzle Knight Defeated":           SKPDLocationData(110, SKPDLocationCategory.Boss_Defeated, "Puzzle Knight"),
        "Enchantress Defeated":             SKPDLocationData(111, SKPDLocationCategory.Boss_Defeated, "Enchantress"),
        "Black Knight Defeated":            SKPDLocationData(112, SKPDLocationCategory.Boss_Defeated, "Black Knight"),
        "Shovel Knight Defeated":           SKPDLocationData(113, SKPDLocationCategory.Boss_Defeated, "Shovel Knight"),
        "First Shrine":                     SKPDLocationData(114, SKPDLocationCategory.Shrine),
        "Second Shrine":                    SKPDLocationData(115, SKPDLocationCategory.Shrine),
        "Third Shrine":                     SKPDLocationData(126, SKPDLocationCategory.Shrine),
        "Fourth Shrine":                    SKPDLocationData(127, SKPDLocationCategory.Shrine),
        "Win Glitzems Game":                SKPDLocationData(118, SKPDLocationCategory.Sideroom, "sideroom gamble"),
        "Tiefs Shop":                       SKPDLocationData(119, SKPDLocationCategory.Sideroom, "sideroom tief shop"),
        "Save Hedge Farmer":                SKPDLocationData(120, SKPDLocationCategory.Sideroom, "sideroom hedge farmer"),
        "Mr. Hat Defeated":                 SKPDLocationData(121, SKPDLocationCategory.Sideroom, "sideroom mrhat"),
        "Baz Defeated":                     SKPDLocationData(122, SKPDLocationCategory.Sideroom, "sideroom traveler"), #todo make these unique siderooms?
        "Reize Defeated":                   SKPDLocationData(123, SKPDLocationCategory.Sideroom, "sideroom traveler"), #yeah
        "Phantom Striker Defeated":         SKPDLocationData(124, SKPDLocationCategory.Sideroom, "sideroom traveler"), #idk
        "Chester Defeated":                 SKPDLocationData(125, SKPDLocationCategory.Sideroom, "sideroom chester"),
        "Random Sideroom 1 Cleared":        SKPDLocationData(126, SKPDLocationCategory.Sideroom, "sideroom2"),
        "Random Sideroom 2 Cleared":        SKPDLocationData(127, SKPDLocationCategory.Sideroom, "sideroom4"),
        "Item Bonus Stash":                 SKPDLocationData(128, SKPDLocationCategory.Sideroom, "sideroom powerup"),
        "Growth Gem Stash Sideroom Cleared":SKPDLocationData(129, SKPDLocationCategory.Sideroom, "sideroom egg stash"),
        "Chest Bonus Stash":                SKPDLocationData(130, SKPDLocationCategory.Sideroom, "sideroom chest stash"),
        "Falling Blocks Sideroom Cleared":  SKPDLocationData(131, SKPDLocationCategory.Sideroom, "sideroom falling blocks"),
        "Shield Sideroom Cleared":          SKPDLocationData(132, SKPDLocationCategory.Sideroom, "sideroom shield"),
        "Invisishade Sideroom Cleared":     SKPDLocationData(133, SKPDLocationCategory.Sideroom, "sideroom ghost"),
        "Stranded Ship Sideroom Cleared":   SKPDLocationData(134, SKPDLocationCategory.Sideroom, "sideroom ice"),
        "Lost City Sideroom Cleared":       SKPDLocationData(135, SKPDLocationCategory.Sideroom, "sideroom fire"),
        "Chronos Coin Sideroom Cleared":    SKPDLocationData(136, SKPDLocationCategory.Sideroom, "sideroom chrono coin"),
        "Survive Against Percy":            SKPDLocationData(137, SKPDLocationCategory.Sideroom, "sideroom bomb"),
        "Survive Against Goldarmor":        SKPDLocationData(138, SKPDLocationCategory.Sideroom, "sideroom cauldron"),
        "Survive Against Hoverhaft":        SKPDLocationData(139, SKPDLocationCategory.Sideroom, "sideroom firing"),
        "Glitzemizer Sideroom Cleared":     SKPDLocationData(140, SKPDLocationCategory.Sideroom, "sideroom glitzemizer"),
        "Random Puzzle Sideroom Cleared":   SKPDLocationData(150, SKPDLocationCategory.Sideroom, "sideroom random puzzle"),
        "Explodatorium Sideroom Cleared":   SKPDLocationData(151, SKPDLocationCategory.Sideroom, "sideroom poison"),
        "Sideroom with Miniboss Cleared":   SKPDLocationData(152, SKPDLocationCategory.Sideroom, "sideroom miniboss"),
        "Troupple Kings Blessing":          SKPDLocationData(153, SKPDLocationCategory.Sideroom, "sideroom troupple"),
        "Armorers Shop":                    SKPDLocationData(154, SKPDLocationCategory.Sideroom, "sideroom armorer"),
        "Valentines Card":                  SKPDLocationData(155, SKPDLocationCategory.Sideroom, "sideroom valentines")
    })
    
    location_index = 156

    def add_dungeon_item_locations(location: str, characters: list):
        nonlocal location_index
        for character in characters:
            skpd_locations.update({f"{location} - {character}": SKPDLocationData(location_index, SKPDLocationCategory.Dungeon_Item, character)})
            location_index += 1

    #add chester camp upgrade locations
    stock_size = 5
    max_restocks = HubShopRestockCount.range_end
    for i in range(max_restocks):
        stock = i+1
        for j in range(stock_size):
            item = j+1
            skpd_locations.update({f"Chester Camp Shop - Stock {stock} - Item {item}": 
                                SKPDLocationData(location_index, SKPDLocationCategory.Chester_Camp_Shop, stock)})
            location_index += 1
    
    #add dungeon item locations, each character has an unique location
    characters = get_item_from_category(SKPDItemCategory.Character)

    for item in range(DungeonItemAmount.range_end):
        for dungeon in range(9):
            add_dungeon_item_locations(f"Dungeon {dungeon+1} Item {item+1}", characters)
        add_dungeon_item_locations(f"Scholar Sanctum Item {item+1}", characters)
        
    for character in characters:
        skpd_locations.update({f"Run Complete - {character}": SKPDLocationData(location_index, SKPDLocationCategory.Run_Complete, character)})
        location_index += 1