from dataclasses import dataclass
from Options import Toggle, Range, DefaultOnToggle, DeathLink, PerGameCommonOptions, Choice

class StartingCharacter(Choice):
    """
    Determines which character you start the game with.
    """
    display_name = "Starting Character"
    option_shovel_knight = "Shovel Knight"
    option_black_knight = "Black Knight"
    option_shield_knight = "Shield Knight"
    option_king_knight = "King Knight"
    option_specter_knight = "Specter Knight"
    option_plague_knight = "Plage Knight"
    option_mole_knight = "Mole Knight"
    option_treasure_knight = "Treasure Knight"
    option_tinker_knight = "Tinker Knight"
    option_polar_knight = "Polar Knight"
    option_propeller_knight = "Propeller Knight"
    option_scrap_knight = "Scrap Knight"
    option_prism_knight = "Prism Knight"
    option_puzzle_knight = "Puzzle Knight"
    option_mona = "Mona"
    option_chester = "Chester"
    option_enchantress = "Enchantress"
    option_quandary_sage = "Quandary Sage"
    option_spinwulf = "Spinwulf"
    option_schmutz = "Schmutz"
    option_beefto = "Beefto"
    default = "Shovel Knight"

class HubShopRestockCount(Range):
    """
    The amount of shop restock items will be shuffled into the itempool.
    Each restock adds 6 extra locations.
    """
    display_name = "Chester Camp Shop Restocks"
    range_start = 10
    range_end = 20
    default = 10

class DoProgressiveDungeons(Toggle):
    """
    Shuffles progressive dungeon items into the itempool.
    Adds a hard cap on how far the player can progress based on the amount of progressive dungeon items they posess.
    """
    display_name = "Enable Progressive Dungeons"

class DungeonStartAmount(Range):
    """
    How many progressive dungeon items the player starts with, helps with preventing a restrictive start.
    Only takes effect if progressive dungeons is turned on.
    """
    display_name = "Starting Dungeons Amount"
    range_start = 0
    range_end = 8
    default = 2

class EnableHats(Toggle):
    """
    Shuffles all hats into the itempool.
    If turned off Almond and Souffle will still be added to the pool.
    """
    display_name = "Enable Hats"

class TrapFillPercent(Range):
    """
    The percentage of filler itemslots that will be replaced by traps.
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 40

@dataclass
class SKPDOptions(PerGameCommonOptions):
    starting_character: StartingCharacter
    hub_shop_restock_count: HubShopRestockCount
    do_progressive_dungeons: DoProgressiveDungeons
    dungeon_start_amount: DungeonStartAmount
    enable_hats: EnableHats
    trap_fill_percent: TrapFillPercent
    death_link: DeathLink