from typing import Any, Dict

SKPD_option_presets: Dict[str, Dict[str, Any]] = {
    "Vanilla Flavor": {
        "total_characters": 21,
        "progression_type": 1,
        "shuffle_relics": True,
        "early_meal_ticket": False,
        "start_inventory_from_pool": {
            "Meal Ticket": 1, 
            "Premium Meal Ticket": 1, 
            "Diamond Dust": 1, 
            "Obsidian Drill": 1, 
            "Snoutin' Charm": 1,
            "Shockproof Socks": 1,
            "Fizzle Wand": 1,
            "Bomb Seed Bag": 1,
            "Nimbus Balloon": 1,
            "Potion Napkin": 1,
            "Dynamallet": 1,
            "Power Pail": 1,
            "Desperation Talon": 1,
            "Gem Chain": 1,
            "Gem Beet": 1
        },
        "dungeon_item_amount": 1,
        "staring_relic_slot_amount": 0
    },
    "Surprise Legendary Quest": {
        "filler_weights": {
            "1000 Gems": 40,
            "2500 Gems": 35,
            "5000 Gems": 20,
            "Garbage": 20,
            "Legendary Gold Helm": 5
        },
        "hat_expiration_action": 0,
        "hat_stack_amount": 1
    },
    "Quickplay": {
        "total_characters": 4,
        "camp_shop_starting_price": 5000,
        "camp_shop_price_modifier": 1000,
        "dungeon_item_amount": 3
    },
    "Maximum Checks": {
        "total_characters": 21,
        "excluded_characters": {},
        "hub_shop_restock_count": 20,
        "dungeon_item_amount": 4,
        "staring_relic_slot_amount": 10
    },
    "Helpful Hats": {
        "filler_weights": {
            "1000 Gems": 40,
            "2500 Gems": 35,
            "5000 Gems": 20,
            "Garbage": 20,
            "Connoisseur's Cap": 10,
            "Fleeto Beret": 10,
            "Turkey Toque": 10,
            "Taming Topper": 10,
            "Bohto Boater": 10,
            "Present Hat": 10,
            "Bugle Hat": 10
        },
        "hat_expiration_action": 1,
        "hat_stack_amount": 2
    }
}