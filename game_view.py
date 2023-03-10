import numpy
from sprites import *

class game_view:

    def __init__(self, number_of_boxes=10, speed=0.4):
        self.pygame = pygame
        self.pygame.init()  # initialize all
        self.running = True

        info = pygame.display.Info()
        screen_width = int(info.current_w * 0.6)
        screen_height = int(info.current_h * 0.6)
        self.screen = pygame.display.set_mode((screen_width, screen_height))  # display screen

        PRISONERS_START_POS = [screen_width // 8, screen_height // 8]
        BOX_START_POS = [screen_width // 2, screen_height // 3]
        BOXES_PER_ROW = 5
        BOXES_SHIFT = screen_width / 9
        BOXES_MAX_NUMBER = 50

        self.active_tb = None
        self.background = pygame.image.load("prison_floor.jpg")
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())

        self.speed = speed
        self.prisoner = Prisoner(PRISONERS_START_POS)
        self.boxes = dict()
        self.paper = Paper()
        for r in range(number_of_boxes // BOXES_PER_ROW):
            for c in range(BOXES_PER_ROW):
                new_pos = (BOX_START_POS[0] + c*BOXES_SHIFT, BOX_START_POS[1] - r*BOXES_SHIFT)
                self.boxes[BOXES_PER_ROW * r + c] = Box(new_pos, r + c)

    def get_game_screen(self):
        return self.screen

    def update_game(self):
        self.pygame.display.flip()

    def draw_game(self, moveTo=None) -> bool:
        self.screen.fill((160, 160, 160))
        self.screen.blit(self.background, (0, 0))
        for box in self.boxes.values():
            self.screen.blit(box.image, box.rect)
        self.screen.blit(self.prisoner.image, self.prisoner.rect)
        if moveTo is not None:
            self.move_prisoner(moveTo)
            if self.prisoner.rect.colliderect(self.boxes[moveTo].rect):
                print("Open Box {}".format(moveTo))
                self.animate_box(self.boxes[moveTo].number)
                return True
            self.update_game()
        return False

    def move_prisoner(self, moveTo):
        Px, Py = self.prisoner.pos
        Bx, By = self.boxes[moveTo].pos
        dx = numpy.sign(Bx - Px) * self.speed + Px
        dy = numpy.sign(By - Py) * self.speed + Py
        self.prisoner.update_location((dx, dy))

    def animate_box(self, number):
        curr_box = self.boxes[number]
        curr_box.open_box()
        self.paper.update(curr_box.pos)
        self.screen.blit(curr_box.image, curr_box.rect)
        self.screen.blit(self.paper.image, self.paper.rect)
        self.update_game()
        pygame.time.delay(500)
        curr_box.close_box()



