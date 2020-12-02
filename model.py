from itertools import product
import random
import time

from utils import Difficulty


class Model:
    def __init__(self, height=8, width=10, bombs=10):
        self.difficulty = Difficulty.EASY
        self.height = height
        self.width = width
        self.bombs = bombs
        self.bombs_left = bombs
        self.set_parameters(self.difficulty, self.height, self.width, self.bombs)
        self.grid = Grid(self.width, self.height, self.bombs)
        self.squares_revealed = 0
        self.init_time = time.time()

    def set_memento(self, memento):
        previous_state = pickle.loads(memento)
        print(previous_state)
        vars(self).clear()
        vars(self).update(previous_state)

    def create_memento(self):
        return pickle.dumps(vars(self))

    def set_parameters(self, difficulty: Difficulty, *argv):
        """ set parameters height, width, bombs """

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
        self.bombs_left = num_bombs_left

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
        return self.grid.board[i][j].revealed


class Grid:
    """ A game grid, containing Squares """

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
            for sq in line:
                sq.reset()

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
        """ Return the list of coordinates of the neighbours of the (i, j) cell """
        lst = []
        iterlist = [[i - 1, i, i + 1], [j - 1, j, j + 1]]
        for (x, y) in product(*iterlist):
            if x in range(self.height) and y in range(self.width) and (x, y) is not (i, j):
                lst.append((x, y))
        return lst


class Cell:
    """ A square of the game """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reset()

    def reset(self):
        self.is_bomb = False
        self.revealed = False
        self.bombs_around = 0

    def reveal(self):
        self.revealed = True
        return self.is_bomb, self.bombs_around

        #   -------->
        # |         y
        # |
        # V x
