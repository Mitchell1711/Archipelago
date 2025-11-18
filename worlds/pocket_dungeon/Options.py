from dataclasses import dataclass
from Options import Toggle, Range, DefaultOnToggle, PerGameCommonOptions, Choice, OptionSet, ItemSet, OptionCounter

class StartingCharacter(Choice):
    """
    Determines which character you start the game with.
    """
    display_name = "Starting Character"
    option_shovel_knight = 0
    option_black_knight = 1
    option_shield_knight = 2
    option_king_knight = 3
    option_specter_knight = 4
    option_plague_knight = 5
    option_mole_knight = 6
    option_treasure_knight = 7
    option_tinker_knight = 8
    option_polar_knight = 9
    option_propeller_knight = 10
    option_scrap_knight = 11
    option_prism_knight = 12
    option_puzzle_knight = 13
    option_mona = 14
    option_chester = 15
    option_enchantress = 16
    option_quandary_sage = 17
    option_spinwulf = 18
    option_schmutz = 19
    option_beefto = 20
    default = option_shovel_knight

    charlist = ["Shovel Knight", 
                "Black Knight", 
                "Shield Knight", 
                "King Knight", 
                "Specter Knight", 
                "Plague Knight", 
                "Mole Knight", 
                "Treasure Knight",
                "Tinker Knight",
                "Polar Knight",
                "Propeller Knight",
                "Scrap Knight",
                "Prism Knight",
                "Puzzle Knight",
                "Mona",
                "Chester",
                "Enchantress",
                "Quandary Sage",
                "Spinwulf",
                "Schmutz",
                "Beefto"]

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
    None: Progression logic is only based on the amount of relics you've collected, there's no hard cap on how far you can get in a run.
    """
    display_name = "Progression Type"
    option_progressive_dungeons = 0
    option_none = 1
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

class FillerWeights(OptionCounter):
    """
    Determines how often each filler item appears in the itempool
    """
    display_name = "Filler Weights"
    default = {
        "1000 Gems": 45,
        "2500 Gems": 35,
        "5000 Gems": 20
    }

class DungeonShopHints(Toggle):
    """
    Toggles behavior of dungeon shops when selling archipelago items.
    On: Dungeon shops will show which item they're selling before purchase but will cost a variable amount of gems.
    Off: Dungeon shops won't show which item they're selling but the item can be picked up for free.
    """
    display_name = "Item Shop Hints"

class RelicLeniency(Range):
    """
    Multiplier that affects how strict relic logic will be.
    If less than 1, more relics will be considered required to progress to the next dungeon.
    The opposite holds true if set to more than 1.
    """
    display_name = "Relic Leniency"
    default = 1
    range_start = 0.25
    range_end = 2

class EarlyMealTicket(DefaultOnToggle):
    """
    Places the meal ticket in an early sphere to prevent characters with low health from getting stuck.
    """
    display_name = "Early Meal Ticket"

class StartingRelicSlotAmount(Range):
    """
    How many "Starting Relic Slot" items get shuffled into the itempool.
    Each slot adds a randomized relic at the start of an adventure run. Helps with speeding up the late game a bit.
    """
    display_name = "Starting Relic Slot Amount"
    default = 0
    range_start = 0
    range_end = 10

class RandomizeBosses(Toggle):
    """
    Shuffles boss locations around on the adventure mode map. 
    """
    display_name = "Randomize Bosses"

@dataclass
class SKPDOptions(PerGameCommonOptions):
    starting_character: StartingCharacter
    shuffle_refract_characters: ShuffleRefractCharacters
    starting_character_is_refract: StartingCharacterIsRefract
    excluded_characters: ExcludedCharacters
    total_characters: TotalCharacters
    hub_shop_restock_count: HubShopRestockCount
    progression_type: ProgressionType
    randomize_level_order: RandomizeLevelOrder
    randomize_bosses: RandomizeBosses
    modded_levels: ModdedLevels
    shuffle_relics: ShuffleRelics
    shuffle_hats: ShuffleHats
    hat_expiration_action: HatExpirationAction
    hat_stack_amount: HatStackAmount
    excluded_hats: ExcludedHats
    trap_fill_percent: TrapFillPercent
    filler_weights: FillerWeights
    dungeon_shop_hints: DungeonShopHints
    relic_leniency: RelicLeniency
    early_meal_ticket: EarlyMealTicket
    staring_relic_slot_amount: StartingRelicSlotAmount