import numpy
from sprites import *
import os


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
    - create_boxes_sprite_list(number_of_boxes, screen_width, screen_height): Creates a dictionary of Box objects
    - display_info(prisoner, boxes): Displays information about the game on the right side of the screen
    - display_results(): Displays the path taken by the prisoner and updates the screen for 20 seconds
    """

    TRANSPARENT = (0, 0, 0, 0)
    BACKGROUND_PATH = ASSETS_FOLDER + 'prison_floor.jpg'
    SUCCESS_SOUND_PATH = 'success.mp3'
    FAIL_SOUND_PATH = 'fail.mp3'

    def __init__(self, number_of_boxes=10, speed=0.7, game_info=tuple()):
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

        # Custom event type
        self.CUSTOM_EVENT_TYPE = pygame.USEREVENT + 1
        self.custom_event = pygame.event.Event(self.CUSTOM_EVENT_TYPE, message="waitBeforeContinue")

        # Set prisoner's screen start position
        self.PRISONERS_START_POS = [self.screen_width // 8, self.screen_height // 8]
        # Max number of displayed boxes on screen
        BOXES_MAX_NUMBER = 25

        # Screen background
        self.background = pygame.image.load(game_view.BACKGROUND_PATH)
        # Adjust background to screen size
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())

        # Initiate sprites and simulation flow
        self.number_of_boxes = min(number_of_boxes, BOXES_MAX_NUMBER)

        self.speed = speed
        self.boxes_target = [None]
        self.prisoner = Prisoner(self.PRISONERS_START_POS)
        self.boxes = self.create_boxes_sprite_list(self.number_of_boxes, self.screen_width, self.screen_height)
        self.lines_path = []
        self.firstBoxOpenFlag = True
        self.game_num = game_info[0] + 1
        self.game_total = game_info[1]
        self.won = 0

    def draw_game(self, expect=None, check=None, prisoner_num=None, isSuccess=None, isLast=None) -> bool:
        """
        Draw the game on the screen.

        :param expect: int, optional
            The expected value of the box to be opened.
        :param check:
        :param prisoner_num:
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

        if self.firstBoxOpenFlag:
            self.create_target_list(check, prisoner_num)
            self.firstBoxOpenFlag = False
            # Display prisoner's details on the right side
            if isSuccess:
                self.won += 1
            self.display_info(prisoner_num, self.number_of_boxes, isSuccess, isLast)


        if expect is not None:
            moveTo = self.boxes_target[0]
            self.move_prisoner(moveTo)
            if self.prisoner.rect.colliderect(self.boxes[moveTo].rect):
                self.lines_path.append(self.boxes[moveTo].pos)
                self.boxes_target.pop(0)
                self.animate_box(moveTo, expect)
                self.pygame.time.delay(1000)
                return True
            self.update_game()

        return False

    def display_results(self, prisoner):
        """
        Display the results of the game.
        """
        if len(self.lines_path) > 1:
            self.pygame.draw.lines(self.screen, (255, 0, 0), False, self.lines_path, 3)
        self.update_game()

        sound = game_view.SUCCESS_SOUND_PATH if prisoner.isSuccess else game_view.FAIL_SOUND_PATH
        try:
            file_path = self.find_file(sound, "./")
            pygame.mixer.Sound(file_path).play()
        except Exception:
            pass

        self.pygame.time.delay(1000)
        self.reset()
        self.screen.fill((160, 160, 160))
        self.screen.blit(self.background, (0, 0))

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

    def display_info(self, prisoner, boxes, isSuccess, isLast):
        """
        Display the game information on the screen.

        :param isSuccess: boolean, did prisoner succeeded or failed
        :param prisoner: int, optional, default: 0
            The prisoner number for the game.
        :param boxes: int, optional, default: 0
            The number of boxes in the game.
        """
        font_size = 28
        label, position = [], (30, 40)
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render("", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=position)
        pygame.draw.rect(self.screen, (0, 0, 0), text_rect)
        self.screen.fill((0, 0, 0))  # Clear the screen
        self.screen.blit(text_surface, text_rect)  # Draw the text
        self.update_game()

        text = ["Game {} out of {}".format(self.game_num, self.game_total),
                "This is the simulation of Prisoner {}".format(prisoner + 1),
                "There are {} number of boxes".format(boxes),
                "The Prisoner has {} The Game".format("Won" if isSuccess else "Lost"),
                "Press any key to continue next prisoner" if isLast else "",
                "Press 'Q' to quit",
                "{} Prisoners Succeeded, {} Prisoners Failed".format(self.won, self.number_of_boxes - self.won) if not isLast else "",
                ("The Game Was Won" if self.number_of_boxes - self.won == 0 else "The Game Was Lost") if not isLast else ""]

        for line in text:
            label.append(font.render(str(line), True, (0, 0, 0)))
        merged = self.background.copy()
        for line in range(len(label)):
            merged.blit(label[line], (position[0], position[1] + (line * font_size) + (15 * line)))
        self.background = merged.copy()
        self.update_game()

    def reset(self):
        self.background = pygame.image.load(game_view.BACKGROUND_PATH)
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())
        self.boxes_target = [None]
        self.prisoner = Prisoner(self.PRISONERS_START_POS)
        self.boxes = self.create_boxes_sprite_list(self.number_of_boxes, self.screen_width, self.screen_height)
        self.lines_path = []
        self.screen.fill((0, 0, 0))
        self.firstBoxOpenFlag = True

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

    def create_target_list(self, checkBoxList, prisoner):
        """
        Create a target list for the boxes to be opened.

        :param prisoner:
        :param checkBoxList: int
            The number of boxes in the game.
        :return: list of int
            A list of box indices to be opened.
        """
        self.boxes_target = [prisoner]
        self.boxes_target.extend(checkBoxList)

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
                boxes_dict[BOXES_PER_ROW * r + c] = Box(new_pos, BOXES_PER_ROW * r + c)
        return boxes_dict

    def find_file(self, filename, search_path):
        for root, dirs, files in os.walk(search_path):
            if filename in files:
                return os.path.join(root, filename)
        return None
