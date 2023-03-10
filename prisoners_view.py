import settings_view
import game_view


class main_view:
    def __init__(self, x_size=800, y_size=800, controller=None):
        self.x_size = x_size  # resolution X
        self.y_size = y_size  # resolution Y
        self.controller = controller
        self.settings = settings_view.settings_view(300, 350, self.controller, self)
        ##self.run()
        settings_screen = self.settings.get_settings_screen()

    def run(self):
        # Run until the user asks to quit
        self.game = game_view.game_view(self.x_size, self.y_size)
        game_screen = self.game.get_game_screen()
        while self.game.running:

            # Did the user click the window close button?
            for event in self.game.pygame.event.get():
                self.eventHandler(event)

            # Fill the background with white
            game_screen.fill((160, 160, 160))
            game_screen.blit(self.game.background, (0, 0))

            # Flip the display
            self.game.update_game()
            self.settings.update_settings()

        # Done! Time to quit.
        game_screen.quit()

    def eventHandler(self, event):
        if event.type == self.game.pygame.QUIT:
            self.game.running = False
