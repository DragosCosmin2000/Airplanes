import pygame

class Loading_Screen(object):
    def __init__(self, surface, surface_size, animation_duration, fps, path_to_image):
        # surface to draw on
        self.surface = surface

        # surface size
        self.surface_size = surface_size

        # animation duration
        self.animation_duration = animation_duration

        # frames per second
        self.fps = fps

        # loading's image
        self.cloud_image = 0

        # try to load the image
        self.load_image(path_to_image)

    def load_image(self, path):
        from time import sleep
        try_duration = 20

        # try to load image
        while True:
            try:
                self.cloud_image = pygame.image.load(path)
                self.cloud_image = pygame.transform.scale(self.cloud_image, (self.surface_size[0] // 2, self.surface_size[1] // 2))
                break
            except:
                if try_duration == 0:
                    raise Exception("Can't load loading image")
                try_duration -= 1
                sleep(1)

    def start_loading(self):
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.cloud_image, (0, 0))