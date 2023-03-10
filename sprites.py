import pygame

class Prisoner(pygame.sprite.Sprite):

    IMG = 'prisoner.png'

    def __init__(self, pos):
        super(Prisoner, self).__init__()
        self.image = pygame.image.load('prisoner.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.image = pygame.transform.flip(self.image, 90, 0)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

    def update_location(self, pos):
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)

class Box(pygame.sprite.Sprite):

    IMG_OPEN = 'box_open.png'
    IMG_CLOSED = 'box_closed.png'

    def __init__(self, pos, number):
        super(Box, self).__init__()
        self.image = pygame.image.load(Box.IMG_CLOSED).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (80, 80))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.number = number

    def open_box(self):
        self.image = pygame.image.load(Box.IMG_OPEN).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (85, 85))

    def close_box(self):
        self.image = pygame.image.load(Box.IMG_CLOSED).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (80, 80))

class Paper(pygame.sprite.Sprite):

    IMG_PAPER = 'paper.png'

    def __init__(self, pos=(0, 0)):
        super(Paper, self).__init__()
        self.image = pygame.image.load(Box.IMG_CLOSED).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

    def update_location(self, pos):
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)