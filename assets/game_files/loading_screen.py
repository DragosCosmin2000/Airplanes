import pygame

class Loading_Screen(object):
    def __init__(self, surface, surface_size, animation_duration, fps, path_to_image):
        # loading flag
        self.loading_flag = True

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

        # cloud color (cyan)
        self.cloud_color = (0, 255, 255)

        # cloud filler rect, x and width never change - I put some value to cover the cloud,
        # FOR "x" - self.surface_size[0] // 4 (where image starts) + some little space to make sure that it doesn't come out
        # FOR "width" - self.surface_size[0] // 2 (that's the dimension of the image) - 2 * that little space mentioned above
            # (double because we have two little spaces: the left and the right)
        self.cloud_filler = (self.surface_size[0] // 4 + self.surface_size[0] // 40, self.surface_size[1] // 4, self.surface_size[0] // 2 - self.surface_size[0] // 20, 200)

        # filler segment dimension, total filler size // how many frames are gonna be shown for animation
        self.filler_segment = (self.surface_size[1] // 2 - self.surface_size[1] // 20) / (self.fps * self.animation_duration)

        # filler animation progression
        self.filler_progression = 0

        # filler top margin(to determine where the filler(which is a rect) starts), from this I'll take self.filler_progression * self.filler_segment
        self.filler_top_margin = 3 * self.surface_size[1] // 4 - self.surface_size[1] // 40

        # TEXT ANIMATION ---------------

        # animation stages
        #1
        # "first pause", before first text

        #2
        # "fade in", fade first text in
        # "keep", keep text visible
        # "fade out", fade first text out

        #3
        # "second pause", before second text

        #4
        # "fade in", fade second text in
        # "keep", keep text visible
        # "fade out", fade second text out

        #5
        # "last pause", stop loading screen after this
        self.text_animation_stage = "first pause"

        # text animation progression
        self.text_animation_progression = 0

        # font, text
        self.current_text = ""

        self.font = pygame.font.Font("assets\\game_fonts\\ShortStack-Regular.ttf", self.surface_size[0] // 80)

        self.text = self.font.render("created by Tudorache Dragos", True, (255, 255, 255), (255, 255, 255))

        self.text_rect = self.text.get_rect()

        # text location
        self.text_rect_center = (self.surface_size[0] // 2, 5 * self.surface_size[1] // 8 + self.text.get_size()[1])

        # set text location
        self.text_rect.center = self.text_rect_center

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

    def start_loading(self, wait_for_content_load):
        # fill the bg with cloud image color
        self.surface.fill((255, 255, 255))

        # draw the filler
        pygame.draw.rect(self.surface, self.cloud_color, self.cloud_filler)
        if self.filler_progression < self.fps * self.animation_duration:
            self.cloud_filler = (self.cloud_filler[0], self.filler_top_margin - self.filler_progression * self.filler_segment, self.cloud_filler[2], self.filler_progression * self.filler_segment)
            self.filler_progression += 1

        # display cloud image in the center
        self.surface.blit(self.cloud_image, (self.surface_size[0] // 4, self.surface_size[1] // 4))

        # display text, make pauses and transitions
        if self.filler_progression >= self.fps * self.animation_duration:
            self.run_text_animation()

    def run_text_animation(self):
        if self.text_animation_stage == "first pause" or self.text_animation_stage == "second pause" or self.text_animation_stage == "last pause":
            # 1 second pause
            if self.text_animation_progression == self.fps // 2:
                # if it is last pause, stop the loading after pause
                if self.text_animation_stage == "last pause":
                    self.loading_flag = False

                # every pause (except last, see above why) is followed by a "fade in" transition for text
                self.text_animation_stage = "fade in"

                # That becomes 255 because the white's rgb is (255, 255, 255) and to make that "fade in" transition
                    # I need to get (0, 255, 255) = cyan from (255, 255, 255), so... I just decrease self.text_animation_progression
                        # until I get (self.text_animation_progression, 255, 255) where self.text_animation_progression is 0
                            # Also, I update the text color every frame to make a smooth transition
                self.text_animation_progression = 255
            else:
                # just increase it until the pause is finished(until self.text_animation_progression is equal to self.fps // 2, look above)
                self.text_animation_progression += 1

            # get the text
            if self.text_animation_stage == "first pause":
                self.current_text = "created by Tudorache Dragos"
            elif self.text_animation_stage == "second pause":
                self.current_text = "Have fun"

        # The "fade in" transition is explained above, line 129
        elif self.text_animation_stage == "fade in":
            # when the transition finished change to "keep" and display the text for some seconds
            if self.text_animation_progression == 0:
                self.text_animation_stage = "keep"
            else:
                # I explained why I did this above, line 129
                self.text_animation_progression -= (255 // self.fps + 1)
                if self.text_animation_progression < 0:
                    self.text_animation_progression = 0

            # update the text and display it
            self.text = self.font.render(self.current_text, True, (self.text_animation_progression, 255, 255), (255, 255, 255))
            self.text_rect = self.text.get_rect()
            self.text_rect.center = self.text_rect_center
            self.surface.blit(self.text, self.text_rect)

        # Just wait and display text normally
        elif self.text_animation_stage == "keep":
            if self.text_animation_progression == 2 * self.fps:
                self.text_animation_stage = "fade out"
                self.text_animation_progression = 0
            else:
                self.text_animation_progression += 1

            # display the text
            self.surface.blit(self.text, self.text_rect)

        # Same for "fade out", but in the opposite way, I need to get (255, 255, 255) from (0, 255, 255). Look line 129 for explanation
        elif self.text_animation_stage == "fade out":
            # update and display text
            self.text = self.font.render(self.current_text, True, (self.text_animation_progression, 255, 255), (255, 255, 255))
            self.text_rect = self.text.get_rect()
            self.text_rect.center = self.text_rect_center
            self.surface.blit(self.text, self.text_rect)

            if self.text_animation_progression == 255:
                if self.current_text == "Have fun":
                    self.text_animation_stage = "last pause"
                else:
                    self.text_animation_stage = "second pause"
                # Becomes 0 because after this comes the pause and the text needs to be "invisible" (needs to be (255, 255, 255) - background's color)
                self.text_animation_progression = 0
            else:
                self.text_animation_progression += (255 // self.fps + 1)
                if self.text_animation_progression > 255:
                    self.text_animation_progression = 255