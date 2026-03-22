"""
game/ai.py
==========
Simple AI for the Rush Hour Shift game.
It uses Minimax with Alpha-Beta pruning.
The code is kept intentionally simple.
"""

import copy
import math
from game.constants import BOARD_ROWS, Player
from game.rules import apply_action, get_legal_actions, get_winner, is_terminal


# ---------------------------------------------------------------------------
# Heuristic Evaluation
# ---------------------------------------------------------------------------


def evaluate_state(state, ai_player):
    """
    Returns a score for the state from the AI player's point of view.
    Higher score = better for the AI.
    """
    if is_terminal(state):
        winner = get_winner(state)
        if winner == ai_player:
            return 10000
        if winner is None:
            return 0
        return -10000

    opponent = ai_player.other()

    ai_hero = state.get_vehicle("G") if ai_player == Player.GOLD else state.get_vehicle("S")
    opp_hero = state.get_vehicle("S") if ai_player == Player.GOLD else state.get_vehicle("G")

    ai_distance = hero_distance_to_exit(ai_hero, ai_player)
    opp_distance = hero_distance_to_exit(opp_hero, opponent)

    ai_blockers = count_blockers(state, ai_player)
    opp_blockers = count_blockers(state, opponent)

    # Small bonus if the AI has more options on its next turn.
    ai_moves = count_actions_for_player(state, ai_player)
    opp_moves = count_actions_for_player(state, opponent)

    score = 0
    score += 15 * (opp_distance - ai_distance)
    score += 6 * (opp_blockers - ai_blockers)
    score += 2 * (ai_moves - opp_moves)

    return score



def hero_distance_to_exit(hero, player):
    """
    Number of rows the hero still needs to move to leave the board.
    Smaller is better.
    """
    if hero is None:
        return BOARD_ROWS

    rows = [row for row, _ in hero.cells()]

    if player == Player.GOLD:
        bottom_row = max(rows)
        return (BOARD_ROWS - 1) - bottom_row
    else:
        top_row = min(rows)
        return top_row



def count_blockers(state, player):
    """
    Counts how many vehicles are in the hero car's way.
    This is simple and only checks the hero column toward the exit.
    """
    hero = state.get_vehicle("G") if player == Player.GOLD else state.get_vehicle("S")
    if hero is None:
        return 0

    hero_cells = hero.cells()
    hero_col = hero.col
    count = 0

    if player == Player.GOLD:
        hero_bottom = max(row for row, _ in hero_cells)
        for vehicle in state.vehicles:
            if vehicle.vehicle_id == hero.vehicle_id:
                continue
            for row, col in vehicle.cells():
                if col == hero_col and row > hero_bottom:
                    count += 1
                    break
    else:
        hero_top = min(row for row, _ in hero_cells)
        for vehicle in state.vehicles:
            if vehicle.vehicle_id == hero.vehicle_id:
                continue
            for row, col in vehicle.cells():
                if col == hero_col and row < hero_top:
                    count += 1
                    break

    return count



def count_actions_for_player(state, player):
    """
    Rough mobility measure: how many legal actions that player would have.
    """
    temp_state = copy.deepcopy(state)
    temp_state.current_player = player
    return len(get_legal_actions(temp_state))


# ---------------------------------------------------------------------------
# Minimax with Alpha-Beta Pruning
# ---------------------------------------------------------------------------


def minimax(state, depth, alpha, beta, ai_player):
    if depth == 0 or is_terminal(state):
        return evaluate_state(state, ai_player)

    legal_actions = get_legal_actions(state)
    if not legal_actions:
        return evaluate_state(state, ai_player)

    if state.current_player == ai_player:
        best_value = -math.inf
        for hand_index, action in legal_actions:
            next_state = copy.deepcopy(state)
            apply_action(next_state, hand_index, action)
            value = minimax(next_state, depth - 1, alpha, beta, ai_player)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    else:
        best_value = math.inf
        for hand_index, action in legal_actions:
            next_state = copy.deepcopy(state)
            apply_action(next_state, hand_index, action)
            value = minimax(next_state, depth - 1, alpha, beta, ai_player)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value


# ---------------------------------------------------------------------------
# Public Function
# ---------------------------------------------------------------------------


def get_best_action(state, legal_actions=None, depth=2):
    """
    Returns the best legal action for the current player.
    """
    if legal_actions is None:
        legal_actions = get_legal_actions(state)

    if not legal_actions:
        return None

    ai_player = state.current_player
    best_action = legal_actions[0]
    best_value = -math.inf

    for hand_index, action in legal_actions:
        next_state = copy.deepcopy(state)
        apply_action(next_state, hand_index, action)
        value = minimax(next_state, depth - 1, -math.inf, math.inf, ai_player)

        if value > best_value:
            best_value = value
            best_action = (hand_index, action)

    return best_action
