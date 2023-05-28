import sys
import random


class prisoner_struct:
    def __init__(self, number, checkBoxesList, isSuccess):
        self.number = number
        self.checkBoxesList = checkBoxesList
        self.isSuccess = isSuccess


class game_struct:
    def __init__(self, number, prisoners):
        self.number = number
        self.prisoners = prisoners
        self.isSuccess = False

    def set_succes(self):
        self.isSuccess = True


class prisoners_model:
    def __init__(self, prisoners_num, num_of_games):
        """
        :param prisoners_num: number of prisoners
        :param games_num: number of games
        """
        self.prisoners_num = prisoners_num
        self.num_of_games = num_of_games
        self.games = {}

    def change_prisoners_number(self, prisoners_num):
        """
        :param prisoners_num: number of prisoners
        :return: None
        """
        self.prisoners_num = prisoners_num

    def change_games_number(self, games_num):
        """
        :param games_num: number of games
        :return: Exception or None
        """
        self.num_of_games = games_num

    def play(self, optimized):
        """
        :param optimized: what strategy will the prisoners apply
        :return: None
        """
        sys.stdout = open("PrisonersReults.txt", "w")
        print('\t\t### PRISONERS ESCAPE #####')
        print('\t\t    Number Of Games: {}'.format(self.num_of_games))
        print('\t\t  Number Of Prisoners: {}'.format(self.prisoners_num))
        print('------------------------------------------------------------')

        success = 0
        strategy = {True: self.optimized_prison_round,
                    False: self.unoptimized_prison_round}[optimized]
        for game in range(self.num_of_games):
            print("game number", (game + 1))
            boxes = self.prisoners_num * [0]
            for prisoner_index in range(self.prisoners_num):
                boxes[prisoner_index] = prisoner_index
            random.shuffle(boxes)
            self.games[game] = game_struct(game, boxes)
            if strategy(boxes, game):
                success += 1
                self.games[game].isSuccess = True

        print("prisoners =", self.prisoners_num, " games =", self.num_of_games, " success = ", success,
              "\nsuccess / games in % =", 100 * (success / self.num_of_games))
        success = 0
        half_prisoners_number = self.prisoners_num / 2
        for self.num_of_games in range(self.prisoners_num // 2):
            success += 1 / (half_prisoners_number + (self.num_of_games + 1))
        if optimized:
            print("probability by loop calculate the geometric series:\n",
                  "1 - (1/((prisoners/2)+1) + 1/((prisoners/2)+2) + ...) =", 1 - success)
        else:
            print("probability by random picking:\n",
                  "1/(2^prisoners) =", 1 / 2 ** self.prisoners_num)
        sys.stdout = sys.__stdout__

    def unoptimized_prison_round(self, boxes, game):
        """
        :param game: Number of a specific game
        :param boxes: List of all boxes containing the prisoner's number by order
        :return: True - All prisoners found their number, else False
        """
        number_of_boxes = len(boxes)
        prisoners_status_list = number_of_boxes * [0]
        for prisoner in range(number_of_boxes):
            print("prisoner =", prisoner + 1)
            checked_boxes = []
            pick = 0
            while True:
                picked_box = random.randint(0, number_of_boxes - 1)
                if picked_box not in checked_boxes:
                    print("try number =", pick + 1, " picked_box =", picked_box)
                    checked_boxes.append(picked_box)
                    pick += 1
                    if picked_box == prisoner:
                        break
            if len(checked_boxes) <= (number_of_boxes // 2):
                prisoners_status_list[prisoner] = 1
            print()
            print("boxes values list by order:", end=" ")
            for val in checked_boxes:
                print(val, end=" ")
            print()
            if len(checked_boxes) <= (number_of_boxes // 2):
                print("prisoner number ", prisoner + 1, " succeeded ",
                      "chain length = {}\n".format(pick + 1))
            else:
                print("prisoner number ", prisoner + 1, " failed ",
                      "chain length = {}\n".format(pick + 1))
            self.games[game].prisoners[prisoner] = prisoner_struct(
                prisoner, checked_boxes.copy(), prisoners_status_list[prisoner])
            checked_boxes.clear()
        print("number of prisoners that find their number is:", sum(prisoners_status_list), "\n    from",
              number_of_boxes, " prisoners.\n")
        if sum(prisoners_status_list) == number_of_boxes:
            return True
        else:
            return False

    def optimized_prison_round(self, boxes, game):
        """
        :param game: Number of a specific game
        :param boxes: List of all boxes containing the prisoner's number by order
        :return: True - All prisoners found their number, else False
        """
        temp = boxes.copy()
        number_of_boxes = len(boxes)
        prisoners_status_list = number_of_boxes * [0]
        for prisoner in range(number_of_boxes):
            print("prisoner =", prisoner + 1)
            boxes = temp.copy()
            checked_boxes = []
            picked_box = boxes[prisoner]
            checked_boxes.append(picked_box)
            success = False
            for pick in range(number_of_boxes):
                print("try number =", pick + 1, " picked_box =", picked_box)
                if picked_box == prisoner and pick < (number_of_boxes // 2):
                    success = True
                    prisoners_status_list[prisoner] = 1
                    break
                else:
                    if picked_box == prisoner:
                        break
                    else:
                        picked_box = boxes[picked_box]
                        checked_boxes.append(picked_box)
            self.games[game].prisoners[prisoner] = prisoner_struct(
                prisoner, checked_boxes.copy(), success)
            print("boxes values list by order:", end=" ")
            for val in checked_boxes:
                print(val, end=" ")
            if success:
                print("prisoner number ", prisoner + 1,
                      " succeeded ", "chain length = {}\n".format(pick + 1))
            else:
                print("prisoner number ", prisoner + 1,
                      " failed ", "chain length = {}\n".format(pick + 1))
            checked_boxes.clear()

        print("number of prisoners that found their number is:", sum(prisoners_status_list), "\n    from",
              number_of_boxes, " prisoners.\n")
        if sum(prisoners_status_list) == number_of_boxes:
            return True
        else:
            return False

    def read_game(self):
        f = open("PrisonersReults.txt", "r")
        data = f.read()
        return data
