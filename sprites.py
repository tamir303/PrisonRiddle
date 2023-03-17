import pygame

ASSETS_FOLDER = 'assets/'


class Prisoner(pygame.sprite.Sprite):

    IMG = 'prisoner.png'

    def __init__(self, pos):
        super(Prisoner, self).__init__()
        self.image = pygame.image.load(
            ASSETS_FOLDER + Prisoner.IMG).convert_alpha()
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

    def __init__(self, pos):
        super(Box, self).__init__()
        self.image = pygame.image.load(
            ASSETS_FOLDER + Box.IMG_CLOSED).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (80, 80))
        self.paper = Paper(pos)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

    def open_box(self, number=None):
        self.image = pygame.image.load(ASSETS_FOLDER + Box.IMG_OPEN).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (85, 85))
        merged = self.image.copy()
        self.paper.display_expected_number(number)
        merged.blit(self.paper.image, (10, 0))
        self.image = merged.copy()

    def close_box(self):
        self.image = pygame.image.load(
            ASSETS_FOLDER + Box.IMG_CLOSED).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (80, 80))


class Paper(pygame.sprite.Sprite):

    IMG_PAPER = 'paper.png'

    def __init__(self, pos=(0, 0)):
        super(Paper, self).__init__()
        self.image = pygame.image.load(
            ASSETS_FOLDER + Paper.IMG_PAPER).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (65, 50))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

    def display_expected_number(self, number=None):
        number_font = pygame.font.SysFont(None, 28)
        number_image = number_font.render(number, True, (0, 0, 0))
        merged = self.image.copy()
        merged.blit(number_image, (20, 15))
        self.image = merged.copy()
