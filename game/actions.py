from dataclasses import dataclass
from game.constants import Section
from game.pieces import Card


@dataclass
class MoveAction:
    card: Card
    vehicle_id: str
    delta: int


@dataclass
class ShiftAction:
    card: Card
    section: Section
    delta: int


@dataclass
class SlideAction:
    card: Card
    vehicle_id: str
    direction: int
