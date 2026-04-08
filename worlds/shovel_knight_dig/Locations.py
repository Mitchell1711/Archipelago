from BaseClasses import Location
from typing import NamedTuple

class SKDigLocation(Location):
    game: str = "Shovel Knight Dig"

class SKDigLocationData(NamedTuple):
    code: int
    category: int

#placeholder location names
skdig_locations: dict[str, SKDigLocationData] = {
    "Hoofman's Shop 1":                 SKDigLocationData(1, "Hoofman's Shop"),

    "Chester Surface Shop 1":           SKDigLocationData(2, "Chester Surface Shop"),

    "Mushroom Mines - Stage 1 - Cog 1": SKDigLocationData(3, "Cog"),

    "Spore Knight Defeated":            SKDigLocationData(4, "Boss Defeated"),
    "Tinker Knight Defeated":           SKDigLocationData(5, "Boss Defeated"),
    "Mole Knight Defeated":             SKDigLocationData(6, "Boss Defeated"),
    "Hive Knight Defeated":             SKDigLocationData(7, "Boss Defeated"),
    "Scrap Knight Defeated":            SKDigLocationData(8, "Boss Defeated"),
    "Drill Knight Defeated":            SKDigLocationData(9, "Boss Defeated"),
    "The Enchantress Defeated":         SKDigLocationData(10, "Boss Defeated")
}