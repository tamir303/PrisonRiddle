from settings_view import settings_view
from game_view import game_view


class main_view:
    def __init__(self, controller=None):
        self.controller = controller
        self.settings = settings_view(300, 350, self.controller, self)
        self.game = None

    def run(self, setting):
        CHOSEN_SIMULATION_PRISONER = self.controller.get_prisoner_details(
            0, 0)                 # PRISONER 0 GAME 0
        locations_generator = self.controller.get_next_location(
            CHOSEN_SIMULATION_PRISONER)
        self.settings = setting
        self.game = game_view(number_of_boxes=len(
            CHOSEN_SIMULATION_PRISONER.checkBoxesList))
        # Run until the user asks to quit
        game_screen = self.game.get_game_screen()

        location = next(locations_generator)
        while self.game.running:

            # Did the user click the window close button?
            for event in self.game.pygame.event.get():
                self.eventHandler(event)

            # Fill the background with white
            if self.game.draw_game(location):
                nextlocation = next(locations_generator)
                if nextlocation is not None:
                    location = nextlocation

            # Flip the display
            self.game.update_game()
            self.settings.update_settings()

        # Done! Time to quit.
        game_screen.quit()

    def eventHandler(self, event):
        if event.type == self.game.pygame.QUIT:
            self.game.running = False
