import json
import random
from enum import Enum

map = []
WIDTH = 30
HEIGHT = 10


class Surface(Enum):
    FIELD = 0
    SEA = 1
    SWAMP = 2
    DESERT = 3
    MOUNTAIN = 4


FILES = {
    Surface.DESERT: ["desertstone.png", "desertcactus.png"],
    Surface.FIELD: ["greenfield.png", "reeds.png", "rainbow.png"],
    Surface.MOUNTAIN: ["mountain.png"],
    Surface.SWAMP: ["swamp.png"],
    Surface.SEA: ["sea.png"]
}

# Заполняем все полями
for _x in range(WIDTH):
    for _y in range(HEIGHT):
        cell = {
            "x": _x,
            "y": _y,
            "animate": False,
            "animal": None,
            "surface": Surface.FIELD
        }
        map.append(cell)

# Добавляем имена файлов
for _cell in map:
    folder = "without_animals"
    if _cell["animate"]:
        folder = _cell["animal"]
    surface = random.choice(FILES[_cell["surface"]])
    _cell["img"] = f"diopark/{folder}/{surface}"
    _cell["surface"] = _cell["surface"].value

with open("data/map.json","w") as f:
  json.dump(map, f, indent=4)