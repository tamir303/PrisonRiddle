import tkinter as tk
from tkinter import font
import prisoners_view
import threading
class settings_view:
    def __init__(self, x_size, y_size, controller, main_view):
           # Main game settings
        self.controller = controller
        self.main_view = main_view
        self.root = tk.Tk()
        self.root.title('Prisoners Escape')
        self.root.resizable(width=False, height=False)
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        self.settings_screen = tk.Frame(self.root, bg='#f5deb3')
        alignstr = '%dx%d+%d+%d' % (x_size, y_size, (self.screenwidth - x_size) / 2, (self.screenheight - y_size) / 2)
        self.root.geometry(alignstr)
        self.root.configure(bg='#F5DEB3')  # Set light brown background

        # Buttons, Labels, TextInput ...
        font_style = font.Font(family='Arial', size=12, weight='bold')
        button_style = {'bg': '#8FBC8F', 'fg': 'white', 'font': font_style, 'activebackground': '#90EE90'}

        self.startLabel = tk.Label(text="Press to start the game", font=font_style, bg='#F5DEB3')
        self.playButton = tk.Button(self.root, text='Play', command=lambda: self.play(), **button_style)
        
        self.simulationLabel = tk.Label(text="Open Game Simulation", font=font_style, bg='#F5DEB3')
        self.playSimulationButton = tk.Button(self.root, text='PlaySimulation', command=lambda: self.play_simulation(), **button_style)

        self.prisonerstLabel = tk.Label(text="Enter amount of prisoners", font=font_style, bg='#F5DEB3')
        self.prisonersInput = tk.Scale(self.root, from_=2, to=1000, orient=tk.HORIZONTAL, length=400,
                                       font=font_style, bg='#F5DEB3')

        self.gamesLabel = tk.Label(text="Enter number of games", font=font_style, bg='#F5DEB3')
        self.gamesInput = tk.Scale(self.root, from_=1, to=100, orient=tk.HORIZONTAL, length=400,
                                    font=font_style, bg='#F5DEB3')

        self.strategyLabel = tk.Label(text="Choose your strategy", font=font_style, bg='#F5DEB3')
        self.optimized = False
        self.optimizedRadioOn = tk.Radiobutton(self.root, text="Optimized", variable=self.optimized,
                                               value=True, command=lambda: self.change_opt(True),
                                               font=font_style, bg='#F5DEB3', activebackground='#90EE90')
        self.optimizedRadioOff = tk.Radiobutton(self.root, text="Random", variable=self.optimized,
                                                value=False, command=lambda: self.change_opt(False),
                                                font=font_style, bg='#F5DEB3', activebackground='#90EE90')
        
        self.packing()
        self.root.mainloop()

    def play(self):
        self.__change_game_settings()
        self.controller.start_game(self.optimized)
    def play_simulation(self):
        my_thread = threading.Thread(target= self.main_view.run())
        # Start the thread
        my_thread.start()
        # Wait for the thread to finish (optional)
        my_thread.join()
    def __change_game_settings(self):
        self.controller.change_model_prisoners(self.prisonersInput.get())
        self.controller.change_model_games(self.gamesInput.get())

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
        self.simulationLabel.pack()
        self.playSimulationButton.pack()
        self.prisonerstLabel.pack()
        self.prisonersInput.pack()
        self.gamesLabel.pack()
        self.gamesInput.pack()
        self.strategyLabel.pack()
        self.optimizedRadioOn.pack(side=tk.LEFT, ipady=2)
        self.optimizedRadioOff.pack(side=tk.LEFT, ipady=2)