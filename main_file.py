import pygame
from network import Network
from player import Player
# pygame initialization
pygame.init()

# clock, framerate = 60 fps
clock = pygame.time.Clock()

def redrawWindow(surface, player, player2):
    surface.fill((255, 255, 255))

    # stuff
    player.draw(surface)
    player2.draw(surface)

    # update window
    pygame.display.update()

def main():
    global clock

    # create window
    # surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Airplanes")

    n = Network()

    # create player
    p = n.get_p()

    # main loop
    run = True
    FPS = 60
    while run:
        clock.tick(FPS)

        # update opponent and send me to him
        p2 = n.send(p)

        # quit check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # check for movements
        p.move()

        redrawWindow(surface, p, p2)

if __name__ == "__main__":
    main()

    pygame.quit()