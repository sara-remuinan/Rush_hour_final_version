from game.display import render_board, render_hand
from game.input_parser import prompt_human_action
from game.rules import apply_action, get_legal_actions, get_winner, is_terminal
from game.setup import create_initial_state


def run_game(seed=None, max_turns=200):
    state = create_initial_state(seed=seed)
    turn = 1

    while not is_terminal(state) and turn <= max_turns:
        print("\n" + "=" * 50)
        print(f"Turn {turn}")
        print(render_board(state))
        print(render_hand(state, state.current_player))

        legal_actions = get_legal_actions(state)
        if not legal_actions:
            print(f"{state.current_player.value} has no legal actions. Turn passes.")
            state.current_player = state.current_player.other()
            turn += 1
            continue

        hand_index, action = prompt_human_action(state, legal_actions)
        apply_action(state, hand_index, action)
        turn += 1

    print("\n" + "=" * 50)
    print(render_board(state))
    winner = get_winner(state)
    if winner is None:
        print("No winner.")
    else:
        print(f"Winner: {winner.value}")
