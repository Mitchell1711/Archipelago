from ..AutoWorld import World, WebWorld

class SKPDWeb(WebWorld):
    theme = "grass"

class SKPDWorld(World):
    """
    SHOVEL KNIGHT YEAH
    """
    game = "Shovel Knight Pocket Dungeon"
    web = SKPDWeb()
