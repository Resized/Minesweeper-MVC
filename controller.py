import tkinter.messagebox as tkmsg
import tkinter.simpledialog as tksmpl
import sys
import time

from model import Model
from view import View
import utils


# Event handlers ###############################################################


class Controller:

    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def left_handler(self, i, j):
        """ Called when left click on the (i, j) cell """
        if self.view.is_empty_image(i, j) and not self.model.grid.board[i][j].revealed:
            self.view.set_clicked(i, j)
            if self.model.grid.board[i][j].is_bomb:
                self.view.set_bomb(i, j)
                self.end_game(False)
            else:
                self.model.grid.board[i][j].revealed = True
                self.model.set_squares_revealed(self.model.get_squares_revealed() + 1)
                if self.model.grid.board[i][j].bombs_around != 0:
                    color = utils.colorpicker(self.model.grid.board[i][j].bombs_around)
                    text = self.model.grid.board[i][j].bombs_around
                    self.view.set_bomb_text(i, j, text, color)
                else:
                    for (x, y) in self.model.get_grid().neighbours(i, j):
                        self.left_handler(x, y)
                if self.model.get_squares_revealed() == (
                        self.model.get_width() * self.model.get_height() - self.model.get_bombs()):
                    self.end_game(True)

    def right_handler(self, i, j):
        """ Called when right click on the (i, j) cell """
        if not self.model.is_square_revealed(i, j):
            if self.view.is_empty_image(i, j):
                self.view.set_flag(i, j)
                self.model.set_bombs_left(self.model.get_bombs_left() - 1)
            else:
                self.view.set_disabled(i, j)
                self.model.set_bombs_left(self.model.get_bombs_left() + 1)

    def end_game(self, win):
        if win:
            title = "You won!"
            msg = "Good job. Play again?"
        else:
            title = "You lost..."
            msg = "Try again?"
        ans = tkmsg.askyesno(title, msg)
        if ans:
            self.start_new_game()
        else:
            sys.exit()

    def start_new_game(self):
        self.model.grid.reset()
        self.view.reset_board(self.model.get_height(), self.model.get_width())
        self.model.grid.add_bombs()
        self.model.set_squares_revealed(0)
        self.model.set_bombs_left(self.model.get_bombs())
        self.model.set_init_time(time.time())

    def set_difficulty(self, difficulty: utils.Difficulty):
        """
        Difficulty - height, width, bombs
        Easy - 8 10 10
        Medium - 14 18 40
        Hard - 20 24 99
        """
        if difficulty == utils.Difficulty.CUSTOM:
            while True:
                title = "Enter custom values"
                prompt = "Height:"
                height = tksmpl.askinteger(title, prompt, minvalue=5, maxvalue=50)
                if height is None:
                    self.view.set_cbox_value(utils.Difficulty.DEFAULT.value)
                    self.set_difficulty(utils.Difficulty.DEFAULT)
                    return
                title = "Enter custom values"
                prompt = "Width:"
                width = tksmpl.askinteger(title, prompt, minvalue=5, maxvalue=50)
                if width is None:
                    self.view.set_cbox_value(utils.Difficulty.DEFAULT.value)
                    self.set_difficulty(utils.Difficulty.DEFAULT)
                    return
                title = "Enter custom values"
                prompt = "Bombs:"
                bombs = tksmpl.askinteger(title, prompt)
                if bombs is None:
                    self.view.set_cbox_value(utils.Difficulty.DEFAULT.value)
                    self.set_difficulty(utils.Difficulty.DEFAULT)
                    return
                if self.model.set_parameters(utils.Difficulty.CUSTOM, height, width, bombs):
                    break
        self.model.set_parameters(difficulty)
        self.model.update_grid()
