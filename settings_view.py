import tkinter as tk
import prisoners_view

class settings_view:
    def __init__(self, x_size, y_size):
        # Main game settings
        self.root = tk.Tk()
        self.root.title('Prisoners Escape')
        self.root.resizable(width=False, height=False)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (x_size, y_size, (screenwidth - x_size) / 2, (screenheight - y_size) / 2)
        self.root.geometry(alignstr)

        # Buttons, Labels, TextInput ...
        startLabel = tk.Label(text="Press to start the game")
        playButton = tk.Button(self.root, text='Play', command=lambda: self.getSettings())
        prisonerstLabel = tk.Label(text="Enter amount of prisoners")
        prisonersInput = tk.Text(self.root, height=5, width=15)
        gamesLabel = tk.Label(text="Enter number of games")
        gamesInput = tk.Text(self.root, height=5, width=15)

        startLabel.pack()
        playButton.pack()
        prisonerstLabel.pack()
        prisonersInput.pack()
        gamesLabel.pack()
        gamesInput.pack()

    def getSettings(self):
        prisoners_view.main_view.controller