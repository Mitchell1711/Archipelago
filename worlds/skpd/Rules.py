from BaseClasses import MultiWorld
from ..generic.Rules import add_rule, set_rule
from .Regions import connect_regions, dungeon_amount
from .Locations import skpd_locations

def set_rules(world: MultiWorld, player: int):
    #connect regions together
    connect_regions(world, player, "Menu", "Camp", None)
    connect_regions(world, player, "Camp", "Castle Quandary", 
                    lambda state:  (state.has_any(["King Knight", "Treasure Knight", "Scrap Knight", "Mole Knight"], player)) and 
                    state.has_any(["Tinker Knight", "Propeller Knight", "Prism Knight", "Plague Knight"], player) and
                    state.has_any(["Shovel Knight", "Black Knight", "Polar Knight"], player))
    connect_regions(world, player, "Camp", "Dungeon 1", None)
    
    for i in range(dungeon_amount - 1):
        connect_regions(world, player, f"Dungeon {i+1}", f"Dungeon {i+2}", lambda state: state.has("Progressive Dungeon", player, i+1))
    
    connect_regions(world, player, "Dungeon 9", "Scholar Sanctum", None)
    connect_regions(world, player, "Scholar Sanctum", "Tower of Fate", lambda state: state.has("Key Fragment", player, 4))

    for location in world.get_locations(player):
        if skpd_locations[location.name].category == "Chester Camp Shop":
            needed_restock = int(skpd_locations[location.name].data - 1)
            if needed_restock != 0:
                set_rule(location, lambda state: state.has("Shop Restock", player, needed_restock))

        elif skpd_locations[location.name].category == "Dungeon Shop":
            set_rule(location, lambda state: state.has(str(skpd_locations[location.name].data), player))
            if skpd_locations[location.name].data == "Random Knight":
                add_rule(location, lambda state: state.has("Almond", player))
            elif skpd_locations[location.name].data == "Shuffle Knight":
                add_rule(location, lambda state: state.has("Souffle", player))