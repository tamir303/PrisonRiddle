import prisoners_game_model
import prisoners_view
import re
import graphs


class Controller(object):

    def __init__(self):
        """
        Initialize a new Controller object.

        :param None:

        :return: None
        :rtype: None
        """
        self.model = prisoners_game_model.prisoners_model(100, 1)
        self.view = prisoners_view.main_view(self)

    def open_graph(self, prisoners_num):
        graphs.show_graph(range(1, int(prisoners_num)))
    
    def show_success_graph(self,game_num):
        graphs.create_success_graph(self.get_game_details(game_num).prisoners)
        
    def change_model_prisoners(self, prisoners_num):
        """
        Change the number of prisoners in the model.

        :param prisoners_num: The new number of prisoners to set in the model.
        :type prisoners_num: int
        :raises: TypeError, ValueError

        :return: None
        :rtype: None
        """
        # Ensure that the input is a valid integer
        try:
            int_prisoners_num = int(prisoners_num)
        except ValueError:
            raise ValueError("Input must be an integer.")

        # Ensure that the input is positive
        if int_prisoners_num <= 0:
            raise ValueError("Input must be a positive integer.")

        # Update the model with the new number of prisoners
        self.model.change_prisoners_number(int(prisoners_num))

    def change_model_games(self, games_num):
        """
               Change the number of games in the model.

               :param games_num: The new number of games to set in the model.
               :type games_num: int
               :raises: ValueError, TypeError

               :return: None
               :rtype: None
               """
        # Ensure that the input is a valid integer
        try:
            int_games_num = int(games_num)
        except ValueError:
            raise ValueError("Input must be an integer.")

        # Ensure that the input is positive
        if int_games_num <= 0:
            raise ValueError("Input must be a positive integer.")

        # Update the model with the new number of games
        self.model.change_games_number(int_games_num)

    def start_game(self, optimized):
        """
        Start a new game with the current model.

        :param optimized: A boolean value indicating whether to use an optimized strategy or not.
        :type optimized: bool

        :return: None
        :rtype: None
        """
        self.model.play(bool(optimized))

    def get_game_details(self, game):
        """
        Get the details for a specific game in the model.

        :param game: The index of the game to retrieve details for.
        :type game: int
        :raises: ValueError, TypeError, IndexError

        :return: A dictionary containing the details for the specified game.
        :rtype: dict
        """
        # Ensure that the input is a valid integer
        try:
            int_game = int(game)
        except ValueError:
            raise ValueError("Input must be an integer.")

        # Ensure that the input is within range
        if int_game < 0 or int_game > len(self.model.games.keys()):
            raise IndexError("Input is out of range.")

        # Return the details for the specified game
        return self.model.games[int_game]

    def input_check(self, game_input):  # , prisoner_number_input):
        """
        Check if the given input values are valid for the current model.

        :param game_input: The index of the game to check for validity.
        :type game_input: int
        :param prisoner_number_input: The number of prisoners to check for validity.
        :type prisoner_number_input: int
        :return: A tuple containing the integer index of the game and the integer number of prisoners if both inputs
                 are valid and within range. Otherwise, False is returned.
        :rtype: tuple or bool
        :raises: None
        """
        # Define the regex pattern for checking if input is a number
        number_pattern = r'^-?\d+(?:\.\d+)?$'

        # Check if both inputs are numbers
        if not bool(re.match(number_pattern, str(game_input))):  # or not bool(re.match(number_pattern, str(prisoner_number_input))):
            return False

        # Convert the inputs to integers
        game_input = int(game_input) - 1
        # prisoner_input = int(prisoner_number_input)

        # Check if game_input is within valid range
        if game_input < 0 or game_input >= len(self.model.games.keys()):
            return False

        # Check if prisoner_number_input is within valid range for the given game
        game = self.get_game_details(game_input)
        # if prisoner_input < 1 or prisoner_input > len(game.prisoners.keys()):
        #     return False

        # If both inputs are valid numbers and within range, return True
        return game_input  # , prisoner_input

    def get_prisoner_details(self, game, prisoner):
        """
        Get the details of a specific prisoner in a specific game.

        :param game: The index of the game.
        :type game: int
        :param prisoner: The index of the prisoner.
        :type prisoner: int
        :return: A dictionary containing the details of the prisoner.
        :rtype: dict
        :raises: IndexError if the game or prisoner index is out of range.
        """
        return self.model.games[game].prisoners[prisoner]

    def get_model_to_string(self):
        """
        Get the current game model as a string.

        :return: A string representation of the current game model.
        :rtype: str
        :raises: None
        """
        return self.model.read_game()

    def get_next_location(self, prisoner):
        """
        Get the next location for the prisoner to move to.

        :param prisoner: The prisoner object.
        :type prisoner: Prisoner
        :return: The next location for the prisoner to move to.
        :rtype: tuple
        :raises: None
        """
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
