from BaseClasses import MultiWorld, Region, Entrance, CollectionState
from .Locations import SKPDLocation, skpd_locations, get_location_from_category
from typing import Callable, Optional
from .Options import SKPDOptions

dungeon_amount = 10

def create_regions(world: MultiWorld, player: int, options: SKPDOptions):
    boss_table = [
        ["King Knight Defeated", "Specter Knight Defeated", "Plague Knight Defeated", "Black Knight Defeated"],
        ["Treasure Knight Defeated", "Tinker Knight Defeated", "Mole Knight Defeated", "Scrap Knight Defeated"],
        ["Propeller Knight Defeated", "Polar Knight Defeated", "Prism Knight Defeated"]
    ]

    reg_menu = create_region("Menu", player, world)
    
    #set up camp region
    reg_camp = create_region("Camp", player, world)
    for loc in get_location_from_category("Chester Camp Shop"):
        if skpd_locations[loc].data < options.hub_shop_restock_count:
            add_location(reg_camp, loc, player)

    #unused for now
    reg_quandary = create_region("Castle Quandary", player, world)

    #generic dungeon, gets randomized each run by the client
    dungeon_shops = get_location_from_category("Dungeon Shop")
    reg_dungeons = []
    for i in range(dungeon_amount):
        #create dungeon regions and add shops
        reg_dungeons.append(create_region(f"Dungeon {i+1}", player, world))
        if i != 0:
            add_dungeon_shops(reg_dungeons[i], player, dungeon_shops)
        #add shrine locations
        match i+1:
            case 3:
                for boss in boss_table[0]:
                    add_location(reg_dungeons[i], boss, player)
                add_location(reg_dungeons[i], "First Shrine", player)
            case 6:
                for boss in boss_table[1]:
                    add_location(reg_dungeons[i], boss, player)
                add_location(reg_dungeons[i], "Second Shrine", player)
            case 8:
                add_location(reg_dungeons[i], "Third Shrine", player)
            case 9:
                for boss in boss_table[2]:
                    add_location(reg_dungeons[i], boss, player)
                add_location(reg_dungeons[i], "Fourth Shrine", player)
    
    #final levels never get shuffled around
    reg_sanctum = create_region("Scholar Sanctum", player, world)
    add_location(reg_sanctum, "Puzzle Knight Defeated", player)
    add_dungeon_shops(reg_sanctum, player, dungeon_shops)

    reg_tower = create_region("Tower of Fate", player, world)
    add_location(reg_tower, "Enchantress Defeated", player)
    add_dungeon_shops(reg_tower, player, dungeon_shops)

def create_region(name: str, player: int, world: MultiWorld) -> Region:
    region = Region(name, player, world, None)
    world.regions.append(region)
    return region

def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule: Optional[Callable[[CollectionState], bool]] = None) -> Entrance:
    return world.get_region(source, player).connect(world.get_region(target, player), f"{source} to {target}", rule)

def add_location(region: Region, location: str, player: int):
    region.locations.append(SKPDLocation(player, location, skpd_locations[location].code, region))

def add_dungeon_shops(region: Region, player: int, locations: list):
    for loc in locations:
        if region.name in loc:
            add_location(region, loc, player)