import pygame

from settings_view import settings_view
from game_view import game_view

class main_view:
    def __init__(self, controller=None):
        self.controller = controller
        self.settings = settings_view(800, 700, self.controller, self)
        self.game = None
        self.is_game_running = False

    def run(self, setting, game_num): #, prisoner_num):
        self.is_game_running = True
        self.simulation_ended = False
        self.is_results_showing = False
        CHOSEN_SIMULATION_GAME = self.controller.get_game_details(game_num)
        CHOSEN_SIMULATION_PRISONERS_NUM = len(CHOSEN_SIMULATION_GAME.prisoners)
        CHOSEN_SIMULATION_PRISONER = CHOSEN_SIMULATION_GAME.prisoners[0]
        locations_generator = self.controller.get_next_location(CHOSEN_SIMULATION_PRISONER)

        self.settings = setting
        self.game = game_view(number_of_boxes=len(CHOSEN_SIMULATION_GAME.prisoners))

        # Run until the user asks to quit
        count = 0
        location = next(locations_generator)
        while self.is_game_running:
            # Fill the background with white
            if self.game.draw_game(location) and self.simulation_ended is False:
                location = self.get_location_from_generator(locations_generator)
                if location is None:
                    self.simulation_ended = True

            if self.simulation_ended:
                # Done! Time to quit.
                self.game.display_results(count, CHOSEN_SIMULATION_PRISONER.isSuccess)
                count += 1
                if count == CHOSEN_SIMULATION_PRISONERS_NUM:
                    break
                CHOSEN_SIMULATION_PRISONER = CHOSEN_SIMULATION_GAME.prisoners[count]
                locations_generator = self.controller.get_next_location(CHOSEN_SIMULATION_PRISONER)
                location = next(locations_generator)
                self.simulation_ended = False


            # Flip the display
            self.game.update_game()
            self.settings.update_settings()

            # Did the user click the window close button?
            for event in self.game.pygame.event.get():
                self.quitEventHandler(event, self.game.pygame, self.simulation_ended)


    def quitEventHandler(self, event,self_pygame,simulation_ended):
        if event.type == pygame.QUIT:
            self_pygame.quit()
            self.is_game_running = False    
        if event.type == pygame.KEYDOWN and simulation_ended:
            self_pygame.quit()
            self.is_game_running = False    
            
    def get_location_from_generator(self, iterable):
        try:
            first = next(iterable)
        except StopIteration:
            return None
        return first
