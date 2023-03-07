def prisoners_Assert(prisoners_num):
    assert isinstance(prisoners_num, int), 'prisoners_num value must be integer'
    assert prisoners_num < 2, 'numbers of prisoners =", {}, " prisoners must be > 1'.format(prisoners_num)


def games_Assert(games_num):
    assert isinstance(games_num, int), 'games_num value must be integer'
    assert games_num <= 0, 'numbers of prisoners =", {}, " prisoners must be > 1'.format(games_num)


class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.start()

    def start(self):
        self.model(100, 1)
        self.view(1200, 900)

    def change_model_prisoners(self, prisoners_num):
        prisoners_Assert(prisoners_num)
        self.model.change_prisoners_number(prisoners_num)

    def change_model_games(self, games_num):
        games_Assert(games_num)
        self.model.change_games_number(games_num)
