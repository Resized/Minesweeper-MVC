import tkinter as tk
from tkinter import ttk, font
import tkinter.font as tkf
import time

import utils
from model import Model


class View:

    def __init__(self):
        self.controller = None
        self.model = None
        self.game_frame = None
        self.board = None
        self.flag = None
        self.mine = None
        self.time = None
        self.difficulty_str = None

    # Main unresizable window ######################################################
    def create_main_window(self):
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.window["bg"] = "white"
        self.window.resizable(width=False, height=False)
        self.create_images()
        self.create_board(self.window)
        self.create_top_frame(self.window)
        return self.window

    def set_controller(self, controller):
        self.controller = controller

    def set_model(self, model: Model):
        self.model = model

    # Images #######################################################################
    def create_images(self):
        self.flag = tk.PhotoImage(file="images/red_flag.gif")
        self.mine = tk.PhotoImage(file="images/mine.gif")
        self.time = tk.PhotoImage(file="images/time.gif")

    # Game frame ###################################################################
    def create_board(self, window):
        self.game_frame = tk.Frame(window, borderwidth=2, relief=tk.SUNKEN)
        my_font = font.Font(family='fixedsys', size=18)

        def create_square(i, j):
            f = tk.Frame(self.game_frame, height=30, width=30)
            s = tk.Button(f, borderwidth=2, state="normal", font=my_font, highlightthickness=10)
            s.pack(fill=tk.BOTH, expand=True)

            # buttons bindings
            def __handler(event, x=i, y=j):
                if event.num == 1:
                    self.controller.left_handler(x, y)
                elif event.num == 3:
                    self.controller.right_handler(x, y)
                else:
                    raise Exception('Invalid event code.')

            s.bind("<Button-1>", __handler)
            s.bind("<Button-3>", __handler)

            f.pack_propagate(False)
            f.grid(row=i, column=j)
            return s

        self.board = [[create_square(i, j) for j in range(self.model.get_width())]
                      for i in range(self.model.get_height())]
        self.game_frame.pack(padx=10, pady=10, side=tk.BOTTOM)
        return self.board

    # Top frame ####################################################################

    def create_top_frame(self, window):
        top_frame = tk.Frame(window, borderwidth=2, height=40, relief=tk.GROOVE)
        top_frame.pack(padx=0, pady=0, side=tk.TOP, fill="x")
        for i in range(4):
            top_frame.columnconfigure(i, weight=1)
        self.create_bombs_counter(top_frame)
        self.create_new_game_button(top_frame)
        self.create_difficulty_cbox(top_frame)
        self.create_time_counter(top_frame)
        return top_frame

    def create_bombs_counter(self, top_frame):
        """ bombs_counter, left """
        bomb_frame = tk.Frame(top_frame, borderwidth=2, height=40, relief=tk.GROOVE)
        bomb_img = tk.Label(bomb_frame, image=self.mine)
        bombs_counter_str = tk.StringVar()

        def update_bombs_counter():
            bombs_counter_str.set(self.model.get_bombs_left())
            top_frame.after(100, update_bombs_counter)

        update_bombs_counter()

        bombs_counter = tk.Label(bomb_frame, height=1, width=3, bg='white',
                                 textvariable=bombs_counter_str,
                                 font=tkf.Font(weight='bold', size=10))
        bombs_counter.grid(row=0, column=0, padx=2, sticky=tk.W)
        bomb_img.grid(row=0, column=1, padx=2, sticky=tk.E)
        bomb_frame.grid(row=0, column=0, padx=5, sticky=tk.W)

    def create_new_game_button(self, top_frame):
        """ new game button, middle left """

        def _start_new_game():
            self.controller.start_new_game()

        newgame_button = tk.Button(top_frame, bd=1, width=10, text="New game",
                                   command=_start_new_game)
        newgame_button.grid(row=0, column=1, padx=0, sticky=tk.E)

    def create_difficulty_cbox(self, top_frame):
        """ difficulty combo box, middle right """

        def _set_difficulty(selected_difficulty):
            self.game_frame.destroy()
            self.controller.set_difficulty(utils.str_to_difficulty_enum(selected_difficulty.widget.get()))
            self.board = self.create_board(self.window)
            self.controller.start_new_game()
            top_frame.focus_set()

        # Using self so var won't get garbage collected, and default value would show
        self.difficulty_str = tk.StringVar()

        # Adding combobox drop down list
        self.difficulty = ttk.Combobox(top_frame, width=10,
                                       textvariable=self.difficulty_str, values=utils.difficulty_list(),
                                       state='readonly')

        self.difficulty.current(0)
        self.difficulty.grid(row=0, column=3, padx=5, sticky=tk.W)
        self.difficulty.bind("<<ComboboxSelected>>", _set_difficulty)

    def create_time_counter(self, top_frame):
        """ time counter, right """
        time_frame = tk.Frame(top_frame, borderwidth=2, height=40, relief=tk.GROOVE)
        time_counter_str = tk.StringVar()
        time_img = tk.Label(time_frame, image=self.time)

        def update_time_counter():
            time_counter_str.set(int((time.time() - self.model.get_init_time()) // 1))
            top_frame.after(100, update_time_counter)

        update_time_counter()

        time_counter = tk.Label(time_frame, height=1, width=3, bg='white',
                                textvariable=time_counter_str,
                                font=tkf.Font(slant='italic', size=10))
        time_counter.grid(row=0, column=1, padx=2, sticky=tk.W)
        time_img.grid(row=0, column=0, padx=2, sticky=tk.E)
        time_frame.grid(row=0, column=4, padx=5, sticky=tk.E)

    def set_bomb(self, i, j):
        """ set given square by (i,j) to bomb """
        self.board[i][j]["bg"] = "#e50000"
        self.board[i][j]["image"] = self.mine
        self.board[i][j]["state"] = "normal"

    def is_empty_image(self, i, j):
        return self.board[i][j]["image"] == ""

    def set_clicked(self, i, j):
        self.board[i][j]["state"] = "disabled"
        self.board[i][j]["relief"] = tk.SUNKEN
        self.board[i][j]["bg"] = "gray80"

    def set_bomb_text(self, i, j, text, color):
        self.board[i][j]["text"] = text
        self.board[i][j]["disabledforeground"] = color

    def set_flag(self, i, j):
        self.board[i][j]["image"] = self.flag
        self.board[i][j]["state"] = "normal"

    def set_disabled(self, i, j):
        self.board[i][j]["state"] = "disabled"
        self.board[i][j]["image"] = ""

    def reset_board(self, height, width):
        for x in range(height):
            for y in range(width):
                self.board[x][y]["image"] = ""
                self.board[x][y]["text"] = ""
                self.board[x][y]["state"] = tk.DISABLED
                self.board[x][y]["relief"] = tk.RAISED
                self.board[x][y]["bg"] = "SystemButtonFace"

    def set_cbox_value(self, value):
        self.difficulty.set(value)
