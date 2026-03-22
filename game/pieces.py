from dataclasses import dataclass
from game.constants import CardType, Orientation, Player


@dataclass
class Card:
    card_type: CardType
    value: int = 0

    def __str__(self):
        if self.card_type == CardType.MOVE:
            return f"MOVE {self.value}"
        if self.card_type == CardType.SHIFT:
            sign = "+" if self.value > 0 else ""
            return f"SHIFT {sign}{self.value}"
        return "SLIDE"


@dataclass
class Vehicle:
    vehicle_id: str
    row: int
    col: int
    length: int
    orientation: Orientation
    owner: Player | None = None
    is_hero: bool = False

    def cells(self):
        cells = []
        for i in range(self.length):
            if self.orientation == Orientation.H:
                cells.append((self.row, self.col + i))
            else:
                cells.append((self.row + i, self.col))
        return cells

    def move(self, delta: int):
        if self.orientation == Orientation.H:
            return Vehicle(
                self.vehicle_id,
                self.row,
                self.col + delta,
                self.length,
                self.orientation,
                self.owner,
                self.is_hero,
            )
        return Vehicle(
            self.vehicle_id,
            self.row + delta,
            self.col,
            self.length,
            self.orientation,
            self.owner,
            self.is_hero,
        )

    def shift_cols(self, delta: int):
        return Vehicle(
            self.vehicle_id,
            self.row,
            self.col + delta,
            self.length,
            self.orientation,
            self.owner,
            self.is_hero,
        )
