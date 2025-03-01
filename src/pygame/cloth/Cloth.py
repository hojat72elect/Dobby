import pygame
from src.pygame.cloth.get_dis import get_distance


class Cloth:
    def __init__(self, rag):
        self.points = [p + p for p in rag['points']]  # dupe position for last position
        self.orig_points = [p + p for p in rag['points']]
        self.sticks = []
        self.scale = rag['scale']
        for stick in rag['connections']:
            self.add_stick(stick)
        self.grounded = rag['grounded']

    def add_stick(self, points):
        self.sticks.append([points[0], points[1], get_distance(self.points[points[0]][:2], self.points[points[1]][:2])])

    def update(self):
        for i, point in enumerate(self.points):
            if i not in self.grounded:
                d_x = point[0] - point[2]
                d_y = point[1] - point[3]
                point[2] = point[0]
                point[3] = point[1]
                point[0] += d_x
                point[1] += d_y
                point[1] += 0.05

    def move_grounded(self, offset):
        for i, point in enumerate(self.points):
            if i in self.grounded:
                point[0] = self.orig_points[i][0] + offset[0] / self.scale
                point[1] = self.orig_points[i][1] + offset[1] / self.scale
                point[2] = point[0]
                point[3] = point[1]

    def update_sticks(self):
        for stick in self.sticks:
            dis = get_distance(self.points[stick[0]][:2], self.points[stick[1]][:2])
            dis_dif = stick[2] - dis
            mv_ratio = dis_dif / dis / 2
            dx = self.points[stick[1]][0] - self.points[stick[0]][0]
            dy = self.points[stick[1]][1] - self.points[stick[0]][1]
            if stick[0] not in self.grounded:
                self.points[stick[0]][0] -= dx * mv_ratio * 0.85
                self.points[stick[0]][1] -= dy * mv_ratio * 0.85
            if stick[1] not in self.grounded:
                self.points[stick[1]][0] += dx * mv_ratio * 0.85
                self.points[stick[1]][1] += dy * mv_ratio * 0.85

    def render_polygon(self, target_surface, color, offset=(0, 0)):
        y_points = [p[1] * self.scale for p in self.points]
        x_points = [p[0] * self.scale for p in self.points]
        min_x = min(x_points)
        max_x = max(x_points)
        min_y = min(y_points)
        max_y = max(y_points)
        width = int(max_x - min_x + 2)
        height = int(max_y - min_y + 2)
        surface = pygame.Surface((width, height))
        self.render_sticks(surface, (int(min_x), int(min_y)))
        surface.set_colorkey((0, 0, 0))
        mask = pygame.mask.from_surface(surface)
        outline = mask.outline()  # get outline of the mask
        surface.fill((0, 0, 0))  # fill with color that will be colorkey
        surface.set_colorkey((0, 0, 0))
        pygame.draw.polygon(surface, color, outline)
        target_surface.blit(surface, (min_x - offset[0], min_y - offset[1]))

    def render_sticks(self, surf, offset=(0, 0)):
        render_points = [[p[0] * self.scale - offset[0], p[1] * self.scale - offset[1]] for p in self.points]
        for stick in self.sticks:
            pygame.draw.line(surf, (255, 255, 255), render_points[stick[0]], render_points[stick[1]], 1)
