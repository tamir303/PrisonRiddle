import prisoners_game_model
import prisoners_view


def prisoners_Assert(prisoners_num):
    assert prisoners_num.isnumeric(), 'prisoners_num value must be integer'
    assert int(prisoners_num) >= 2, 'numbers of prisoners =", {}, " prisoners must be > 1'.format(
        prisoners_num)


def games_Assert(games_num):
    assert games_num.isnumeric(), 'games_num value must be integer'
    assert int(games_num) > 0, 'numbers of prisoners =", {}, " prisoners must be > 1'.format(
        games_num)


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
        return self.model.play(bool(optimized))

    def get_game_details(self, game):
        return self.model.games[game]

    def get_prisoner_details(self, prisoner, game):
        return self.model.games[game].prisoners[prisoner]

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
