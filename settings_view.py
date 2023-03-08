import tkinter as tk

class settings_view:
    def __init__(self, x_size, y_size, controller):
        # Main game settings
        self.controller = controller
        self.root = tk.Tk()
        self.root.title('Prisoners Escape')
        self.root.resizable(width=False, height=False)
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (x_size, y_size, (self.screenwidth - x_size) / 2, (self.screenheight - y_size) / 2)
        self.root.geometry(alignstr)
        self.settings_screen = tk.Frame(self.root)

        # Buttons, Labels, TextInput ...
        self.startLabel = tk.Label(text="Press to start the game")
        self.playButton = tk.Button(self.root, text='Play', command=lambda: self.play())

        self.prisonerstLabel = tk.Label(text="Enter amount of prisoners")
        self.prisonersInput = tk.Text(self.root, height=5, width=15)

        self.gamesLabel = tk.Label(text="Enter number of games")
        self.gamesInput = tk.Text(self.root, height=5, width=15)

        self.strategyLabel = tk.Label(text="Choose your strategy")
        self.optimized = False
        self.optimizedRadioOn = tk.Radiobutton(self.root, text="Optimized", variable=self.optimized,
                                               value=True, command=lambda: self.change_opt(True))
        self.optimizedRadioOff = tk.Radiobutton(self.root, text="Random", variable=self.optimized,
                                                value=False, command=lambda: self.change_opt(False))

        self.packing()

    def play(self):
        self.__change_game_settings()
        self.controller.start_game(self.optimized)

    def __change_game_settings(self):
        self.controller.change_model_prisoners(self.prisonersInput.get("1.0", 'end-1c'))
        self.controller.change_model_games(self.gamesInput.get("1.0", 'end-1c'))

    def get_settings_screen(self):
        return self.settings_screen

    def update_settings(self):
        self.settings_screen.update()

    def change_opt(self, val):
        self.optimized = val

    def packing(self):
        self.settings_screen.pack()
        self.startLabel.pack()
        self.playButton.pack()
        self.prisonerstLabel.pack()
        self.prisonersInput.pack()
        self.gamesLabel.pack()
        self.gamesInput.pack()
        self.strategyLabel.pack()
        self.optimizedRadioOn.pack(side=tk.BOTTOM, ipady=2)
        self.optimizedRadioOff.pack(side=tk.BOTTOM, ipady=2)
