from BaseClasses import MultiWorld, CollectionState, ItemClassification
from ..generic.Rules import add_rule, set_rule
from .Regions import connect_regions, dungeon_amount
from .Locations import skpd_locations
from .Items import get_item_from_category, skpd_items
from .Options import SKPDOptions

def set_rules(world: MultiWorld, player: int, options: SKPDOptions):
    #connect regions together
    connect_regions(world, player, "Menu", "Camp", None)
    connect_regions(world, player, "Camp", "Dungeon 1", None)
    
    relics = get_item_from_category("Relic")
    relevant_relics: set[str] = set()
    #only add relics that have relevancy to logic
    for relic in relics:
        if skpd_items[relic].classification == ItemClassification.progression:
            relevant_relics.add(relic)
    
    characters = get_item_from_category("Character")
    characters += get_item_from_category("Refract Character")

    for i in range(dungeon_amount - 1):
        dungeon_connection = connect_regions(world, player, f"Dungeon {i+1}", f"Dungeon {i+2}")
        add_rule(dungeon_connection, lambda state, quality=i: relic_logic(state, player, relevant_relics, quality, options.relic_leniency.value / 10))
        #add progressive dungeon rule after bosses
        if options.progression_type == 0:
            if i+1 == 3:
                add_rule(dungeon_connection, lambda state: state.has("Progressive Dungeon", player, 1))
            elif i+1 == 6:
                add_rule(dungeon_connection, lambda state: state.has("Progressive Dungeon", player, 2))
    
    dungeon_connection = connect_regions(world, player, "Dungeon 9", "Scholar Sanctum", lambda state: 
                                         relic_logic(state, player, relevant_relics, 8, options.relic_leniency.value / 10))

    connect_regions(world, player, "Scholar Sanctum", "Tower of Fate", lambda state: state.has("Key Fragment", player, 4))

    for location in world.get_locations(player):
        if skpd_locations[location.name].category == "Chester Camp Shop":
            needed_restock = skpd_locations[location.name].data - 1
            if needed_restock != 0:
                add_rule(location, lambda state, amount=needed_restock: state.has("Shop Restock", player, amount))
                #make sure players don't need to grind the first couple areas due to shop restocks
                add_rule(location, lambda state, dungeon=min(needed_restock + 1, 9): 
                         state.has("Glitched Logic", player) or state.can_reach_region(f"Dungeon {dungeon}", player))

        elif skpd_locations[location.name].category == "Dungeon Shop" or skpd_locations[location.name].category == "Run Complete":
            character = skpd_locations[location.name].data
            add_rule(location, lambda state, char=character: state.has(char, player))
            #add refract characters if enabled
            if options.shuffle_refract_characters and location.name != "Dungeon 1 Shop - Chester":
                refract_char = f"{character} B"
                if refract_char in skpd_items:
                    add_rule(location, lambda state, char=refract_char: state.has(char, player), "or")
        
        #bosses that are the same character as the one you're currently playing won't spawn
        elif skpd_locations[location.name].category == "Boss Defeated":
            character = skpd_locations[location.name].data
            if(character is not None):
                #remove boss character and the refract variant from full character list
                allowed_chars = characters.copy()
                allowed_chars.remove(character)
                allowed_chars.remove(f"{character} B")
                add_rule(location, lambda state: state.has_any(allowed_chars, player))

#calculates whether an area is feasible by counting the quality of your acquired relics
def relic_logic(state: CollectionState, player: int, items: set, required_quality: int, multiplier: float):
    #skip relic related logic for UT glitched logic
    if state.has("Glitched Logic", player):
        return True
    total_quality = 0
    for item in items:
        if state.has(item, player):
            total_quality += (skpd_items[item].data * multiplier)
    return required_quality <= total_quality