import pygame

ASSETS_FOLDER = 'assets/'


class Prisoner(pygame.sprite.Sprite):
    """
    Represents a prisoner in the game.

    :param pos: The position of the prisoner.
    :type pos: tuple
    :ivar image: The image of the prisoner.
    :vartype image: pygame.Surface
    :ivar paper: The paper object inside the prisoner.
    :vartype paper: Paper
    :ivar rect: The rectangle of the prisoner.
    :vartype rect: pygame.Rect
    :ivar pos: The position of the prisoner.
    :vartype pos: tuple
    """

    IMG = 'prisoner.png'

    def __init__(self, pos):
        """
        Initialize a new Prisoner object.

        :param pos: The initial position of the prisoner.
        :type pos: tuple
        :return: None
        :rtype: None
        """
        super(Prisoner, self).__init__()
        self.image = pygame.image.load(
            ASSETS_FOLDER + Prisoner.IMG).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.image = pygame.transform.flip(self.image, 90, 0)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

    def update_location(self, pos):
        """
        Update the position of the prisoner.

        :param pos: The new position of the prisoner.
        :type pos: tuple
        :return: None
        :rtype: None
        """
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)


class Box(pygame.sprite.Sprite):
    """
    Represents a box in the game.

    :param pos: The position of the box.
    :type pos: tuple
    :ivar image: The image of the box.
    :vartype image: pygame.Surface
    :ivar paper: The paper object inside the box.
    :vartype paper: Paper
    :ivar rect: The rectangle of the box.
    :vartype rect: pygame.Rect
    :ivar pos: The position of the box.
    :vartype pos: tuple
    """

    IMG_OPEN = 'box_open.png'
    IMG_CLOSED = 'box_closed.png'

    def __init__(self, pos, num):
        super(Box, self).__init__()
        self.image = pygame.image.load(
            ASSETS_FOLDER + Box.IMG_CLOSED).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (80, 80))
        self.num = num
        self.paper = Paper(pos)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.close_box()

    def open_box(self, number=None):
        """
        Opens the box and displays an expected number on the paper inside the box.

        :param number: The expected number to be displayed on the paper inside the box. Defaults to None.
        :type number: int or None
        :return: None
        :rtype: None
        """
        self.image = pygame.image.load(ASSETS_FOLDER + Box.IMG_OPEN).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (85, 85))
        merged = self.image.copy()
        self.paper.display_expected_number(number)
        merged.blit(self.paper.image, (10, 0))
        self.image = merged.copy()

    def close_box(self):
        """
         Closes the box.

        :return: None
        :rtype: None
        """
        self.image = pygame.image.load(
            ASSETS_FOLDER + Box.IMG_CLOSED).convert_alpha()
        number_font = pygame.font.SysFont(None, 84)
        number_image = number_font.render(str(int(self.num) + 1), True, (255, 255, 0))
        merged = self.image.copy()
        merged.blit(number_image, (20, 15))
        self.image = merged.copy()
        self.image = pygame.transform.smoothscale(self.image, (80, 80))


class Paper(pygame.sprite.Sprite):
    """
    Represents a paper in the game.

    :param pos: The position of the paper.
    :type pos: tuple
    :ivar image: The image of the paper.
    :vartype image: pygame.Surface
    :ivar paper: The paper object inside the paper.
    :vartype paper: Paper
    :ivar rect: The rectangle of the paper.
    :vartype rect: pygame.Rect
    :ivar pos: The position of the paper.
    :vartype pos: tuple
    """

    IMG_PAPER = 'paper.png'

    def __init__(self, pos=(0, 0)):
        """
        Initializes a Paper object.

        :param pos: The position of the paper. Default is (0, 0).
        :type pos: tuple
        """
        super(Paper, self).__init__()
        self.image = pygame.image.load(
            ASSETS_FOLDER + Paper.IMG_PAPER).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (65, 50))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

    def display_expected_number(self, number=None):
        """
        Displays the expected number on the paper.

        :param number: The number to display on the paper.
        :type number: str
        """
        number_font = pygame.font.SysFont(None, 28)
        number_image = number_font.render(str(int(number) + 1), True, (0, 0, 0))
        merged = self.image.copy()
        merged.blit(number_image, (20, 15))
        self.image = merged.copy()
