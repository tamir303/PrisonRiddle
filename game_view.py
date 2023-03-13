import numpy
from sprites import *


class game_view:

    TRANSPARENT = (0, 0, 0, 0)

    def __init__(self, number_of_boxes=10, speed=0.4):
        self.pygame = pygame
        self.pygame.init()  # initialize all
        self.running = True
        info = pygame.display.Info()
        screen_width = int(info.current_w * 0.6)
        screen_height = int(info.current_h * 0.6)
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height))  # display screen

        PRISONERS_START_POS = [screen_width // 8, screen_height // 8]
        BOXES_MAX_NUMBER = 25

        self.active_tb = None
        self.background = pygame.image.load(ASSETS_FOLDER + "prison_floor.jpg")
        self.background = pygame.transform.smoothscale(
            self.background, self.screen.get_size())

        number_of_boxes = min(number_of_boxes, BOXES_MAX_NUMBER)
        self.boxes_target = self.create_target_list(number_of_boxes)
        self.speed = speed
        self.prisoner = Prisoner(PRISONERS_START_POS)
        self.boxes = self.create_boxes_sprite_list(
            number_of_boxes, screen_width, screen_height)
        self.paper = Paper()

    def get_game_screen(self):
        return self.screen

    def update_game(self):
        self.pygame.display.flip()

    def draw_game(self, expect=None) -> bool:
        self.screen.fill((160, 160, 160))
        self.screen.blit(self.background, (0, 0))
        for box in self.boxes.values():
            self.screen.blit(box.image, box.rect)
        self.screen.blit(self.prisoner.image, self.prisoner.rect)
        if expect is not None:
            moveTo = self.boxes_target[0]
            self.move_prisoner(moveTo)
            if self.prisoner.rect.colliderect(self.boxes[moveTo].rect):
                print("Open Box {}".format(moveTo))
                self.boxes_target.pop(0)
                self.animate_box(moveTo, expect)
                return True
            self.update_game()
        return False

    def move_prisoner(self, moveTo):
        p_corr = self.prisoner.pos
        b_corr = self.boxes[moveTo].pos
        vect = tuple(map(lambda element: numpy.sign(element[1] - element[0]) *
                     self.speed + element[0], zip(p_corr, b_corr)))
        self.prisoner.update_location(vect)

    def animate_box(self, moveTo, expect):
        curr_box = self.boxes[moveTo]
        curr_box.image.fill(game_view.TRANSPARENT)
        self.screen.blit(curr_box.image, curr_box.rect)
        curr_box.open_box()
        self.screen.blit(curr_box.image, curr_box.rect)
        self.screen.blit(self.paper.image, self.paper.rect)
        pygame.time.delay(500)

    def close_all_boxes(self):
        for box in self.boxes.values():
            box.close_box()

    def create_target_list(self, number_of_boxes):
        target = list(range(0, number_of_boxes))
        numpy.random.shuffle(target)
        return target

    def create_boxes_sprite_list(self, number_of_boxes, screen_width, screen_height):
        boxes_dict = dict()
        BOX_START_POS = [screen_width // 2, screen_height // 8]
        BOXES_PER_ROW = 5
        BOXES_SHIFT = screen_width / 9
        LAST_ROW = number_of_boxes // BOXES_PER_ROW

        for r in range(max(1, int(numpy.ceil(number_of_boxes / BOXES_PER_ROW)))):
            for c in range(min(number_of_boxes, BOXES_PER_ROW) if r + 1 != LAST_ROW else number_of_boxes % BOXES_PER_ROW):
                new_pos = (BOX_START_POS[0] + c*BOXES_SHIFT,
                           BOX_START_POS[1] + r*BOXES_SHIFT)
                boxes_dict[BOXES_PER_ROW * r + c] = Box(new_pos)
        return boxes_dict
