import pygame

class game_view:
    def __init__(self, x_size, y_size, controller):
        self.pygame = pygame
        self.pygame.init()  # initialize all
        self.running = True  # set program to run
        self.screen = pygame.display.set_mode([x_size, y_size])  # display screen
        self.active_tb = None
        self.background = pygame.image.load("prison_floor.jpg")
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())

    def get_game_screen(self):
        return self.screen

    def update_game(self):
        self.pygame.display.flip()
