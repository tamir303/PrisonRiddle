import game_view
from settings_view import settings_view

class main_view:
    def __init__(self, controller=None):
        self.controller = controller
        self.settings = settings_view(300, 350, self.controller, self)

    def run(self, setting):
        self.settings= setting
        # Run until the user asks to quit
        self.game = game_view.game_view()
        game_screen = self.game.get_game_screen()
        while self.game.running:

            # Did the user click the window close button?
            for event in self.game.pygame.event.get():
                self.eventHandler(event)

            # Fill the background with white
            self.game.draw_game(3)

            # Flip the display
            self.game.update_game()
            self.settings.update_settings()

        # Done! Time to quit.
        game_screen.quit()

    def eventHandler(self, event):
        if event.type == self.game.pygame.QUIT:
            self.game.running = False
