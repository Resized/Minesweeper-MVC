# Minesweeper

This is a Minesweeper game implemented using Python and the Tkinter library. The game features a graphical user interface (GUI) that allows players to interact with the game board and uncover cells to avoid mines.

![alt-text](https://github.com/Resized/Minesweeper-MVC/blob/master/images/example.png)

## Installation

1. Clone the repository to your local machine.
2. Ensure you have Python 3 installed.
3. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

## Usage

To start the game, run the `main.py` script:

```
python main.py
```

The game window will open, displaying the Minesweeper board. You can left-click on a cell to uncover it and right-click to flag it as a potential mine. The objective is to uncover all cells that do not contain mines without triggering any mines.

The top menu bar provides additional functionality:

- **New Game**: Starts a new game with the current difficulty level.
- **Undo**: Undoes the last move made, restoring the board to its previous state.
- **Difficulty**: Allows you to change the difficulty level of the game.

## Files

The project consists of the following files:

- `main.py`: The entry point of the application. It initializes the model, view, and controller, and creates the main GUI window.
- `model.py`: Contains the `Model` class, which represents the game state and logic. It manages the grid, bombs, game parameters, and undo functionality.
- `view.py`: Contains the `View` class, which handles the graphical representation of the game. It creates the main window, game board, and top menu bar.
- `controller.py`: Contains the `Controller` class, which acts as an intermediary between the model and view. It handles user interactions and updates the model and view accordingly.
- `utils.py`: Provides utility functions and enums used throughout the project.
- `images/`: A directory containing the image assets used in the GUI.
