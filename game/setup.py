import random
from game.constants import CardType, Orientation, Player
from game.pieces import Card, Vehicle
from game.state import GameState


def make_deck():
    deck = []
    for _ in range(6):
        deck.append(Card(CardType.MOVE, 1))
        deck.append(Card(CardType.MOVE, 2))
        deck.append(Card(CardType.MOVE, 3))
    for _ in range(5):
        deck.append(Card(CardType.SHIFT, 1))
        deck.append(Card(CardType.SHIFT, -1))
    for _ in range(6):
        deck.append(Card(CardType.SLIDE, 0))
    random.shuffle(deck)
    return deck


def create_initial_state(seed=None):
    if seed is not None:
        random.seed(seed)

    vehicles = [
        Vehicle("G", 11, 3, 2, Orientation.V, Player.GOLD, True),
        Vehicle("S", 1, 4, 2, Orientation.V, Player.SILVER, True),
        Vehicle("A", 0, 1, 2, Orientation.H),
        Vehicle("B", 2, 2, 3, Orientation.H),
        Vehicle("C", 3, 6, 2, Orientation.V),
        Vehicle("D", 5, 1, 2, Orientation.H),
        Vehicle("E", 7, 3, 3, Orientation.H),
        Vehicle("F", 8, 6, 2, Orientation.V),
        Vehicle("H", 9, 2, 2, Orientation.H),
        Vehicle("I", 10, 5, 3, Orientation.V),
        Vehicle("J", 12, 1, 3, Orientation.H),
    ]

    deck = make_deck()
    hands = {
        Player.GOLD: [deck.pop(0), deck.pop(0), deck.pop(0)],
        Player.SILVER: [deck.pop(0), deck.pop(0), deck.pop(0)],
    }

    return GameState(
        vehicles=vehicles,
        deck=deck,
        discard=[],
        hands=hands,
        current_player=Player.GOLD,
    )
