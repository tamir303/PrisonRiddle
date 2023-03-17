import sys
import random


class prisoner_struct:
    def __init__(self, number, checkBoxesList, isSuccess):
        self.number = number
        self.checkBoxesList = checkBoxesList
        self.isSuccess = isSuccess


class game_struct:
    def __init__(self, number):
        self.number = number
        self.prisoners = {}
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
        self.total_print = ""

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
        :return:
        """
        # sys.stdout = open("PrisonersReults.txt", "w")
        success = 0
        self.total_print= ""
        strategy = {True: self.optimized_prison_round, False: self.unoptimized_prison_round}[optimized]
        for game in range(self.num_of_games):
            self.total_print += "-------------------------------------------------------------- \n"
            self.total_print += "game number " + str(game + 1) + "\n\t"
            boxes = self.prisoners_num * [0]
            for prisoner_index in range(self.prisoners_num):
                boxes[prisoner_index] = prisoner_index
            random.shuffle(boxes)
            self.games[game] = game_struct(game)
            if strategy(boxes, game):
                success += 1
                self.games[game].isSuccess = True

        self.total_print += "\n\nn = " + str(self.prisoners_num) + " k = " + str(self.num_of_games) + " s = " + str(success) + "\n\ts / k in % = " + str(100 * (success / self.num_of_games)) + "\n\n"
        success = 0
        half_prisoners_number = self.prisoners_num / 2
        for self.num_of_games in range(self.prisoners_num // 2):
            success += 1 / (half_prisoners_number + (self.num_of_games + 1))
        if optimized:
            self.total_print += "probability by loop calculate the geometric series:\n\t" + "1 - (1/((n/2)+1) + 1/((n/2)+2) + ...) = " + str(1 - success) + "\n\n"
        else:
            self.total_print += "probability by random picking:\n\t" + "1/(2^n) = " + str(1 / 2**self.prisoners_num) + "\n\n"
        # sys.stdout.close()
        return self.total_print

    def unoptimized_prison_round(self, boxes, game):
        """
        :param boxes: List of all boxes containing the prisoner's number by order
        :return: True - All prisoners found their number, else False
        """
        number_of_boxes = len(boxes)
        prisoners_status_list = number_of_boxes * [0]
        for prisoner in range(number_of_boxes):
            self.total_print += "\tprisoner =" + str(prisoner) + "\n"
            checked_boxes = []
            pick = 0
            while True:
                picked_box = random.randint(0, number_of_boxes - 1)
                if picked_box not in checked_boxes:
                    self.total_print += "\t\ttry number =" + str(pick) + " picked_box =" + str(picked_box) + "\n"
                    checked_boxes.append(picked_box)
                    pick += 1
                    if picked_box == prisoner:
                        break
            if len(checked_boxes) <= (number_of_boxes // 2):
                prisoners_status_list[prisoner] = 1
            self.total_print += "\n\tboxes values list by order:"
            for val in checked_boxes:
                self.total_print +=", "+ str(val)
            self.total_print+="\n"
            if len(checked_boxes) <= (number_of_boxes // 2):
                self.total_print += "\tprisoner number " + str(prisoner) + " succeeded " + "chain length = " + str(len(checked_boxes)) + "\n"
            else:
                self.total_print += "\tprisoner number " + str(prisoner) + " failed " + "chain length =" + str(len(checked_boxes)) + "\n"
            self.games[game].prisoners[prisoner] = prisoner_struct(
                prisoner, checked_boxes.copy(), prisoners_status_list[prisoner])
            checked_boxes.clear()
            self.total_print += "\t" + "number of prisoners that find their number is:" + str(sum(prisoners_status_list)) + " from " + str(number_of_boxes) + " prisoners.\n\n"
            if sum(prisoners_status_list) == number_of_boxes:
                return True
            else:
                return False

    def optimized_prison_round(self, boxes, game):
        """
        :param boxes: List of all boxes containing the prisoner's number by order
        :return: True - All prisoners found their number, else False
        """
        number_of_boxes = len(boxes)
        prisoners_status_list = number_of_boxes * [0]
        checked_boxes = []
        for prisoner in range(number_of_boxes):
            checked_boxes.append(boxes[prisoner])
            if len(checked_boxes) <= (number_of_boxes // 2):
                prisoners_status_list[prisoner] = 1
            self.total_print += "prisoner number " + str(prisoner) + " succeeded " + "chain length = " + str(
                len(checked_boxes)) + "\n"
            self.games[game].prisoners[prisoner] = prisoner_struct(
                prisoner, checked_boxes.copy(), prisoners_status_list[prisoner])
        if sum(prisoners_status_list) == number_of_boxes:
            return True
        else:
            return False