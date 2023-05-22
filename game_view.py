import numpy
from sprites import *


class game_view:
    """
    This class represents the view of the game and contains methods for drawing and updating the game screen.

    Attributes:
    - number_of_boxes (int): The number of boxes to be displayed in the game (default 10)
    - speed (float): The speed at which the prisoner moves towards a box (default 0.7)
    - prisoner (int): The number assigned to the prisoner in the simulation (default 0)

    Methods:
    - get_game_screen(): Returns the game screen object
    - update_game(): Updates the game screen
    - draw_game(expect=None) -> bool: Draws the game screen and moves the prisoner towards the next box.
        If expect is provided, opens the box with the expected number and returns True if successful, False otherwise.
    - move_prisoner(moveTo): Moves the prisoner towards the specified box
    - animate_box(moveTo, expect): Animates the opening of the specified box with the provided number
    - close_all_boxes(): Closes all boxes in the game
    - create_target_list(number_of_boxes): Creates a list of random indices for opening the boxes
    - create_boxes_sprite_list(number_of_boxes, screen_width, screen_height): Creates a dictionary of Box objects
    - display_info(prisoner, boxes): Displays information about the game on the right side of the screen
    - display_results(): Displays the path taken by the prisoner and updates the screen for 20 seconds
    """

    TRANSPARENT = (0, 0, 0, 0)
    BACKGROUND_PATH = ASSETS_FOLDER + 'prison_floor.jpg'

    def __init__(self, number_of_boxes=10, speed=0.7):
        """
        Initialize the GameView object.

        :param number_of_boxes: int, optional, default: 10
            The number of boxes in the game.
        :param speed: float, optional, default: 0.7
            The speed at which the prisoner moves.
        :param prisoner: int, optional, default: 0
            The prisoner number for the game.
        """
        # initialize all
        self.pygame = pygame
        self.pygame.init()
        # Start game run condition
        self.running = True
        # Fetch user's screen information
        info = pygame.display.Info()
        # Set screen width
        self.screen_width = int(info.current_w * 0.6)
        # Set screen height
        self.screen_height = int(info.current_h * 0.6)
        # Display screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Set prisoner's screen start position
        self.PRISONERS_START_POS = [self.screen_width // 8, self.screen_height // 8]
        # Max number of displayed boxes on screen
        BOXES_MAX_NUMBER = 25

        # Screen background
        self.background = pygame.image.load(game_view.BACKGROUND_PATH)
        # Adjust background to screen size
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())

        # Display prisoner's details on the right side
        self.display_info(boxes=number_of_boxes)

        # Initiate sprites and simulation flow
        self.number_of_boxes = min(number_of_boxes, BOXES_MAX_NUMBER)
        self.speed = speed
        self.boxes_target = self.create_target_list(number_of_boxes)
        self.prisoner = Prisoner(self.PRISONERS_START_POS)
        self.boxes = self.create_boxes_sprite_list(number_of_boxes, self.screen_width, self.screen_height)
        self.lines_path = []

    def get_game_screen(self):
        """
        Get the game screen.

        :return: pygame.Surface
            The game screen surface.
        """
        return self.screen

    def update_game(self):
        """
        Update the game screen.
        """
        self.pygame.display.flip()

    def draw_game(self, expect=None) -> bool:
        """
        Draw the game on the screen.

        :param expect: int, optional
            The expected value of the box to be opened.
        :return: bool
            True if the game is over, False otherwise.
        """
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
        """
        Move the prisoner to the given box.

        :param moveTo: int
            The box to move the prisoner to.
        """
        p_corr = self.prisoner.pos
        b_corr = self.boxes[moveTo].pos
        vector = tuple(map(lambda element: numpy.sign(element[1] - element[0]) *
                                           self.speed + element[0], zip(p_corr, b_corr)))
        self.prisoner.update_location(vector)

    def animate_box(self, moveTo, expect):
        """
        Animate the opening of the given box.

        :param moveTo: int
            The box to open.
        :param expect: int
            The expected value of the box to be opened.
        """
        curr_box = self.boxes[moveTo]
        curr_box.image.fill(game_view.TRANSPARENT)
        self.screen.blit(curr_box.image, curr_box.rect)
        curr_box.open_box(str(expect))
        self.screen.blit(curr_box.image, curr_box.rect)

    def close_all_boxes(self):
        """
        Close all boxes.
        """
        for box in self.boxes.values():
            box.close_box()

    def create_target_list(self, number_of_boxes):
        """
        Create a target list for the boxes to be opened.

        :param number_of_boxes: int
            The number of boxes in the game.
        :return: list of int
            A list of box indices to be opened.
        """
        target = list(range(0, number_of_boxes - 1))
        numpy.random.shuffle(target)
        return target

    def create_boxes_sprite_list(self, number_of_boxes, screen_width, screen_height):
        """
        Create a dictionary of box sprites.

        :param number_of_boxes: int
            The number of boxes in the game.
        :param screen_width: int
            The width of the game screen.
        :param screen_height: int
            The height of the game screen.
        :return: dict of Box
            A dictionary of Box objects representing the boxes in the game.
        """
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
        """
        Display the game information on the screen.

        :param prisoner: int, optional, default: 0
            The prisoner number for the game.
        :param boxes: int, optional, default: 0
            The number of boxes in the game.
        """
        text = ["This is the simulation of Prisoner {}".format(prisoner + 1), "There are {} number of boxes".format(boxes),
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

    def display_results(self, prisoner):
        """
        Display the results of the game.
        """
        if len(self.lines_path) > 1:
            self.pygame.draw.lines(self.screen, (255, 0, 0), False, self.lines_path, 3)
        self.update_game()
        self.pygame.time.delay(2000)
        self.reset(prisoner)
        self.screen.fill((160, 160, 160))
        self.screen.blit(self.background, (0, 0))
        self.display_info(prisoner=prisoner, boxes=self.number_of_boxes)

    def reset(self, prisoner):
        self.background = pygame.image.load(game_view.BACKGROUND_PATH)
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())
        self.boxes_target = self.create_target_list(self.number_of_boxes)
        self.prisoner = Prisoner(self.PRISONERS_START_POS)
        self.boxes = self.create_boxes_sprite_list(self.number_of_boxes, self.screen_width, self.screen_height)
        self.lines_path = []
        self.screen.fill((0, 0, 0))
