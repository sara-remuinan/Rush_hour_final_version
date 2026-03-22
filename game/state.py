from dataclasses import dataclass, field
from game.constants import HAND_SIZE, Player, Section
from game.pieces import Card, Vehicle


@dataclass
class GameState:
    vehicles: list[Vehicle]
    deck: list[Card]
    discard: list[Card]
    hands: dict[Player, list[Card]]
    current_player: Player
    top_offset: int = 0
    bottom_offset: int = 0
    winner: Player | None = None

    def get_vehicle(self, vehicle_id: str):
        for vehicle in self.vehicles:
            if vehicle.vehicle_id == vehicle_id:
                return vehicle
        return None

    def replace_vehicle(self, old_vehicle: Vehicle, new_vehicle: Vehicle):
        new_list = []
        for vehicle in self.vehicles:
            if vehicle.vehicle_id == old_vehicle.vehicle_id:
                new_list.append(new_vehicle)
            else:
                new_list.append(vehicle)
        self.vehicles = new_list

    def remove_card_from_hand(self, player: Player, index: int):
        return self.hands[player].pop(index)

    def draw_card(self, player: Player):
        if not self.deck:
            self.deck = self.discard[:]
            self.discard = []
        if self.deck and len(self.hands[player]) < HAND_SIZE:
            self.hands[player].append(self.deck.pop(0))

    def current_offset(self, section: Section):
        if section == Section.TOP:
            return self.top_offset
        return self.bottom_offset

    def set_offset(self, section: Section, value: int):
        if section == Section.TOP:
            self.top_offset = value
        else:
            self.bottom_offset = value
