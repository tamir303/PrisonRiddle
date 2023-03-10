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

class game_view:

    def __init__(self, x_size, y_size, number_of_boxes=10):

        PRISONERS_START_POS = (x_size // 8, y_size // 8)
        BOX_START_POS = [x_size // 2, y_size // 3]
        BOXES_PER_ROW = 5
        BOXES_SHIFT = x_size / 9
        BOXES_MAX_NUMBER = 50

        self.pygame = pygame
        self.pygame.init()  # initialize all
        self.running = True

        self.screen = pygame.display.set_mode([x_size, y_size])  # display screen
        self.active_tb = None
        self.background = pygame.image.load("prison_floor.jpg")
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())

        self.prisoner = Prisoner(PRISONERS_START_POS)
        self.boxes = dict()
        for r in range(number_of_boxes // BOXES_PER_ROW):
            for c in range(BOXES_PER_ROW):
                new_pos = (BOX_START_POS[0] + c*BOXES_SHIFT, BOX_START_POS[1] - r*BOXES_SHIFT)
                self.boxes[BOXES_PER_ROW * r + c] = Box(new_pos, r + c)

    def get_game_screen(self):
        return self.screen

    def update_game(self):
        self.pygame.display.flip()

    def draw_game(self, moveTo=None):
        self.screen.fill((160, 160, 160))
        self.screen.blit(self.background, (0, 0))
        for box in self.boxes.values():
            self.screen.blit(box.image, box.rect)
        self.screen.blit(self.prisoner.image, self.prisoner.rect)
        if moveTo is not None:
            self.movePrisoner(moveTo)

    def movePrisoner(self, moveTo):
        pass

