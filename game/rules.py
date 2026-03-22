from game.actions import MoveAction, ShiftAction, SlideAction
from game.constants import BOARD_COLS, BOARD_ROWS, CardType, Player, Section
from game.display import section_rows, valid_cell


MIDDLE_ROWS = {5, 6, 7, 8}


def occupied_cells(state, exclude_id=None):
    cells = set()
    for vehicle in state.vehicles:
        if vehicle.vehicle_id == exclude_id:
            continue
        for cell in vehicle.cells():
            cells.add(cell)
    return cells


def is_terminal(state):
    return state.winner is not None


def get_winner(state):
    return state.winner


def can_place(state, vehicle, occupied):
    for row, col in vehicle.cells():
        if (row, col) in occupied:
            return False
        if not (0 <= col < BOARD_COLS):
            return False
        if vehicle.is_hero and vehicle.owner == Player.GOLD and row >= BOARD_ROWS:
            continue
        if vehicle.is_hero and vehicle.owner == Player.SILVER and row < 0:
            continue
        if not valid_cell(state, row, col):
            return False
    return True


def get_legal_moves_for_vehicle(state, vehicle_id, budget):
    vehicle = state.get_vehicle(vehicle_id)
    if vehicle is None:
        return []

    occupied = occupied_cells(state, exclude_id=vehicle_id)
    legal = []
    for direction in (-1, 1):
        for steps in range(1, budget + 1):
            delta = direction * steps
            candidate = vehicle.move(delta)
            if not can_place(state, candidate, occupied):
                break
            legal.append(delta)
    return legal


def get_slide_delta(state, vehicle_id, direction):
    vehicle = state.get_vehicle(vehicle_id)
    if vehicle is None:
        return 0
    occupied = occupied_cells(state, exclude_id=vehicle_id)
    best = 0
    for steps in range(1, BOARD_ROWS + BOARD_COLS + 1):
        delta = direction * steps
        candidate = vehicle.move(delta)
        if not can_place(state, candidate, occupied):
            break
        best = delta
    return best


def vehicles_in_section_only(state, section):
    rows = set(section_rows(state, section))
    result = []
    for vehicle in state.vehicles:
        vehicle_rows = {r for r, _ in vehicle.cells()}
        if vehicle_rows & rows and not (vehicle_rows & MIDDLE_ROWS):
            result.append(vehicle)
    return result


def shift_is_legal(state, section, delta):
    current = state.current_offset(section)
    new_offset = current + delta
    if new_offset < -1 or new_offset > 1:
        return False

    moved = vehicles_in_section_only(state, section)
    occupied = occupied_cells(state)
    for vehicle in moved:
        for cell in vehicle.cells():
            occupied.discard(cell)

    old_offset = state.current_offset(section)
    state.set_offset(section, new_offset)
    try:
        for vehicle in moved:
            shifted = vehicle.shift_cols(delta)
            if not can_place(state, shifted, occupied):
                return False
    finally:
        state.set_offset(section, old_offset)
    return True


def get_legal_actions(state):
    actions = []
    hand = state.hands[state.current_player]
    for index, card in enumerate(hand):
        if card.card_type == CardType.MOVE:
            for vehicle in state.vehicles:
                for delta in get_legal_moves_for_vehicle(state, vehicle.vehicle_id, card.value):
                    if abs(delta) == card.value:
                        actions.append((index, MoveAction(card, vehicle.vehicle_id, delta)))
        elif card.card_type == CardType.SHIFT:
            for section in (Section.TOP, Section.BOTTOM):
                if shift_is_legal(state, section, card.value):
                    actions.append((index, ShiftAction(card, section, card.value)))
        elif card.card_type == CardType.SLIDE:
            for vehicle in state.vehicles:
                for direction in (-1, 1):
                    if get_slide_delta(state, vehicle.vehicle_id, direction) != 0:
                        actions.append((index, SlideAction(card, vehicle.vehicle_id, direction)))
    return actions


def apply_action(state, hand_index, action):
    played_card = state.remove_card_from_hand(state.current_player, hand_index)
    state.discard.append(played_card)

    if isinstance(action, MoveAction):
        vehicle = state.get_vehicle(action.vehicle_id)
        if vehicle is not None:
            state.replace_vehicle(vehicle, vehicle.move(action.delta))

    elif isinstance(action, ShiftAction):
        current = state.current_offset(action.section)
        state.set_offset(action.section, current + action.delta)
        for vehicle in vehicles_in_section_only(state, action.section):
            state.replace_vehicle(vehicle, vehicle.shift_cols(action.delta))

    elif isinstance(action, SlideAction):
        delta = get_slide_delta(state, action.vehicle_id, action.direction)
        vehicle = state.get_vehicle(action.vehicle_id)
        if vehicle is not None and delta != 0:
            state.replace_vehicle(vehicle, vehicle.move(delta))

    check_winner(state)
    if not is_terminal(state):
        state.draw_card(state.current_player)
        state.current_player = state.current_player.other()


def check_winner(state):
    for vehicle in state.vehicles:
        if vehicle.is_hero and vehicle.owner == Player.GOLD:
            if all(row >= BOARD_ROWS for row, _ in vehicle.cells()):
                state.winner = Player.GOLD
        if vehicle.is_hero and vehicle.owner == Player.SILVER:
            if all(row < 0 for row, _ in vehicle.cells()):
                state.winner = Player.SILVER
