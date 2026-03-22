from game.actions import MoveAction, ShiftAction, SlideAction
from game.constants import Section


def prompt_human_action(state, legal_actions):
    while True:
        print("Choose one action by typing its number:")
        for i, (hand_index, action) in enumerate(legal_actions):
            if isinstance(action, MoveAction):
                text = f"play card {hand_index}: move {action.vehicle_id} by {action.delta}"
            elif isinstance(action, ShiftAction):
                text = f"play card {hand_index}: shift {action.section.value} by {action.delta}"
            elif isinstance(action, SlideAction):
                direction = "forward/right/down" if action.direction == 1 else "backward/left/up"
                text = f"play card {hand_index}: slide {action.vehicle_id} {direction}"
            else:
                text = str(action)
            print(f"  {i}: {text}")

        raw = input("> ").strip()
        if raw.isdigit():
            choice = int(raw)
            if 0 <= choice < len(legal_actions):
                return legal_actions[choice]
        print("Invalid choice. Try again.")
