import os
import json
import random
from enum import Enum

map = []
WIDTH = 101
HEIGHT = 102


class Surface(Enum):
    FIELD = 0
    SEA = 1
    SWAMP = 2
    DESERT = 3
    MOUNTAIN = 4


FILES = {
    "without_animals": {
        Surface.DESERT: ["desertstone.png", "desertcactus.png"],
        Surface.FIELD: ["greenfield.png", "reeds.png", "rainbow.png"],
        Surface.MOUNTAIN: ["mountain.png"],
        Surface.SWAMP: ["swamp.png"],
        Surface.SEA: ["sea.png"]
    },
    "barrel":{
        Surface.FIELD: ["greenfield.png"],
        Surface.SEA: ["sea.png"]
    },
    "criminals": {
        Surface.FIELD: ["greenfield.png"],
    },
    "elephants": {
        Surface.DESERT: ["desertcactus.png"],
        Surface.FIELD: ["greenfield.png", "reeds.png"],
        Surface.SEA: ["sea.png"]},
    "geese": {
        Surface.FIELD: ["reeds.png", "rainbow.png"],
        Surface.SWAMP: ["swamp.png"],
        Surface.SEA: ["sea.png"]
    },
    "gekkons": {
        Surface.DESERT: ["desertstone.png", "desertcactus.png"]
    },
    "koalas": {
        Surface.FIELD: ["reeds.png", "rainbow.png"],
    },
    "lamas": {
        Surface.DESERT: ["desertstone.png"],
        Surface.FIELD: ["greenfield.png", "reeds.png", "rainbow.png"]
    },
    "loafers": {
        Surface.DESERT: ["desertstone.png"],
        Surface.FIELD: ["reeds.png"],
    },
    "zebras": {
        Surface.DESERT: ["desertstone.png", "desertcactus.png"],
        Surface.FIELD: ["greenfield.png", "reeds.png", "rainbow.png"],
        Surface.MOUNTAIN: ["mountain.png"],
    }
}
BY_SURF = {}
for animal, values in FILES.items():
    for surf in values.keys():
        BY_SURF[surf] = BY_SURF.get(surf, []) + [animal]

FREQUENCIES = [Surface.FIELD] * 10 + [Surface.MOUNTAIN] * 3 + [Surface.SEA] + [Surface.SWAMP] + [Surface.DESERT] * 2
ANIMALS = {
    "barrel": []
}

# Заполняем все полями
for _x in range(WIDTH):
    for _y in range(HEIGHT):
        cell = {
            "x": _x,
            "y": _y,
            "animate": False,
            "animal": None,
            "surface": random.choice(FREQUENCIES),
            "light": max(0, _x * _x - _y + 10)
        }
        map.append(cell)


# Добавляем животных
for _cell in map:
    surf = _cell["surface"]
    animal = random.choice(BY_SURF[surf])
    if animal not in ["without_animals", "criminals", "barrel"]:
        _cell["animate"] = True
        _cell["animal"] = animal
    # Добавляем слона
    if _cell["x"] == _cell["y"] and random.choice([0, 1]) == 0 and "elephants" in BY_SURF[_cell["surface"]]:
        _cell["animate"] = True
        _cell["animal"] = "elephants"

# Добавляем имена файлов
for _cell in map:
    folder = "without_animals"
    if _cell["animate"]:
        folder = _cell["animal"]
    if _cell["surface"] not in FILES[folder].keys():
        print(folder)
    surface = random.choice(FILES[folder][_cell["surface"]])
    _cell["img"] = f"diopark/photos/{folder}/{surface}"
    if not os.path.exists(_cell["img"].replace("diopark/", "")):
        print(_cell["img"])
    _cell["surface"] = _cell["surface"].value

# Добавляем зебру
row_5 = [_c for _c in map if _c["x"] == 5]
ind = random.randint(0, len(row_5) - 1)
row_5[ind]["animate"] = True
row_5[ind]["animal"] = "zebras"
row_5[ind]["surface"] = Surface.SWAMP.value
row_5[ind]["img"] = "diopark/photos/zebras/swamp.png"

# Добавляем браконьеров
cr = [_c for _c in map if _c["x"] == 49 and _c["y"] == 49][0]
cr["animate"] = True
cr["animal"] = "criminals"
cr["surface"] = Surface.FIELD.value
cr["img"] = "diopark/photos/criminals/greenfield.png"

# Добавляем бочку
b = [_c for _c in map if _c["x"] == 12 and _c["y"] == 24][0]
b["animate"] = True
b["animal"] = "barrel"
b["surface"] = Surface.FIELD.value
b["img"] = "diopark/photos/barrel/sea.png"

with open("data/map.json","w") as f:
  json.dump(map, f, indent=4)