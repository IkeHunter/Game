directions = {
    0: {"short": "N", "long": "NORTH"},
    1: {"short": "E", "long": "EAST"},
    2: {"short": "S", "long": "SOUTH"},
    3: {"short": "W", "long": "WEST"},
    4: {"short": "Q", "long": "QUIT"}
}

locations = {
    0: {"name": "flag", "locations": ("N", "E", "S", "Q"), "death": 0, "heal": 0,
        "directions": {"N": 1, "E": 2, "S": 3, "Q": 100}, "values": [1, 2, 3]},
    1: {"name": "tree", "locations": ("N", "E", "W", "Q"), "death": 4, "heal": 1,
        "directions": {"N": 5, "E": 2, "W": 4, "Q": 100}, "values": {5, 2, 4}},
    2: {"name": "fountain", "locations": ("N", "E", "S", "Q"), "death": 3, "heal": 4,
        "directions": {"N": 1, "E": 6, "S": 13, "Q": 100}, "values": {1, 6, 13}},
    3: {"name": "bridge", "locations": ("N", "S", "Q"), "death": 3, "heal": 1,
        "directions": {"N": 0, "S": 7, "Q": 100}, "values": {0, 7}},
    4: {"name": "path", "locations": ("N", "E", "W", "Q"), "death": 6, "heal": 0,
        "directions": {"N": 1, "E": 0, "W": 8, "Q": 100}, "values": {1, 0, 8}},
    5: {"name": "river", "locations": ("E", "S", "Q"), "death": 3, "heal": 2,
        "directions": {"E": 6, "S": 1, "Q": 100}, "values": {6, 1}},
    6: {"name": "garden", "locations": ("N", "W", "Q"), "death": 4, "heal": 1,
        "directions": {"N": 5, "W": 2, "Q": 100}, "values": {5, 2}},
    7: {"name": "forest", "locations": ("E", "Q"), "death": 9, "heal": 0,
        "directions": {"E": 10, "Q": 100}, "values": {10}},
    8: {"name": "bench", "locations": ("E", "S", "Q"), "death": 6, "heal": 1,
        "directions": {"E": 4, "S": 11, "Q": 100}, "values": {4, 11}},
    9: {"name": "statue", "locations": ("N", "S", "W", "Q"), "death": 4, "heal": 1,
        "directions": {"N": 6, "S": 12, "W": 13, "Q": 100}, "values": {6, 12, 13}},
    10: {"name": "lake", "locations": ("N", "E", "W", "Q"), "death": 3, "heal": 4,
        "directions": {"N": 13, "E": 12, "W": 7, "Q": 100}, "values": {13, 12, 7}},
    11: {"name": "coffee", "locations": ("N", "Q"), "death": 1, "heal": 2,
        "directions": {"N": 8, "Q": 100}, "values": {8}},
    12: {"name": "chest", "locations": ("N", "W", "Q"), "death": 3, "heal": 0,
        "directions": {"N": 9, "W": 10, "Q": 100}, "values": {9, 10}},
    13: {"name": "pole", "locations": ("S", "W", "Q"), "death": 6, "heal": 3,
        "directions": {"S": 10, "W": 3, "Q": 100}, "values": {10, 3}},
    100: {"name": "quit"}
}

possible_encounters = {
    0: "Nobody",
    1: "Goblin",
    2: "Doctor"
}
