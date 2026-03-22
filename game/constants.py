from enum import Enum

BOARD_COLS = 8
BOARD_ROWS = 14
HAND_SIZE = 3


class Player(Enum):
    GOLD = "Gold"
    SILVER = "Silver"

    def other(self):
        return Player.SILVER if self == Player.GOLD else Player.GOLD


class Orientation(Enum):
    H = "H"
    V = "V"


class Section(Enum):
    TOP = "TOP"
    BOTTOM = "BOTTOM"


class CardType(Enum):
    MOVE = "move"
    SHIFT = "shift"
    SLIDE = "slide"
