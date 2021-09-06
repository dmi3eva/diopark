from diopark.album import *
# from album import *
from copy import deepcopy
import os
import json

with open("diopark/data/map.json","r") as f:
  map = json.load(f)

# with open("../data/map.json","r") as f:
#   map = json.load(f)

with_animals = [_c for _c in map if _c["animate"]]
without_animals = [_c for _c in map if not _c["animate"]]

surfaces = [
    [_c for _c in map if _c["surface"] == i]
    for i in range(5)
]


SURFACES_MAPPING = {
    "FIELD": 0,
    "SEA": 1,
    "SWAMP": 2,
    "DESERT": 3,
    "MOUNTAIN": 4
}

def dio_union(map_1, map_2):
    hash_1 = {(_c["x"], _c["y"]): _c for _c in map_1}
    hash_2 = {(_c["x"], _c["y"]): _c for _c in map_2}
    all = deepcopy(hash_1)
    all.update(hash_2)
    hash_result = list(set(hash_1.keys()).union(hash_2.keys()))
    return [_v for _k, _v in all.items() if _k in hash_result]

def dio_intersection(map_1, map_2):
    hash_1 = {(_c["x"], _c["y"]): _c for _c in map_1}
    hash_2 = {(_c["x"], _c["y"]): _c for _c in map_2}
    all = deepcopy(hash_1)
    hash_result = list(set(hash_1.keys()).intersection(hash_2.keys()))
    return [_v for _k, _v in all.items() if _k in hash_result]


def execute_animals(condition):
    if "without" in condition:
        return without_animals
    return with_animals

def execute_surface(condition):
    for _name, _value in SURFACES_MAPPING.items():
        if _name in condition.upper():
            return surfaces[_value]


def execute_coordinates_equal(a, b, c):
    cells = [_c for _c in map if a*_c["x"]+b*_c["y"]+c==0]
    return cells


def execute_coordinates_less(a, b, c):
    cells = [_c for _c in map if a*_c["x"]+b*_c["y"]+c<0]
    return cells


def execute_coordinates_greater(a, b, c):
    cells = [_c for _c in map if a*_c["x"]+b*_c["y"]+c>0]
    return cells

def extract_coefs(expression):
    a = 0
    b = 0
    c = 0
    if "x" in expression:
        a = 1
        ind = expression.index("x")
        koef = ""
        while ind > 0 and expression[ind - 1].isnumeric():
            koef = expression[ind - 1] + koef
            ind -= 1
        if len(koef) > 0:
            a = int(koef)
        if ind >= 0 and expression[ind - 1] == "-":
            a *= -1
            expression = expression[:ind - 1] +expression[ind:]
        if ind >= 0 and expression[ind - 1] == "+":
            expression = expression[:ind - 1] +expression[ind:]
        expression = expression.replace("x", "")
        if len(koef) > 0:
            expression = expression.replace(koef, "")
    if "y" in expression:
        b = 1
        ind = expression.index("y")
        koef = ""
        while ind > 0 and expression[ind - 1].isnumeric():
            koef = expression[ind - 1] + koef
            ind -= 1
        if len(koef) > 0:
            b = int(koef)
        if ind >= 0 and expression[ind - 1] == "-":
            b *= -1
            expression = expression[:ind - 1] +expression[ind:]
        if ind >= 0 and expression[ind - 1] == "+":
            expression = expression[:ind - 1] +expression[ind:]
        expression = expression.replace("y", "")
        if len(koef) > 0:
            expression = expression.replace(koef, "")
    k = 1
    if "+" in expression:
        expression = expression.replace("+", "")
    if "-" in expression:
        expression = expression.replace("-", "")
        k = -1
    if expression.isnumeric():
        c = int(expression) * k
    elif len(expression) > 0:
        raise ValueError("Ошибка в условии с координатами")
    return {
        "a": a,
        "b": b,
        "c": c
    }


def execute_coordinates(condition):
    signs = ["=", "<", ">"]
    sign = [_s for _s in condition if _s in signs]
    if len(sign) > 1:
        raise ValueError("В вашем условии несколько знаков сравнения")
    sign = sign[0]
    left_part = condition.split(sign[0])[0]
    right_part = condition.split(sign[0])[1]
    left_coefs = extract_coefs(left_part)
    right_coefs = extract_coefs(right_part)
    coefs = {
        "a": left_coefs["a"] - right_coefs["a"],
        "b": left_coefs["b"] - right_coefs["b"],
        "c": left_coefs["c"] - right_coefs["c"]
    }
    if sign == "=":
        return execute_coordinates_equal(coefs["a"], coefs["b"], coefs["c"])
    if sign == ">":
        return execute_coordinates_greater(coefs["a"], coefs["b"], coefs["c"])
    if sign == "<":
        return execute_coordinates_less(coefs["a"], coefs["b"], coefs["c"])
    raise ValueError("Не хватает знака сравнения")


def execute_one_condiotion(condition):
    if "=" in condition or ">" in condition or "<" in condition:
        return execute_coordinates(condition)
    if "animal" in condition:
        return execute_animals(condition)
    return execute_surface(condition)


def execute_and_expression(condition):
    ands = condition.split("and")
    result = []
    for ind, _and in enumerate(ands):
        and_result = execute_one_condiotion(_and)
        if ind > 0:
            result = dio_intersection(result, and_result)
        else:
            result = and_result
    return result

def execute_condition(condition):
    while " " in condition:
        condition = condition.replace(" ", "")
    condition = condition.lower()
    if "х" in condition:
        condition.replace("х", "x")
    # Фотографируем все
    if len(condition) == 0:
        return Album(map)
    ors = condition.split("or")
    result = []
    for _or in ors:
        or_result = execute_and_expression(_or)
        result = dio_union(result, or_result)
    return Album(result)


class Drone:
    def __init__(self):
        pass

    def photo(self, condition):
        return execute_condition(condition)

# album = execute_condition("x=5 and y = 7")
# album.print_size()
# album.print_avg_light()

# drone = Drone("x=5")
# album = execute_condition("x=5 and y = 7")