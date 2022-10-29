import time

from constants import DEFAULT_UNDO_TRIES
from grid import Grid, BoardState
from memento import Originator, Caretaker
from utils import Difficulty


class Model:
    def __init__(self, height: int = 8, width: int = 10, bombs: int = 10) -> None:
        """
        :param height: Height of grid
        :param width: Width of grid
        :param bombs: Amount of bombs in grid
        """
        self.squares_revealed = 0
        self.difficulty = Difficulty.EASY
        self.height = height
        self.width = width
        self.bombs = bombs
        self.bombs_left = bombs
        self.set_parameters(self.difficulty, self.height, self.width, self.bombs)
        self.grid = Grid(self.width, self.height, self.bombs)
        self.init_time = time.time()
        self.originator = Originator()
        self.caretaker = Caretaker(self.originator)
        self.state = BoardState(self.grid.get_grid_state(), 0, bombs)
        self.memento_instances = 0
        self.undos_remaining = DEFAULT_UNDO_TRIES

    def save_state(self) -> None:
        """ Save current state as memento """
        self.state = self.grid.get_state()
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
        self.grid.set_state(self.state)
        self.memento_instances -= 1
        self.undos_remaining -= 1
        return True

    def set_parameters(self, difficulty: Difficulty, *argv) -> bool:
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

    def new_game(self) -> None:
        """ Resets model values and start a new game """
        self.caretaker.clear()
        self.memento_instances = 0
        self.grid.reset()
        self.grid.add_bombs()
        self.set_squares_revealed(0)
        self.set_bombs_left(self.bombs)
        self.undos_remaining = DEFAULT_UNDO_TRIES
        self.set_init_time(time.time())

    def get_grid(self) -> Grid:
        return self.grid

    def get_width(self) -> int:
        return self.grid.width

    def get_height(self) -> int:
        return self.grid.height

    def get_bombs(self) -> int:
        return self.bombs

    def get_bombs_left(self) -> int:
        return self.grid.get_bombs_left()

    def get_init_time(self) -> float:
        return self.init_time

    def get_squares_revealed(self) -> int:
        return self.grid.get_squares_revealed()

    def set_squares_revealed(self, num_squares_revealed: int) -> None:
        self.squares_revealed = num_squares_revealed

    def set_bombs_left(self, num_bombs_left: int) -> bool:
        if num_bombs_left < 0:
            return False
        self.bombs_left = num_bombs_left
        return True

    def set_bombs(self, num_bombs: int) -> bool:
        if num_bombs < 0:
            return False
        self.bombs = num_bombs
        return True

    def set_height(self, height_num: int) -> bool:
        if height_num < 1:
            return False
        self.height = height_num
        return True

    def set_width(self, width_num: int) -> bool:
        if width_num < 1:
            return False
        self.width = width_num
        return True

    def set_init_time(self, set_time: float) -> None:
        self.init_time = set_time

    def update_grid(self) -> None:
        self.grid = Grid(self.width, self.height, self.bombs)

    def is_square_revealed(self, i: int, j: int) -> bool:
        return self.grid.board[i][j].is_revealed

    def get_state(self) -> BoardState:
        return self.state

    def get_undos_remaining(self) -> int:
        return self.undos_remaining

    def get_memento_instances(self) -> int:
        return self.memento_instances
