import pygame
import prisoners_view

class game_view:
    def __init__(self, x_size, y_size, main_dialog):
        pygame.init()  # initialize all
        self.running = True  # set program to run
        self.screen = pygame.display.set_mode([x_size, y_size])  # display screen
        self.active_tb = None
        self.background = pygame.image.load("prison_floor.jpg")
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())
        self.main_dialog = main_dialog
        self.run()

    def run(self):
        # Run until the user asks to quit
        self.running = True
        self.main_dialog.pack()
        while self.running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                self.eventHandler(event)

            # Fill the background with white
            self.screen.fill((160, 160, 160))
            self.screen.blit(self.background, (0, 0))

            # Flip the display
            pygame.display.flip()
            self.main_dialog.update()

        # Done! Time to quit.
        pygame.quit()

    def eventHandler(self, event):
        if event.type == pygame.QUIT:
            self.running = False
