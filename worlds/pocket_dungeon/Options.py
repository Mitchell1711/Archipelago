from dataclasses import dataclass
from Options import Toggle, Range, DefaultOnToggle, PerGameCommonOptions, Choice, OptionSet, ItemSet

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
    default = 0

class StartingCharacterIsRefract(Toggle):
    """
    Makes starting character use their refract variant.
    Characters without a refract skill won't be affected.
    """
    display_name = "Use Refract Starting Character"

class ExcludedCharacters(ItemSet):
    """
    Prevent these characters and their related locations from being shuffled into the multiworld.
    """
    display_name = "Excluded Characters"
    default = {"Quandary Sage", "Spinwulf", "Schmutz", "Beefto"}

class TotalCharacters(Range):
    """
    Cut out a percentage of playable characters from the pool at random, useful for shorter Archipelago sessions.
    100 will include all characters, 0 will only add your starting character.
    """
    display_name = "Total Characters"
    range_start = 0
    range_end = 100
    default = 100

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

class ShuffleRelics(DefaultOnToggle):
    """
    Shuffles all relics into the itempool.
    """
    display_name = "Shuffle Relics"

class ShuffleHats(Toggle):
    """
    Shuffles all hats into the itempool.
    """
    display_name = "Shuffle Hats"

class HatExpirationAction(Choice):
    """
    When any recieved hat effects wear off.
    New hat: Current hat gets removed when a new hat is sent
    End run: Current hat gets removed when dying or beating the next adventure run.
    """
    display_name = "Hat Expiration Action"
    option_new_hat = 0
    option_end_run = 1
    default = 1

class HatStackAmount(Range):
    """
    The maximum amount of hats a player is able to have at a time.
    """
    display_name = "Hat Stack Amount"
    range_start = 1
    range_end = 50
    default = 1

class ExcludedHats(ItemSet):
    """
    Prevent these hats from being shuffled into the multiworld.
    """
    display_name = "Excluded Hats"
    default = {"Shop Lock Shako", "Legendary Gold Helm", "Protracted Beeto Beret"}

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

class EndGoal(Choice):
    """
    Which condition you need to reach to finish your game.
    Normal Ending: Reach the Scholar Sanctum and defeat Puzzle Knight.
    True Ending: Collect 4 key fragments to reach the Tower of Fate and defeat the Enchantress.
    """
    display_name = "End Goal"
    option_normal_ending = 0
    option_true_ending = 1
    default = 1

@dataclass
class SKPDOptions(PerGameCommonOptions):
    end_goal: EndGoal
    starting_character: StartingCharacter
    shuffle_refract_characters: ShuffleRefractCharacters
    starting_character_is_refract: StartingCharacterIsRefract
    excluded_characters: ExcludedCharacters
    total_characters: TotalCharacters
    hub_shop_restock_count: HubShopRestockCount
    progression_type: ProgressionType
    randomize_level_order: RandomizeLevelOrder
    modded_levels: ModdedLevels
    shuffle_relics: ShuffleRelics
    shuffle_hats: ShuffleHats
    hat_expiration_action: HatExpirationAction
    hat_stack_amount: HatStackAmount
    excluded_hats: ExcludedHats
    trap_fill_percent: TrapFillPercent