import random
from dataclasses import dataclass
from itertools import product
from typing import Any

from utils import BoardState


class Grid:
    """ A game grid, containing Cell """

    def __init__(self, width: int, height: int, bombs: int) -> None:
        self.squares_revealed = 0
        self.bombs_left = 0
        self.height = height
        self.width = width
        self.bombs = bombs
        # Instantiate board with number of cells by given height and width
        self.board = [[Cell(i, j) for j in range(self.width)]
                      for i in range(self.height)]
        self.add_bombs()

    def reset(self) -> None:
        """ Reset all squares in grid to default values """
        for line in self.board:
            for cell in line:
                cell.reset()

    def add_bombs(self) -> None:
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
                for (i2, j2) in self.get_neighbours(i, j):
                    self.board[i2][j2].bombs_around += 1

    def get_neighbours(self, i: int, j: int) -> list[tuple[Any, Any]]:
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

    def get_state(self) -> BoardState:
        """
        Returns a nested list representing the current Grid state

        :return: GridState.state -> List[List[dict[str, bool]]]
        """
        return BoardState(
            grid_state=[
                [{'is_revealed': self.board[i][j].is_revealed, 'is_flagged': self.board[i][j].is_flagged} for j in
                 range(self.width)]
                for i in range(self.height)], squares_revealed=self.squares_revealed,
            bombs_left=self.bombs_left)

    def set_state(self, state: BoardState) -> None:
        """
        Set Grid's state by given state

        :param state: BoardState representing the current Grid state
        """
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j].is_revealed = state.grid_state[i][j]['is_revealed']
                self.board[i][j].is_flagged = state.grid_state[i][j]['is_flagged']
        self.bombs_left = state.bombs_left
        self.squares_revealed = state.squares_revealed

    def get_grid_state(self) -> list[list[dict[str, bool]]]:
        """
        Return the current Grid state

        :return: GridState.state -> List[List[dict[str, bool]]]
        """
        return self.get_state().grid_state

    def get_squares_revealed(self) -> int:
        """
        Return the number of squares revealed

        :return: Number of squares revealed
        """
        return sum([sum([1 for cell in line if cell.is_revealed]) for line in self.board])

    def get_bombs_left(self) -> int:
        """
        Return the number of bombs left

        :return: Number of bombs left
        """
        return self.bombs - sum([sum([1 for cell in line if cell.is_flagged]) for line in self.board])


class Cell:
    """ Class representing a square of the game """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.is_bomb = False
        self.is_revealed = False
        self.is_flagged = False
        self.bombs_around = 0

    def reset(self) -> None:
        """ Reset cell to default values """
        self.is_bomb = False
        self.is_revealed = False
        self.bombs_around = 0
        self.is_flagged = False

    def reveal(self) -> tuple[bool, int]:
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
