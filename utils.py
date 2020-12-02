from enum import Enum


def colorpicker(bombs_around):
    """ Set correct cell text color by number of bombs around """
    text_color = ""
    if bombs_around == 1:
        text_color = "blue"
    elif bombs_around == 2:
        text_color = "green"
    elif bombs_around == 3:
        text_color = "red"
    elif bombs_around == 4:
        text_color = "navy"
    elif bombs_around == 5:
        text_color = "orangered4"
    elif bombs_around == 6:
        text_color = "turquoise"
    elif bombs_around == 7:
        text_color = "black"
    elif bombs_around == 8:
        text_color = "snow4"
    return text_color


class Difficulty(Enum):
    """ Enum representing game difficulties """
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'
    CUSTOM = 'Custom'
    DEFAULT = EASY


def str_to_difficulty_enum(difficulty_str: str) -> Difficulty:
    """ Helper function to convert from difficulty string to difficulty enum """
    for difficulty in Difficulty:
        if difficulty.value == difficulty_str:
            return difficulty


def difficulty_list():
    lst = []
    for difficulty in Difficulty:
        lst.append(difficulty.value)
    return lst
