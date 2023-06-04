import pygame

from settings_view import settings_view
from game_view import game_view


class main_view:
    def __init__(self, controller=None):
        self.controller = controller
        self.settings = settings_view(800, 800, self.controller, self)
        self.game = None
        self.is_game_running = False

    def run(self, setting, game_num, speed):  # , prisoner_num):
        self.is_game_running = True
        self.simulation_ended = False
        self.is_results_showing = False
        CHOSEN_SIMULATION_GAME = self.controller.get_game_details(game_num)
        CHOSEN_SIMULATION_PRISONERS_NUM = len(CHOSEN_SIMULATION_GAME.prisoners)
        CHOSEN_SIMULATION_PRISONER = CHOSEN_SIMULATION_GAME.prisoners[0]
        locations_generator = self.controller.get_next_location(CHOSEN_SIMULATION_PRISONER)

        self.settings = setting
        self.game = game_view(number_of_boxes=len(CHOSEN_SIMULATION_GAME.prisoners), speed=self.get_game_speed(speed),
                              game_info=(game_num, self.controller.get_num_of_games()))

        # Run until the user asks to quit
        count = 0
        location = next(locations_generator)
        while self.is_game_running:
            # Fill the background with white
            if self.game.draw_game(location, CHOSEN_SIMULATION_PRISONER.checkBoxesList, count,
                                   CHOSEN_SIMULATION_PRISONER.isSuccess, count + 1 != CHOSEN_SIMULATION_PRISONERS_NUM) and self.simulation_ended is False:
                location = self.get_location_from_generator(locations_generator)
                if location is None:
                    self.simulation_ended = True

            if self.simulation_ended:
                # Done! Time to quit.
                pygame.event.post(self.game.custom_event)
                self.game.display_results(CHOSEN_SIMULATION_PRISONER)
                count += 1
                if count == CHOSEN_SIMULATION_PRISONERS_NUM:
                    break
                CHOSEN_SIMULATION_PRISONER = CHOSEN_SIMULATION_GAME.prisoners[count]
                locations_generator = self.controller.get_next_location(CHOSEN_SIMULATION_PRISONER)
                location = next(locations_generator)
                self.simulation_ended = False

            # Did the user click the window close button?
            for event in self.game.pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.quitEventHandler(event)
                self.continueSimulationEevent(event)  # Check for key press

            # Flip the display
            self.game.update_game()
            self.settings.update_settings()

        while True:
            for event in self.game.pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.game.pygame.quit()

    def quitEventHandler(self, event):
        if event.key == pygame.K_q:
            self.is_game_running = False
            pygame.quit()

    def continueSimulationEevent(self, event):
        if event.type == self.game.CUSTOM_EVENT_TYPE:
            flag = True
            while flag:
                for event in self.game.pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        flag = False

    def get_location_from_generator(self, iterable):
        try:
            first = next(iterable)
        except StopIteration:
            return None
        return first

    def get_game_speed(self, speed):
        if speed == "low":
            return 0.7
        elif speed == "med":
            return 5.0
        else:
            return 7.0
