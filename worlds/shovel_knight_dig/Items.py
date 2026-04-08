from BaseClasses import Item, ItemClassification
from typing import NamedTuple

class SKDigItem(Item):
    game: str = "Shovel Knight Dig"

class SKDigItemData(NamedTuple):
    code: int
    category: str
    classification: ItemClassification

skdig_items: dict[str, SKDigItemData] = {
    "Cog on a String":          SKDigItemData(1, "Progression", ItemClassification.progression),
    "Altius":                   SKDigItemData(2, "Progression", ItemClassification.progression),
    "Skeleton Key":             SKDigItemData(3, "Progression", ItemClassification.progression),
    "Follow Slot Upgrade":      SKDigItemData(4, "Progression", ItemClassification.progression),
    "Gems":                     SKDigItemData(5, "Filler", ItemClassification.filler),

    "Enchanted Slamvil":        SKDigItemData(10, "Accessory", ItemClassification.progression),
    "Suave Salve":              SKDigItemData(11, "Accessory", ItemClassification.progression),
    "Burrow Horns":             SKDigItemData(12, "Accessory", ItemClassification.progression),
    "Comet Collar":             SKDigItemData(13, "Accessory", ItemClassification.progression),
    "Berserker Bauble":         SKDigItemData(14, "Accessory", ItemClassification.progression),
    "Inverse Repeller":         SKDigItemData(15, "Accessory", ItemClassification.progression),
    "Lucky U-shaped Charm":     SKDigItemData(16, "Accessory", ItemClassification.progression),
    "Spikeproof Sabatons":      SKDigItemData(17, "Accessory", ItemClassification.progression),
    "Scoot Boots":              SKDigItemData(18, "Accessory", ItemClassification.progression),
    "Leaping Plume":            SKDigItemData(19, "Accessory", ItemClassification.progression),
    "Book of Bomb":             SKDigItemData(20, "Accessory", ItemClassification.progression),
    "Looking Glass":            SKDigItemData(21, "Accessory", ItemClassification.progression),
    "Platter Charm":            SKDigItemData(22, "Accessory", ItemClassification.progression),
    "Boom Rock Trigger":        SKDigItemData(23, "Accessory", ItemClassification.progression),
    "Flameo Ring":              SKDigItemData(24, "Accessory", ItemClassification.progression),
    "Bolteo Ring":              SKDigItemData(25, "Accessory", ItemClassification.progression),
    "Blast Ring":               SKDigItemData(26, "Accessory", ItemClassification.progression),
    "Blizzeo Ring":             SKDigItemData(27, "Accessory", ItemClassification.progression),
    "Gusteo Ring":              SKDigItemData(28, "Accessory", ItemClassification.progression),
    "Lucky Magic Vial":         SKDigItemData(29, "Accessory", ItemClassification.progression),
    "Tome of Relic Thrift":     SKDigItemData(30, "Accessory", ItemClassification.progression),
    "Fenix Feather":            SKDigItemData(31, "Accessory", ItemClassification.progression),
    "Shovel Blade Flint":       SKDigItemData(32, "Accessory", ItemClassification.progression),
    "Dynamo Greaves":           SKDigItemData(33, "Accessory", ItemClassification.progression),
    "Dynamo Gauntlets":         SKDigItemData(34, "Accessory", ItemClassification.progression),
    "Dirtwrecker Curse":        SKDigItemData(35, "Accessory", ItemClassification.progression),
    "Drop Spark":               SKDigItemData(36, "Accessory", ItemClassification.progression),
    "Nesting Twigs":            SKDigItemData(37, "Accessory", ItemClassification.progression),
    "Wand Wisp":                SKDigItemData(38, "Accessory", ItemClassification.progression),
    "Boulder Blade":            SKDigItemData(39, "Accessory", ItemClassification.progression),
    "Lightward Locket":         SKDigItemData(40, "Accessory", ItemClassification.progression),
    "Hoofling's Boot":          SKDigItemData(41, "Accessory", ItemClassification.progression),

    "Pandemonium Plate":        SKDigItemData(50, "Armor", ItemClassification.useful),
    "Final Guard":              SKDigItemData(51, "Armor", ItemClassification.useful),
    "Ornate Plate":             SKDigItemData(52, "Armor", ItemClassification.filler),
    "Streamline Mail":          SKDigItemData(53, "Armor", ItemClassification.useful),
    "Scrounger's Suit":         SKDigItemData(54, "Armor", ItemClassification.useful),
    "Ballistic Armor":          SKDigItemData(55, "Armor", ItemClassification.useful),
    "Conjurer's Coat":          SKDigItemData(56, "Armor", ItemClassification.useful),
    "Brash Bracers":            SKDigItemData(57, "Armor", ItemClassification.useful),
    "Combo Cuirass":            SKDigItemData(58, "Armor", ItemClassification.useful),
    "Black Knight Suit":        SKDigItemData(59, "Armor", ItemClassification.useful),
}