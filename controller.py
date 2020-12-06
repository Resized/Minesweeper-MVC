import tkinter.simpledialog as tksmpl
import tkinter.dialog as tkdiag
import sys
from model import Model
from view import View
import utils


class Controller:

    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def left_handler(self, i, j, to_save_state=True):
        """
        Called when left click on the (i, j) cell

        :param i: Height location of the cell
        :param j: Width location of the cell
        :param to_save_state: Whether to save current state
        """
        if to_save_state:
            self.model.save_state()
        if self.view.is_empty_image(i, j) and not self.model.grid.board[i][j].is_revealed:
            self.view.set_clicked(i, j)
            is_bomb, bombs_around = self.model.grid.board[i][j].reveal()
            if is_bomb:
                self.view.set_bomb(i, j)
                self.end_game(False)
            else:
                self.model.set_squares_revealed(self.model.get_squares_revealed() + 1)
                if bombs_around != 0:
                    color = utils.colorpicker(bombs_around)
                    text = str(bombs_around)
                    self.view.set_bomb_text(i, j, text, color)
                else:
                    for (x, y) in self.model.get_grid().neighbours(i, j):
                        self.left_handler(x, y, False)
                if self.model.get_squares_revealed() == (
                        self.model.get_width() * self.model.get_height() - self.model.get_bombs()):
                    self.end_game(True)

    def right_handler(self, i: int, j: int):
        """
        Called when right click on the (i, j) cell

        :param i: Height location of the cell
        :param j: Width location of the cell
        """
        if not self.model.is_square_revealed(i, j):
            if self.view.is_empty_image(i, j):
                if self.model.set_bombs_left(self.model.get_bombs_left() - 1):
                    self.view.set_flag(i, j)
                    self.model.grid.board[i][j].is_flagged = True
            else:
                if self.model.set_bombs_left(self.model.get_bombs_left() + 1):
                    self.view.set_disabled(i, j)
                    self.model.grid.board[i][j].is_flagged = False

    def end_game(self, win: bool) -> None:
        """
        Called when end game logic occurred, either win or lose.

        :param win: True = win, False = lose
        """
        if win:
            title = "You won!"
            msg = "Good job. Play again?"
            strings = ('New Game', 'Quit')
            question = tkdiag.Dialog(title=title, text=msg, bitmap="question", strings=strings, default=0)
            ans = strings[question.num]
            if ans == strings[0]:
                self.start_new_game()
            elif ans == strings[1]:
                sys.exit()
        else:
            title = "You lost..."
            if self.model.undos_remaining > 0:
                msg = f"You have {self.model.undos_remaining} undos remaining.\nDo you want to undo last move?"
                strings = ('Undo', 'New Game', 'Quit')
                question = tkdiag.Dialog(title=title, text=msg, bitmap="question", strings=strings, default=0)
                ans = strings[question.num]
                if ans == strings[0]:
                    self.undo_state()
                elif ans == strings[1]:
                    self.start_new_game()
                elif ans == strings[2]:
                    sys.exit()
            else:
                msg = f"You have {self.model.undos_remaining} undos remaining.\nDo you want to play a new game?"
                strings = ('New Game', 'Quit')
                question = tkdiag.Dialog(title=title, text=msg, bitmap="question", strings=strings, default=0)
                ans = strings[question.num]
                if ans == strings[0]:
                    self.start_new_game()
                elif ans == strings[1]:
                    sys.exit()

    def start_new_game(self):
        """
        Helper function that resets the board and model and starts a new game
        """
        self.model.new_game()
        self.view.reset_board(self.model.get_height(), self.model.get_width())

    def undo_state(self):
        """
        Helper function that restores state of model and board to previous one
        """
        if self.model.undo_state():
            self.view.board_to_state(self.model.state)

    def set_difficulty(self, difficulty: utils.Difficulty):
        """
        Difficulty - height, width, bombs
        Easy - 8 10 10
        Medium - 14 18 40
        Hard - 20 24 99

        :param difficulty: Enum representing difficulty (EASY, MEDIUM, HARD, CUSTOM)
        :type difficulty: Difficulty
        """
        if difficulty == utils.Difficulty.CUSTOM:
            title = "Enter custom values (5-50)"
            while True:
                prompt = "Height:"
                height = tksmpl.askinteger(title, prompt, minvalue=5, maxvalue=50)
                if height is None:
                    self.view.set_cbox_value(utils.Difficulty.DEFAULT.value)
                    self.set_difficulty(utils.Difficulty.DEFAULT)
                    return
                prompt = "Width:"
                width = tksmpl.askinteger(title, prompt, minvalue=5, maxvalue=50)
                if width is None:
                    self.view.set_cbox_value(utils.Difficulty.DEFAULT.value)
                    self.set_difficulty(utils.Difficulty.DEFAULT)
                    return
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
        self.model.new_game()
