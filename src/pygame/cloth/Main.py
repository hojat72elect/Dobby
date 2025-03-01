import sys

import pygame

from src.pygame.cloth.ClothObj import ClothObj
from src.pygame.cloth.load_rags import load_rags

if __name__ == '__main__':

    # setup the pygame and create a window for the game
    main_clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("2D Cloth Simulation")
    screen = pygame.display.set_mode((500, 500), 0, 32)

    # Load the rag
    rag_data = load_rags('resources')
    my_cloth = ClothObj(rag_data['vine'])
    render_mode = 0

    while True:
        # Background of the screen
        screen.fill((0,0,0))

        # Get position of the mouse
        mx, my = pygame.mouse.get_pos()

        # Move the cloth to where the mouse pointer is
        my_cloth.move_grounded([mx, my])
        my_cloth.update()
        my_cloth.update_sticks()

        # render everything
        if render_mode:
            my_cloth.render_polygon(screen, (255, 255, 255))
        else:
            my_cloth.render_sticks(screen)

        # keyboards control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_r:
                    if render_mode:
                        render_mode = 0
                    else:
                        render_mode = 1

        pygame.display.update()
        main_clock.tick(60)




