import pygame, sys

"""
example 1 : just shows a simple window with black background..
"""

pygame.init()
display_surface = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Example 1')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()