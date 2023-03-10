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

    def play(self, optimized):
        """
        :return:
        """
        # sys.stdout = open("PrisonersReults.txt", "w")
        success = 0
        games = self.games
        strategy = {True: self.optimized_prison_round, False: self.unoptimized_prison_round}[optimized]
        for game in range(games):
            print("game number", (game + 1))
            boxes = self.prisoners * [0]
            for prisoner_index in range(self.prisoners):
                boxes[prisoner_index] = prisoner_index
            random.shuffle(boxes)

            if strategy(self, boxes):
                success += 1

        print("n =", self.prisoners, " k =", self.games, " s = ", success,
              "\ns / k in % =", 100 * (success / games))
        success = 0
        half_prisoners_number = self.prisoners / 2
        for games in range(self.prisoners // 2):
            success += 1 / (half_prisoners_number + (games + 1))
        if optimized:
            print("probability by loop calculate the geometric series:\n",
                  "1 - (1/((n/2)+1) + 1/((n/2)+2) + ...) =", 1 - success)
        else:
            print("probability by random picking:\n",
                  "1/(2^n) =", 1 / 2**self.prisoners)
        # sys.stdout.close()

    def unoptimized_prison_round(self, boxes):
        """
        :param boxes: List of all boxes containing the prisoner's number by order
        :return: True - All prisoners found their number, else False
        """
        number_of_boxes = len(boxes)
        prisoners_status_list = number_of_boxes * [0]
        for prisoner in range(number_of_boxes):
            print("prisoner =", prisoner)
            checked_boxes = []
            pick = 0
            while True:
                picked_box = random.randint(0, number_of_boxes - 1)
                if picked_box not in checked_boxes:
                    print("try number =", pick, " picked_box =", picked_box)
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
                print("prisoner number ", prisoner, " succeeded ", "chain length = ", len(checked_boxes))
            else:
                print("prisoner number ", prisoner, " failed ", "chain length =", len(checked_boxes))
            checked_boxes.clear()
        print("number of prisoners that find their number is:", sum(prisoners_status_list), "\n    from",
              number_of_boxes, " prisoners.\n")
        if sum(prisoners_status_list) == number_of_boxes:
            return True
        else:
            return False

    def optimized_prison_round(self, boxes):
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

            print("boxes values list by order:", end=" ")
            for val in checked_boxes:
                print(val, end=" ")
            print()
            if success:
                print("prisoner number ", prisoner, " succeeded ", "chain length =", (pick + 1))
            else:
                print("prisoner number ", prisoner, " failed ", "chain length =", (pick + 1))
            checked_boxes.clear()

        print("number of prisoners that found their number is:", sum(prisoners_status_list), "\n    from",
              number_of_boxes, " prisoners.\n")
        if sum(prisoners_status_list) == number_of_boxes:
            return True
        else:
            return False
