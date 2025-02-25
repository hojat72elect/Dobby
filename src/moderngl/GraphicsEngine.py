import sys

import moderngl
import pygame


class GraphicsEngine:
    def __init__(self, window_size=(1600, 900)):
        pygame.init()
        self.WINDOW_SIZE = window_size

        # set up open gl attributes
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        pygame.display.set_mode(size=self.WINDOW_SIZE, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        self.opengl_context = moderngl.create_context()
        self.clock = pygame.time.Clock()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def render(self):
        # clear the frame buffer (instead of being from 0 to 255, our colors are from 0.0 to 1.0)
        self.opengl_context.clear(color=(0.08, 0.16, 0.18, 1.0))
        # swap the buffers
        pygame.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.render()
            self.clock.tick(60)

