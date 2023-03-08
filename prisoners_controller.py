import prisoners_game_model
import prisoners_view

def prisoners_Assert(prisoners_num):
    assert prisoners_num.isnumeric(), 'prisoners_num value must be integer'
    assert int(prisoners_num) >= 2, 'numbers of prisoners =", {}, " prisoners must be > 1'.format(prisoners_num)


def games_Assert(games_num):
    assert games_num.isnumeric(), 'games_num value must be integer'
    assert int(games_num) > 0, 'numbers of prisoners =", {}, " prisoners must be > 1'.format(games_num)


class Controller(object):

    def __init__(self, model: prisoners_game_model, view: prisoners_view):
        self.model = model
        self.view = view
        self.run()

    def run(self):
        self.model(100, 1)
        self.view(1200, 900, self)

    def change_model_prisoners(self, prisoners_num):
        prisoners_Assert(prisoners_num)
        self.model.change_prisoners_number(self.model, int(prisoners_num))

    def change_model_games(self, games_num):
        games_Assert(games_num)
        self.model.change_games_number(self.model, int(games_num))

    def start_game(self, optimized):
        self.model.play(self.model, bool(optimized))
