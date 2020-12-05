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

    def create_main_window(self):
        """
        Creates main unresizable window
        """
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

    def create_images(self):
        """
        Load game related images
        """
        self.flag = tk.PhotoImage(file="images/red_flag.gif")
        self.mine = tk.PhotoImage(file="images/mine.gif")
        self.time = tk.PhotoImage(file="images/time.gif")

    def create_board(self, window: tk.Tk):
        """
        Create main game frame

        :param window: Main window to draw upon
        :return: Board which is a list of list of buttons
        """
        self.game_frame = tk.Frame(window, borderwidth=2, relief=tk.SUNKEN)
        my_font = font.Font(family='fixedsys', size=18)

        def create_square(i: int, j: int) -> tk.Button:
            """
            Create an individual button in grid by height and width location

            :param i: Height location of the cell
            :param j: Width location of the cell
            :return: tkinter Button as cell
            """
            frame = tk.Frame(self.game_frame, height=30, width=30)
            cell = tk.Button(frame, borderwidth=2, state="normal", font=my_font, highlightthickness=10)
            cell.pack(fill=tk.BOTH, expand=True)

            # buttons bindings
            def __handler(event, x=i, y=j):
                if event.num == 1:
                    self.controller.left_handler(x, y)
                elif event.num == 3:
                    self.controller.right_handler(x, y)
                else:
                    raise Exception('Invalid event code.')

            cell.bind("<Button-1>", __handler)
            cell.bind("<Button-3>", __handler)

            frame.pack_propagate(False)
            frame.grid(row=i, column=j)
            return cell

        self.board = [[create_square(i, j) for j in range(self.model.get_width())]
                      for i in range(self.model.get_height())]
        self.game_frame.pack(padx=10, pady=10, side=tk.BOTTOM)
        return self.board

    # Top frame ####################################################################

    def create_top_frame(self, window):
        """
        Draw the top menu frame

        :param window: Main window to draw upon
        """
        top_frame = tk.Frame(window, borderwidth=2, height=40, relief=tk.GROOVE)
        top_frame.pack(padx=0, pady=0, side=tk.TOP, fill="x")
        for i in range(4):
            top_frame.columnconfigure(i, weight=1)
        self.create_bombs_counter(top_frame)
        self.create_new_game_button(top_frame)
        self.create_undo_frame(top_frame)
        self.create_difficulty_cbox(top_frame)
        self.create_time_counter(top_frame)

    def create_bombs_counter(self, top_frame):
        """
        Draw a frame with bombs counter and a bomb image

        :param top_frame: Frame to draw upon
        """
        bomb_frame = tk.Frame(top_frame, borderwidth=2, height=40, relief=tk.GROOVE)
        bomb_img = tk.Label(bomb_frame, image=self.mine)
        bombs_counter_str = tk.StringVar()

        def _update_bombs_counter():
            """
            Helper function to update bombs counter periodically
            """
            bombs_counter_str.set(self.model.get_bombs_left())
            top_frame.after(100, _update_bombs_counter)

        _update_bombs_counter()

        bombs_counter = tk.Label(bomb_frame, height=1, width=3, bg='white',
                                 textvariable=bombs_counter_str,
                                 font=tkf.Font(weight='bold', size=10))
        bombs_counter.grid(row=0, column=0, padx=2, sticky=tk.W)
        bomb_img.grid(row=0, column=1, padx=2, sticky=tk.E)
        bomb_frame.grid(row=0, column=0, padx=5, sticky=tk.W)

    def create_undo_frame(self, top_frame):
        """
        Draw a frame with undo button and remaining undo counter

        :param top_frame: Frame to draw upon
        """
        undo_remaining_str = tk.StringVar()

        def _update_undo_button():
            if self.model.memento_instances == 0 or self.model.undos_remaining == 0:
                undo_button['state'] = 'disabled'
            else:
                undo_button['state'] = 'normal'
            undo_button.after(100, _update_undo_button)

        def _update_undo_remaining():
            """
            Helper function to update number of undos remaining periodically
            """
            undo_remaining_str.set(self.model.undos_remaining)
            top_frame.after(100, _update_undo_remaining)

        _update_undo_remaining()

        def _undo():
            self.controller.undo_state()

        memento_frame = tk.Frame(top_frame, borderwidth=2, height=40, relief=tk.GROOVE, padx=2)
        undo_button = tk.Button(memento_frame, bd=1, width=5, text="Undo", command=_undo)
        undo_remaining_label = tk.Label(memento_frame, height=1, width=3, bg='white',
                                        textvariable=undo_remaining_str,
                                        font=tkf.Font(weight='bold', size=10))
        _update_undo_button()
        undo_button.grid(row=0, column=0, padx=0)
        undo_remaining_label.grid(row=0, column=1, padx=0)
        memento_frame.grid(row=0, column=1, padx=5)

    def create_new_game_button(self, top_frame):
        """
        Draw a new game button

        :param top_frame: Frame to draw upon
        """

        def _start_new_game():
            self.controller.start_new_game()

        newgame_button = tk.Button(top_frame, bd=1, width=10, text="New game",
                                   command=_start_new_game)
        newgame_button.grid(row=0, column=2, padx=0)

    def create_difficulty_cbox(self, top_frame):
        """
        Draw a difficulty combo box

        :param top_frame: Frame to draw upon
        """

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
        self.difficulty.grid(row=0, column=3, padx=5)
        self.difficulty.bind("<<ComboboxSelected>>", _set_difficulty)

    def create_time_counter(self, top_frame):
        """
        Draw a frame with time counter and an image

        :param top_frame: Frame to draw upon
        """
        time_frame = tk.Frame(top_frame, borderwidth=2, height=40, relief=tk.GROOVE)
        time_counter_str = tk.StringVar()
        time_img = tk.Label(time_frame, image=self.time)

        def _update_time_counter():
            time_counter_str.set(int((time.time() - self.model.get_init_time()) // 1))
            top_frame.after(100, _update_time_counter)

        _update_time_counter()

        time_counter = tk.Label(time_frame, height=1, width=3, bg='white',
                                textvariable=time_counter_str,
                                font=tkf.Font(slant='italic', size=10))
        time_counter.grid(row=0, column=1, padx=2, sticky=tk.W)
        time_img.grid(row=0, column=0, padx=2, sticky=tk.E)
        time_frame.grid(row=0, column=4, padx=5, sticky=tk.E)

    def set_bomb(self, i: int, j: int):
        """
        Set given cell to bomb

        :param i: Height location of the cell
        :param j: Width location of the cell
        """
        self.board[i][j]["bg"] = "#e50000"
        self.board[i][j]["image"] = self.mine
        self.board[i][j]["state"] = "normal"

    def is_empty_image(self, i: int, j: int):
        """
        Checks whether cell has no image

        :param i: Height location of the cell
        :param j: Width location of the cell
        :return: True/False if cell has no image
        """
        return self.board[i][j]["image"] == ""

    def set_clicked(self, i: int, j: int):
        """
        Set cell's button state to clicked

        :param i: Height location of the cell
        :param j: Width location of the cell
        """
        self.board[i][j]["state"] = "disabled"
        self.board[i][j]["relief"] = tk.SUNKEN
        self.board[i][j]["bg"] = "gray80"

    def set_unclicked(self, i: int, j: int):
        """
        Set cell's button state to unclicked

        :param i: Height location of the cell
        :param j: Width location of the cell
        """
        self.board[i][j]["image"] = ""
        self.board[i][j]["text"] = ""
        self.board[i][j]["state"] = tk.DISABLED
        self.board[i][j]["relief"] = tk.RAISED
        self.board[i][j]["bg"] = "SystemButtonFace"

    def set_bomb_text(self, i: int, j: int, text: str, color: str):
        """
        Set the cells text and color

        :param i: Height location of the cell
        :param j: Width location of the cell
        :param text: Text to show on cell
        :param color: String representing the color of text
        """
        self.board[i][j]["text"] = text
        self.board[i][j]["disabledforeground"] = color

    def set_flag(self, i: int, j: int):
        """
        Set cell as flagged

        :param i: Height location of the cell
        :param j: Width location of the cell
        """
        self.board[i][j]["image"] = self.flag
        self.board[i][j]["state"] = "normal"

    def set_disabled(self, i: int, j: int):
        """
        Set cell as disabled

        :param i: Height location of the cell
        :param j: Width location of the cell
        """
        self.board[i][j]["state"] = "disabled"
        self.board[i][j]["image"] = ""

    def reset_board(self, height, width):
        """
        Resets entire board

        :param height: Height of entire board
        :param width: Width of entire board
        """
        for x in range(height):
            for y in range(width):
                self.set_unclicked(x, y)

    def board_to_state(self, state):
        """
        Sets the board to given state

        :param state: State of board to set it to
        """
        for i in range(self.model.get_height()):
            for j in range(self.model.get_width()):
                if not state['grid_state'][i][j]['is_revealed']:
                    self.set_unclicked(i, j)
                if state['grid_state'][i][j]['is_flagged']:
                    self.set_flag(i, j)
                else:
                    self.set_disabled(i, j)

    def set_cbox_value(self, value):
        """
        Set combobox value

        :param value: Value to to it to
        """
        self.difficulty.set(value)
