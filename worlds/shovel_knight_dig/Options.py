from dataclasses import dataclass
from Options import PerGameCommonOptions, OptionGroup, Toggle

class DummyOption(Toggle):
    """
    This is a dummy option
    """

@dataclass
class SKDigOptions(PerGameCommonOptions):
    dummy_option: DummyOption

SKDig_option_groups = [
    OptionGroup("Dummy Optiongroup", [
        DummyOption
    ])
]