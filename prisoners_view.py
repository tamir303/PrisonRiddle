
import settings_view
import game_view

class main_view:
    def __init__(self, x_size=800, y_size=800, controller=None):
        self.x_size = x_size  # resolution X
        self.y_size = y_size  # resolution Y
        self.controller = controller
        self.settings = settings_view.settings_view(300, 300)
        main_dialog = settings_view.tk.Frame(self.settings.root)
        self.game = game_view.game_view(x_size, y_size, main_dialog)

    def getSettings(self):