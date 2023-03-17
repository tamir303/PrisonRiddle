from settings_view import settings_view
from game_view import game_view


class main_view:
    def __init__(self, controller=None):
        self.controller = controller
        self.settings = settings_view(300, 350, self.controller, self)
        self.game = None
        self.is_game_running = False

    def run(self, setting):
        self.is_game_running = True
        CHOSEN_SIMULATION_GAME = self.controller.get_game_details(0)
        CHOSEN_SIMULATION_PRISONER = self.controller.get_prisoner_details(0, 0)

        locations_generator = self.controller.get_next_location(
            CHOSEN_SIMULATION_PRISONER)

        self.settings = setting
        self.game = game_view(number_of_boxes=len(CHOSEN_SIMULATION_GAME.prisoners))

        # Run until the user asks to quit
        game_screen = self.game.get_game_screen()
        location = next(locations_generator)
        while self.is_game_running:

            # Did the user click the window close button?
            for event in self.game.pygame.event.get():
                self.eventHandler(event)

            # Fill the background with white
            if self.game.draw_game(location):
                location = self.get_location_from_generator(
                    locations_generator)
                if location is None:
                    self.InitilizeEndSequancea()

            # Flip the display
            self.game.update_game()
            self.settings.update_settings()

        # Done! Time to quit.
        self.game.display_results()

    def eventHandler(self, event):
        if event.type == self.game.pygame.QUIT:
            self.game.running = False

    def get_location_from_generator(self, iterable):
        try:
            first = next(iterable)
        except StopIteration:
            return None
        return first

    def InitilizeEndSequancea(self):
        self.is_game_running = False
