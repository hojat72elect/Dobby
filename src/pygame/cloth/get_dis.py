import math


def get_distance(point1: list[float], point2: list[float]):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
