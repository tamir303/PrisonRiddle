import sys
import random

class prisoners_model:
    def __init__(self, prisoners_num, games_num):
        """
        :param prisoners_num: number of prisoners
        :param games_num: number of games
        """
        self.prisoners = prisoners_num
        self.games = games_num

    def change_prisoners_number(self, prisoners_num):
        """
        :param prisoners_num: number of prisoners
        :return: None
        """
        self.prisoners = prisoners_num

    def change_games_number(self, games_num):
        """
        :param games_num: number of games
        :return: Exception or None
        """
        self.games = games_num

    def play(self):
        """
        :return:
        """
        success = 0
        games = self.prisoners
        for game in range(games):
            print("game number", (game + 1))
            boxes = self.prisoners * [0]
            for prisoner_index in range(self.prisoners):
                boxes[prisoner_index] = prisoner_index
            random.shuffle(boxes)

            if self.prison_round(boxes):
                success += 1

        print("n =", self.prisoners, " k =", games, " success = ", success,
              "\nsuccess / k in % =", 100 * (success / games))
        success = 0
        half_prisoners_number = self.prisoners / 2
        for games in range(self.prisoners // 2):
            success += 1 / (half_prisoners_number + (games + 1))
        print("probability by loop calculate the geometric series:\n",
              "1 - (1/((n/2)+1) + 1/((n/2)+2) + ...) =", 1 - success)

    def prison_round(self, boxes):
        """
        :param boxes: List of all boxes containing the prisoner's number by order
        :return: True - All prisoners found their number, else False
        """
        number_of_boxes = len(boxes)
        prisoners_status_list = number_of_boxes * [0]
        for prisoner in range(number_of_boxes):
            print("prisoner =", prisoner)
            checked_boxes = []
            picked_box = boxes[prisoner]
            checked_boxes.append(picked_box)
            for pick in range(number_of_boxes):
                success = False
                print("try number =", pick, " picked_box =", picked_box)
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

            print("boxes list by order:", end=" ")
            for index in range(number_of_boxes):
                print(boxes[index], end=" ")
            print()
            print("picked boxes values by oder:", end=" ")
            for index in range(len(checked_boxes)):
                print(checked_boxes[index], end=" ")
            print()
            if success:
                print("prisoner number ", prisoner, " succeeded ", "chain length =", (pick + 1))
            else:
                print("prisoner number ", prisoner, " failed ", "chain length =", (pick + 1))

        print("number of prisoners that found their number is:",
              sum(prisoners_status_list), "\n    from", number_of_boxes, " prisoners.\n")
        if sum(prisoners_status_list) == number_of_boxes:
            return True
        else:
            return False
