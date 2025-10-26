from BaseClasses import MultiWorld, CollectionState
from ..generic.Rules import add_rule, set_rule
from .Regions import connect_regions, dungeon_amount
from .Locations import skpd_locations
from .Items import get_item_from_category, skpd_items
from .Options import SKPDOptions

def set_rules(world: MultiWorld, player: int, options: SKPDOptions):
    #connect regions together
    connect_regions(world, player, "Menu", "Camp", None)
    connect_regions(world, player, "Camp", "Castle Quandary", 
                    lambda state:  (state.has_any(["King Knight", "Treasure Knight", "Scrap Knight", "Mole Knight"], player)) and 
                    state.has_any(["Tinker Knight", "Propeller Knight", "Prism Knight", "Plague Knight"], player) and
                    state.has_any(["Shovel Knight", "Black Knight", "Polar Knight"], player))
    connect_regions(world, player, "Camp", "Dungeon 1", None)
    
    relics = get_item_from_category("Relic")
    for i in range(dungeon_amount - 1):
        dungeon_connection = connect_regions(world, player, f"Dungeon {i+1}", f"Dungeon {i+2}")
        add_rule(dungeon_connection, lambda state, quality=i: relic_logic(state, player, relics, quality, options.relic_leniency))
        #add progressive dungeon rule after bosses
        if options.progression_type == 0:
            if i+1 == 3:
                add_rule(dungeon_connection, lambda state: state.has("Progressive Dungeon", player, 1))
            elif i+1 == 6:
                add_rule(dungeon_connection, lambda state: state.has("Progressive Dungeon", player, 2))
    
    dungeon_connection = connect_regions(world, player, "Dungeon 9", "Scholar Sanctum", lambda state: 
                                         relic_logic(state, player, relics, 8, options.relic_leniency))

    connect_regions(world, player, "Scholar Sanctum", "Tower of Fate", lambda state: state.has("Key Fragment", player, 4))

    for location in world.get_locations(player):
        if skpd_locations[location.name].category == "Chester Camp Shop":
            needed_restock = skpd_locations[location.name].data - 1
            if needed_restock != 0:
                add_rule(location, lambda state, amount=needed_restock: state.has("Shop Restock", player, amount))
                #make sure players don't need to grind the first couple areas due to shop restocks
                add_rule(location, lambda state, dungeon=max(0, min(needed_restock, 9)): 
                         state.can_reach_region(f"Dungeon {dungeon}", player))

        elif skpd_locations[location.name].category == "Dungeon Shop":
            character = skpd_locations[location.name].data
            add_rule(location, lambda state, char=character: state.has(char, player))
            #add refract characters if enabled
            if options.shuffle_refract_characters and location.name != "Dungeon 1 Shop - Chester":
                refract_char = f"{character} B"
                if refract_char in skpd_items:
                    add_rule(location, lambda state, char=refract_char: state.has(char, player), "or")

#calculates whether an area is feasible by counting the quality of your acquired relics
def relic_logic(state: CollectionState, player: int, items: list, required_quality: int, multiplier: float):
    total_quality = 0
    for item in items:
        if state.has(item, player):
            total_quality += (skpd_items[item].data * multiplier)
    return required_quality <= total_quality