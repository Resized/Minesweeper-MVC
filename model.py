from itertools import product
import random
import time
from constants import DEFAULT_UNDO_TRIES
from memento import Originator, Caretaker
from utils import Difficulty


class Model:
    def __init__(self, height=8, width=10, bombs=10):
        """
        :param height: Height of grid
        :param width: Width of grid
        :param bombs: Amount of bombs in grid
        """
        self.difficulty = Difficulty.EASY
        self.height = height
        self.width = width
        self.bombs = bombs
        self.bombs_left = bombs
        self.set_parameters(self.difficulty, self.height, self.width, self.bombs)
        self.grid = Grid(self.width, self.height, self.bombs)
        self.squares_revealed = 0
        self.init_time = time.time()
        self.originator = Originator()
        self.caretaker = Caretaker(self.originator)
        self.state = dict()
        self.memento_instances = 0
        self.undos_remaining = DEFAULT_UNDO_TRIES

    def save_state(self):
        """ Save current state as memento """
        self.state = {'squares_revealed': self.squares_revealed,
                      'grid_state': self.grid.get_state(),
                      'bombs_left': self.bombs_left}
        self.originator.set(self.state)
        self.caretaker.backup()
        self.memento_instances += 1

    def undo_state(self) -> bool:
        """
        Undo state to previous one

        :return: True/False whether undo was successful
        """
        if self.undos_remaining == 0:
            return False
        try:
            self.state = self.caretaker.undo()
        except IndexError:
            print('No memento to undo')
            return False
        self.squares_revealed = self.state['squares_revealed']
        self.bombs_left = self.state['bombs_left']
        self.grid.set_state(self.state['grid_state'])
        self.memento_instances -= 1
        self.undos_remaining -= 1
        return True

    def set_parameters(self, difficulty: Difficulty, *argv):
        """
        set parameters height, width, bombs

        :param difficulty: Enum of Difficulty
        :param argv: height, width, bombs to set values at
        :return: True/False whether parameters were set successfully
        """

        if len(argv) != 3 and len(argv) != 0:
            print("Warning : Invalid parameters")
            print("Need 4 arguments (difficulty, height, width, bombs) or 1 argument (difficulty)")
            return False

        if len(argv) == 0:
            # Only difficulty given
            if difficulty == Difficulty.EASY:
                self.difficulty = Difficulty.EASY
                return self.set_parameters(Difficulty.EASY, 8, 10, 10)

            elif difficulty == Difficulty.MEDIUM:
                self.difficulty = Difficulty.MEDIUM
                return self.set_parameters(Difficulty.MEDIUM, 14, 18, 40)

            elif difficulty == Difficulty.HARD:
                self.difficulty = Difficulty.HARD
                return self.set_parameters(Difficulty.HARD, 20, 24, 99)
            else:
                return False

        # if they aren't ints
        try:
            height = int(argv[0])
            width = int(argv[1])
            bombs = int(argv[2])
        except ValueError:
            print("Warning : Invalid parameters")
            print("Arguments aren't ints")
            return False

        # if constraints aren't respected
        if height <= 0 or width <= 0 or bombs <= 0 or bombs >= height * width:
            print("Warning : Invalid parameters")
            print("Can't create game with these values")
            return False

        self.height = height
        self.width = width
        self.bombs = bombs
        self.bombs_left = bombs
        self.difficulty = difficulty
        return True

    def new_game(self):
        """ Resets model values and start a new game """
        self.caretaker.clear()
        self.memento_instances = 0
        self.grid.reset()
        self.grid.add_bombs()
        self.set_squares_revealed(0)
        self.set_bombs_left(self.bombs)
        self.undos_remaining = DEFAULT_UNDO_TRIES
        self.set_init_time(time.time())

    def get_grid(self):
        return self.grid

    def get_squares_revealed(self):
        return self.squares_revealed

    def get_width(self):
        return self.grid.width

    def get_height(self):
        return self.grid.height

    def get_bombs(self):
        return self.bombs

    def get_bombs_left(self):
        return self.bombs_left

    def get_init_time(self):
        return self.init_time

    def set_squares_revealed(self, num_squares_revealed):
        self.squares_revealed = num_squares_revealed

    def set_bombs_left(self, num_bombs_left):
        if num_bombs_left < 0:
            return False
        self.bombs_left = num_bombs_left
        return True

    def set_bombs(self, num_bombs):
        self.bombs = num_bombs

    def set_height(self, height_num):
        self.height = height_num

    def set_width(self, width_num):
        self.width = width_num

    def set_init_time(self, set_time):
        self.init_time = set_time

    def update_grid(self):
        self.grid = Grid(self.width, self.height, self.bombs)

    def is_square_revealed(self, i, j):
        return self.grid.board[i][j].is_revealed


class Grid:
    """ A game grid, containing Cell """

    def __init__(self, width: int, height: int, bombs: int):
        self.height = height
        self.width = width
        self.bombs = bombs
        # Instantiate board with number of cells by given height and width
        self.board = [[Cell(i, j) for j in range(self.width)]
                      for i in range(self.height)]
        self.add_bombs()

    def reset(self):
        """ Reset all squares in grid to default values """
        for line in self.board:
            for cell in line:
                cell.reset()

    def add_bombs(self):
        """ Fill board squares with bombs """
        if self.bombs <= 0 or self.bombs >= self.height * self.width:
            raise Exception("Invalid number of bombs.")
        else:
            # sample makes random choices with distinct elements
            # we don't want several bombs on the same square
            pos = random.sample([(i, j) for j in range(self.width)
                                 for i in range(self.height)], self.bombs)
            for (i, j) in pos:
                self.board[i][j].is_bomb = True
                for (i2, j2) in self.neighbours(i, j):
                    self.board[i2][j2].bombs_around += 1

    def neighbours(self, i, j):
        """
        Return the list of coordinates of the neighbours of the (i, j) cell

        :param i: Height location of the cell
        :param j: Width location of the cell
        :return: List of neighbouring cells
        """
        lst = []
        iterlist = [[i - 1, i, i + 1], [j - 1, j, j + 1]]
        for (x, y) in product(*iterlist):
            if x in range(self.height) and y in range(self.width) and (x, y) is not (i, j):
                lst.append((x, y))
        return lst

    def get_state(self):
        """
        Returns a nested list representing the current Grid state

        :return: state -> List[List[dict[str, bool]]]
        """
        state = [[{'is_revealed': self.board[i][j].is_revealed, 'is_flagged': self.board[i][j].is_flagged} for j in
                  range(self.width)]
                 for i in range(self.height)]
        return state

    def set_state(self, state):
        """
        Set Grid's state by given state

        :param state: List[List[dict[str, bool]]] representing the current Grid state
        """
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j].is_revealed = state[i][j]['is_revealed']
                self.board[i][j].is_flagged = state[i][j]['is_flagged']


class Cell:
    """ Class representing a square of the game """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_bomb = False
        self.is_revealed = False
        self.is_flagged = False
        self.bombs_around = 0

    def reset(self):
        """ Reset cell to default values """
        self.is_bomb = False
        self.is_revealed = False
        self.bombs_around = 0
        self.is_flagged = False

    def reveal(self):
        """
        Set cell logic to be revealed
        :return: Tuple of is_bomb and bombs_around values
        """
        self.is_revealed = True
        return self.is_bomb, self.bombs_around

        #   -------->
        # |         y
        # |
        # V x
