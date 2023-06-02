import tkinter as tk
from tkinter import font
import prisoners_view
import threading


class settings_view:
    def __init__(self, x_size, y_size, controller, main_view):
        """
        Initializes the PrisonEscapeGUI object with the given parameters.

        :param x_size: The width of the window in pixels.
        :type x_size: int
        :param y_size: The height of the window in pixels.
        :type y_size: int
        :param controller: The controller object for the game.
        :type controller: PrisonersEscapeController
        :param main_view: The main view object for the game.
        :type main_view: PrisonersEscapeMainView
        """
        # Main game settings
        self.controller = controller
        self.main_view = main_view
        self.root = tk.Tk()
        self.root.title('Prisoners Escape')
        # self.root.resizable(width=False, height=False)
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        self.settings_screen = tk.Frame(self.root, bg='#f5deb3')
        alignstr = '%dx%d+%d+%d' % (x_size, y_size, (self.screenwidth -
                                                     x_size) / 2, (self.screenheight - y_size) / 2)
        self.root.geometry(alignstr)
        self.root.configure(bg='#F5DEB3')  # Set light brown background
        self.game = 0
        # Buttons, Labels, TextInput ...
        font_style = font.Font(family='Arial', size=12, weight='bold')
        button_style = {'bg': '#8FBC8F', 'fg': 'white',
                        'font': font_style, 'activebackground': '#90EE90'}

        self.startLabel = tk.Label(
            text="Press to start the game", font=font_style, bg='#F5DEB3')
        self.playButton = tk.Button(
            self.root, text='Play', command=lambda: self.play(), **button_style)

        self.successgraphButton = tk.Button(
            self.root, text='Game Success Rate Graph', command=lambda: self.showSuccessGraph(), **button_style,state='disabled')
        self.simulationLabel = tk.Label(
            text="Open Game Simulation", font=font_style, bg='#F5DEB3', state='disabled')
        self.adjustspeed = tk.Label(
            text="Adjust Speed", font=font_style, bg='#F5DEB3', state='disabled')
        self.simspeed = tk.StringVar(value="low")  # Set the initial value to "low"
        
        self.lowButton = tk.Radiobutton(self.root, text="Low", variable=self.simspeed,
                                        value="low", command=lambda: self.change_speed("low"),
                                        font=('Arial', 12), bg='#F5DEB3', activebackground='#90EE90')
        
        self.medButton = tk.Radiobutton(self.root, text="Med", variable=self.simspeed,
                                        value="med", command=lambda: self.change_speed("med"),
                                        font=('Arial', 12), bg='#F5DEB3', activebackground='#90EE90')
        
        self.fastButton = tk.Radiobutton(self.root, text="Fast", variable=self.simspeed,
                                         value="fast", command=lambda: self.change_speed("fast"),
                                         font=('Arial', 12), bg='#F5DEB3', activebackground='#90EE90')
        
        self.playSimulationButton = tk.Button(
            self.root, text='PlaySimulation', command=lambda: self.play_simulation(), **button_style, state='disabled')

        self.prisonerstLabel = tk.Label(
            text="Enter amount of prisoners", font=font_style, bg='#F5DEB3')
        self.prisonersInput = tk.Scale(self.root, from_=2, to=25, orient=tk.HORIZONTAL, length=200,
                                       font=font_style, bg='#F5DEB3')

        self.gamesLabel = tk.Label(
            text="Enter number of games", font=font_style, bg='#F5DEB3')
        self.gamesInput = tk.Scale(self.root, from_=1, to=100, orient=tk.HORIZONTAL, length=200,
                                   font=font_style, bg='#F5DEB3')

        self.strategyLabel = tk.Label(
            text="Choose your strategy", font=font_style, bg='#F5DEB3')
        self.optimized = False
        self.optimizedRadioOn = tk.Radiobutton(self.root, text="Random", variable=self.optimized,
                                               value=False, command=lambda: self.change_opt(False),
                                               font=font_style, bg='#F5DEB3', activebackground='#90EE90')
        self.optimizedRadioOff = tk.Radiobutton(self.root, text="Optimized", variable=self.optimized,
                                                value=True, command=lambda: self.change_opt(True),
                                                font=font_style, bg='#F5DEB3', activebackground='#90EE90')
        self.optimized = True
        self.text_area = tk.Text(self.root, height=40, width=60)
        self.scrollbar = tk.Scrollbar(self.root, command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        self.gameInputLabel = tk.Label(self.root, text="Enter game number:", font=font_style, bg='#F5DEB3',
                                       state='disable')
        self.gameInputentry = tk.Entry(self.root, validate="key", state='disable')
        # self.prisoner_number_InputLabel = tk.Label(self.root, text="Enter Prioner number:", font=font_style,
        #                                            bg='#F5DEB3', state='disable')
        # self.prisoner_number_input_entry = tk.Entry(self.root, validate="key", state='disable')
        self.packing()
        self.root.mainloop()

    def play(self):
        """
        Starts the game and sets game settings. Deletes the content of the text_area, enables some buttons
        and inputs, and adds text to the text_area based on the controller's output.

        :return: None
        """
        self.__change_game_settings()
        self.controller.start_game(self.optimized)
        self.text_area.delete("1.0", tk.END)
        self.simulationLabel['state'] = 'normal'
        self.adjustspeed['state'] ='normal'
        self.playSimulationButton['state'] = 'normal'
        self.successgraphButton['state'] = 'normal'
        self.gameInputLabel['state'] = 'normal'
        self.gameInputentry['state'] = 'normal'
        # self.prisoner_number_input_entry['state'] = 'normal'
        # self.prisoner_number_InputLabel['state'] = 'normal'
        self.text_area.insert(tk.END, self.controller.get_model_to_string())
        self.text_area.tag_configure("failed", foreground="red")
        
    def showGraph(self):
        my_thread = threading.Thread(target=self.controller.open_graph(self.prisonersInput.get()))
        # Start the thread
        my_thread.start()
        # Wait for the thread to finish (optional)
    def showSuccessGraph(self):
        input = self.controller.input_check(self.gameInputentry.get()) #, self.prisoner_number_input_entry.get())
        if input is False:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", "Failed Input", "failed")
            return
        else:
            self.text_area.tag_configure("failed", foreground="black")
        my_thread = threading.Thread(target=self.controller.show_success_graph(input))
        # Start the thread
        my_thread.start()
        # Wait for the thread to finish (optional)

    def play_simulation(self):
        """
        Validates input values and displays error message in the text area if validation fails.
        Otherwise, configure text area for simulation results.
        """
        input = self.controller.input_check(self.gameInputentry.get()) #, self.prisoner_number_input_entry.get())
        if input is False:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", "Failed Input", "failed")
            return
        else:
            self.text_area.tag_configure("failed", foreground="black")

        my_thread = threading.Thread(target=self.main_view.run(self, input,self.simspeed)) #, input[1]))
        # Start the thread
        my_thread.start()
        # Wait for the thread to finish (optional)
        my_thread.join()

    def __change_game_settings(self):
        """
        Updates the model's prisoner and game settings based on the values entered in the GUI input fields.

        :return: None
        """
        self.controller.change_model_prisoners(self.prisonersInput.get())
        self.controller.change_model_games(self.gamesInput.get())

    def get_settings_screen(self):
        """
        Returns the settings screen object.

        :return: The settings screen object.
        """
        return self.settings_screen

    def update_settings(self):
        """
        Updates the settings screen.

        :return: None
        """
        self.settings_screen.update()

    def change_opt(self, val):
        """
        Changes the value of the 'optimized' attribute to the given value.

        :param val: The new value of the 'optimized' attribute.
        :return: None
        """
        self.optimized = val
        
    def change_speed(self, val):
        """
        Changes the value of the 'optimized' attribute to the given value.

        :param val: The new value of the 'optimized' attribute.
        :return: None
        """
        self.simspeed=val
        
    def validate_integer(self, text):
        """
        Validates whether the given string is a valid integer or not.

        :param text: The string to be validated.
        :return: True if the string is a valid integer, False otherwise.
        """
        if text.isdigit():
            return True
        elif text == "":
            return True
        else:
            return False

    def packing(self):
        """
        Packs all widgets in the GUI window.
        Positions widgets on the left side of the window including the settings screen, scrollbar, and text area.
        Sets positions of various labels, inputs, and buttons in the settings screen.

        :return: None
        """
        # Left side
        self.settings_screen.pack(side=tk.LEFT, padx=10, pady=10)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        self.text_area.pack(side=tk.RIGHT, anchor=tk.N, pady=10, expand=True, fill=tk.Y)

        self.prisonerstLabel.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.prisonersInput.pack(side=tk.TOP, anchor=tk.W, pady=5)

        self.gamesLabel.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.gamesInput.pack(side=tk.TOP, anchor=tk.W, pady=5)

        self.startLabel.pack(side=tk.TOP, anchor=tk.W)
        self.strategyLabel.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.optimizedRadioOn.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.optimizedRadioOff.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.playButton.pack(side=tk.TOP, anchor=tk.W, pady=5)
        
        self.gameInputLabel.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.gameInputentry.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.successgraphButton.pack(side=tk.TOP, anchor=tk.W, pady=10)
        

        # self.prisoner_number_InputLabel.pack(side=tk.TOP, anchor=tk.W, pady=5)
        # self.prisoner_number_input_entry.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.simulationLabel.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.adjustspeed.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.lowButton.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.medButton.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.fastButton.pack(side=tk.TOP, anchor=tk.W, pady=5)
        self.playSimulationButton.pack(side=tk.TOP, anchor=tk.W, pady=5)



        # Right side
