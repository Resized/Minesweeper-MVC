from utils import BoardState


class Originator:
    """
    The Originator holds some important state that may change over time. It also
    defines a method for saving the state inside a memento and another method
    for restoring the state from it.
    """

    class Memento:
        """
        The Memento class provides a way to retrieve the memento's metadata.
        However, it doesn't expose the Originator's state.
        """

        def __init__(self, state: BoardState) -> None:
            self._state = state

        def get_saved_state(self) -> BoardState:
            return self._state

    _state = None

    def set(self, state: BoardState) -> None:
        self._state = state

    def save_to_memento(self) -> Memento:
        return self.Memento(self._state)

    def restore_from_memento(self, memento: Memento) -> BoardState:
        self._state = memento.get_saved_state()
        return self._state


class Caretaker:
    """
    Caretaker class which calls the save and restore methods of Originator
    And holds the collection of Memento classes
    """

    def __init__(self, originator: Originator) -> None:
        self._history = []
        self._originator = originator

    def backup(self) -> None:
        memento = self._originator.save_to_memento()
        self._history.append(memento)

    def undo(self) -> BoardState:
        try:
            memento = self._history.pop()
        except IndexError as e:
            raise e
        return self._originator.restore_from_memento(memento)

    def clear(self):
        self._history.clear()
