import numpy
from sprites import *


class game_view:
    TRANSPARENT = (0, 0, 0, 0)
    BACKGROUND_PATH = ASSETS_FOLDER + 'prison_floor.jpg'

    def __init__(self, number_of_boxes=10, speed=0.7, prisoner=0):
        # initialize all
        self.pygame = pygame
        self.pygame.init()
        # Start game run condition
        self.running = True
        # Fetch user's screen information
        info = pygame.display.Info()
        # Set screen width
        screen_width = int(info.current_w * 0.6)
        # Set screen height
        screen_height = int(info.current_h * 0.6)
        # Display screen
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        # Set prisoner's screen start position
        PRISONERS_START_POS = [screen_width // 8, screen_height // 8]
        # Max number of displayed boxes on screen
        BOXES_MAX_NUMBER = 25

        # Screen background
        self.background = pygame.image.load(game_view.BACKGROUND_PATH)
        # Adjust background to screen size
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())

        # Display prisoner's details on the right side
        self.display_info(boxes=number_of_boxes)

        # Initiate sprites and simulation flow
        number_of_boxes = min(number_of_boxes, BOXES_MAX_NUMBER)
        self.speed = speed
        self.boxes_target = self.create_target_list(number_of_boxes)
        self.prisoner = Prisoner(PRISONERS_START_POS)
        self.boxes = self.create_boxes_sprite_list(number_of_boxes, screen_width, screen_height)
        self.lines_path = []

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
        if len(self.boxes) == 0 or len(self.boxes_target) == 0:
            return True
        if expect is not None:
            moveTo = self.boxes_target[0]
            self.move_prisoner(moveTo)
            if self.prisoner.rect.colliderect(self.boxes[moveTo].rect):
                print("Open Box {}".format(moveTo))
                self.lines_path.append(self.boxes[moveTo].pos)
                self.boxes_target.pop(0)
                self.animate_box(moveTo, expect)
                self.pygame.time.delay(1000)
                return True
            self.update_game()
        return False

    def move_prisoner(self, moveTo):
        p_corr = self.prisoner.pos
        b_corr = self.boxes[moveTo].pos
        vector = tuple(map(lambda element: numpy.sign(element[1] - element[0]) *
                                self.speed + element[0], zip(p_corr, b_corr)))
        self.prisoner.update_location(vector)

    def animate_box(self, moveTo, expect):
        curr_box = self.boxes[moveTo]
        curr_box.image.fill(game_view.TRANSPARENT)
        self.screen.blit(curr_box.image, curr_box.rect)
        curr_box.open_box(str(expect))
        self.screen.blit(curr_box.image, curr_box.rect)

    def close_all_boxes(self):
        for box in self.boxes.values():
            box.close_box()

    def create_target_list(self, number_of_boxes):
        target = list(range(0, number_of_boxes - 1))
        numpy.random.shuffle(target)
        return target

    def create_boxes_sprite_list(self, number_of_boxes, screen_width, screen_height):
        boxes_dict = dict()
        BOX_START_POS = [screen_width // 2, screen_height // 8]
        BOXES_PER_ROW = 5
        BOXES_SHIFT = screen_width / 9
        NUMBER_OF_ROWS = max(1, int(numpy.ceil(number_of_boxes / BOXES_PER_ROW)))

        for r in range(NUMBER_OF_ROWS):
            for c in range(
                    number_of_boxes % BOXES_PER_ROW if r + 1 == NUMBER_OF_ROWS and number_of_boxes % BOXES_PER_ROW != 0
                    else min(number_of_boxes, BOXES_PER_ROW)):
                new_pos = (BOX_START_POS[0] + c * BOXES_SHIFT,
                           BOX_START_POS[1] + r * BOXES_SHIFT)
                boxes_dict[BOXES_PER_ROW * r + c] = Box(new_pos)
        return boxes_dict

    def display_info(self, prisoner=0, boxes=0):
        text = ["This is the simulation of Prisoner {}".format(prisoner), "There are {} number of boxes".format(boxes),
                "Press any key to quit the simulation"]
        font_size = 28
        font = pygame.font.SysFont(None, font_size)
        label, position = [], (30, 40)
        for line in text:
            label.append(font.render(str(line), True, (0, 0, 0)))
        merged = self.background.copy()
        for line in range(len(label)):
            merged.blit(label[line], (position[0], position[1] + (line * font_size) + (15 * line)))
        self.background = merged.copy()

    def display_results(self):
        self.pygame.draw.lines(self.screen, (255, 0, 0), False, self.lines_path, 3)
        self.update_game()
        self.pygame.time.delay(20000)
