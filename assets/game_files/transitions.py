import pygame
from math import ceil

class Section_Transition(object):
    def __init__(self, surface, screen_size, color, FPS, fade_duration):
        self.surface = surface
        self.screen_size = screen_size
        self.color = color
        self.fps = FPS
        self.fade_duration = fade_duration
        self.running = False

        # at fade in - from 0 to 255 (increase opacity)
        # at fade out - from 255 to 0 (decrease opacity)
        self.transition_progression = 0

        # increase/decrease opacity velocity
        self.opacity_velocity = 255 / (FPS * self.fade_duration)

        # for fade in stage
        self.fade_in_flag = True

        self.pause = True

        self.pause_duration = 2 * self.fps * self.fade_duration

    def run(self):
        # The section transition effect has 3 stages:
            # fade in - a rect over the screen which's opacity will get from 0(0%) to 255(100%)
            # pause - a pause with the rect over the window
            # fade out - rect lose opacity(from 255 to 0)

        # True at the beginning for fade in stage
        if self.fade_in_flag:
            # increase opacity until it gets 255(100%) to cover the window
            self.transition_progression += self.opacity_velocity
            if self.transition_progression >= 255: # that's because of division, in case of 255.00...001
                # when the opacity gets 100% the fade in flag become false, to start pause stage
                self.transition_progression = 255
                self.fade_in_flag = False
        else:
            # fade in ended, now pause stage begins
            if self.pause:
                # if pause duration ends change self.pause to False and start fading out
                if self.pause_duration == 0:
                    self.pause = False
                    self.pause_duration = 2 * self.fps * self.fade_duration
                else:
                    # if pause duration doesn't end yet, keep decreasing pause duration
                    self.pause_duration -= 1
            else:
                # pause ended, time for fading out now
                # decrease opacity until 0
                self.transition_progression -= self.opacity_velocity
                if self.transition_progression <= 0: # in case of 0.000...001
                    # reset to 0 for the next transition fade in
                    self.transition_progression = 0
                    # become True for next fade in
                    self.fade_in_flag = True
                    # stop the transition
                    self.running = False
                    # reset the pause
                    self.pause = True

        # DRAW THE RECT ON THE SCREEN

        # create the surface object with the screen size
        rect = pygame.Surface(self.screen_size)
        # set alpha
        rect.set_alpha(ceil(self.transition_progression))
        # fill the surface with the color
        rect.fill(self.color)
        # display the surface
        self.surface.blit(rect, (0, 0))