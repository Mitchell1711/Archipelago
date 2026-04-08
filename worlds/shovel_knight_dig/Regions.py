from BaseClasses import MultiWorld, Region, Entrance, CollectionState
from .Locations import SKDigLocation, skdig_locations
from .Options import SKDigOptions
from typing import Callable, Optional

def create_regions(world: MultiWorld, player: int, options: SKDigOptions):
    reg_menu = create_region("Menu", player, world)

    #add hoofman shop location as test
    #the menu region is always accessible from the start
    add_location(reg_menu, "Hoofman's Shop 1", player)

    #add win condition to menu so the generator doesn't complain the game is unbeatable
    add_location(reg_menu, "The Enchantress Defeated", player)

def add_location(region: Region, location: str, player: int):
    """
    Adds a location to a region
    """
    region.locations.append(SKDigLocation(player, location, skdig_locations[location].code, region))

def create_region(name: str, player: int, world: MultiWorld) -> Region:
    """
    Create a region and add it to the multiworld
    """
    region = Region(name, player, world, None)
    world.regions.append(region)
    return region

def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule: Optional[Callable[[CollectionState], bool]] = None) -> Entrance:
    """
    Connect a region to another region, usually called from set_rules
    """
    return world.get_region(source, player).connect(world.get_region(target, player), f"{source} to {target}", rule)