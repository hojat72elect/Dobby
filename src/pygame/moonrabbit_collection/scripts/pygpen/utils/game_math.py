import math

import pygame

def normalize(v, amt, target=0):
    if v > target + amt:
        v -= amt
    elif v < target - amt:
        v += amt
    else:
        v = target
    return v

def rectify(p1, p2):
    tl = (min(p1[0], p2[0]), min(p1[1], p2[1]))
    br = (max(p1[0], p2[0]), max(p1[1], p2[1]))
    return pygame.Rect(*tl, br[0] - tl[0] + 1, br[1] - tl[1] + 1)

def box_points(rect):
    points = []
    for y in range(rect.height):
        for x in range(rect.width):
            points.append((rect.x + x, rect.y + y))
    return points

def advance(vec, angle, amt):
    vec[0] += math.cos(angle) * amt
    vec[1] += math.sin(angle) * amt
    return vec

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)