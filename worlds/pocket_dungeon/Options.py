from dataclasses import dataclass
from Options import Toggle, Range, DefaultOnToggle, DeathLink, PerGameCommonOptions, Choice, OptionSet, FreeText

class StartingCharacter(FreeText):
    """
    Determines which character you start the game with.
    Refract characters use their name + B (eg. Shovel Knight B)
    """
    display_name = "Starting Character"
    default = "Shovel Knight"

class ShuffleRefractCharacters(DefaultOnToggle):
    """
    Shuffles the refract variants of all characters into the itempool.
    """
    display_name = "Shuffle Refract Characters"

class HubShopRestockCount(Range):
    """
    The amount of shop restock items will be shuffled into the itempool.
    Each restock adds 5 extra locations.
    """
    display_name = "Chester Camp Shop Restocks"
    range_start = 5
    range_end = 20
    default = 10

class ProgressionType(Choice):
    """
    How to handle game progression.
    Progressive Dungeons: adds a hard cap on how far the player can progress based on the amount of progressive dungeon items they posess.
    Key Hunt: Keys stop spawning inside of levels and will be shuffled into the multiworld, each run starts with your amount of collected keys.
    None: Progression logic is only based on the amount of relics you've collected, there's no hard cap on how far you can get in a run.
    """
    display_name = "Progression Type"
    option_progressive_dungeons = 0
    option_key_hunt = 1
    option_none = 2
    default = 0

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

class RandomizeLevelOrder(Toggle):
    """
    Shuffles around level themes, does not have an effect on logic.
    Different from the "shuffle all" in-game option as the level shuffle will be unique to each Archipelago world.
    """
    display_name = "Randomize Level Order"

class ModdedLevels(OptionSet):
    """
    Add level ids for any modded levels you may want to include in the level shuffle.
    This doesn't need to be set if randomize level order is disabled.
    """
    display_name = "Modded Levels"
    default = {}

@dataclass
class SKPDOptions(PerGameCommonOptions):
    starting_character: StartingCharacter
    shuffle_refract_characters: ShuffleRefractCharacters
    hub_shop_restock_count: HubShopRestockCount
    progression_type: ProgressionType
    randomize_level_order: RandomizeLevelOrder
    modded_levels: ModdedLevels
    enable_hats: EnableHats
    trap_fill_percent: TrapFillPercent
    death_link: DeathLink