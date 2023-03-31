import prisoners_game_model
import prisoners_view
import re

class Controller(object):

    def __init__(self):
        self.model = prisoners_game_model.prisoners_model(100, 1)
        self.view = prisoners_view.main_view(self)

    def change_model_prisoners(self, prisoners_num):
        # prisoners_Assert(prisoners_num)
        self.model.change_prisoners_number(int(prisoners_num))

    def change_model_games(self, games_num):
        # games_Assert(games_num)
        self.model.change_games_number(int(games_num))

    def start_game(self, optimized):
        self.model.play(bool(optimized))

    def get_game_details(self, game):
        return self.model.games[game]

    def input_check(self, game_input, prisoner_number_input):
        # Define the regex pattern for checking if input is a number
        number_pattern = r'^-?\d+(?:\.\d+)?$'

        # Check if both inputs are numbers
        if not bool(re.match(number_pattern, str(game_input))) or not bool(re.match(number_pattern, str(prisoner_number_input))):
            return False
        
        # Convert the inputs to integers
        game_input = int(game_input) - 1
        prisoner_input = int(prisoner_number_input)

        # Check if game_input is within valid range
        if game_input < 0 or game_input >= len(self.model.games.keys()):
            return False

        # Check if prisoner_number_input is within valid range for the given game
        game = self.get_game_details(game_input)
        if prisoner_input < 1 or prisoner_input > len(game.prisoners.keys()):
            return False

        # If both inputs are valid numbers and within range, return True
        return game_input,prisoner_input   

    def get_prisoner_details(self,game,prisoner):
        return self.model.games[game].prisoners[prisoner]
    
    def get_model_to_string(self):
        return self.model.read_game()

    def get_next_location(self, prisoner):
        queue = []
        for element in prisoner.checkBoxesList:
            queue.append(element)
        yield queue.pop(0)
        while True:
            if len(queue) > 0:
                yield queue.pop(0)
            else:
                break
        return None
