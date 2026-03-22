from game.constants import BOARD_COLS, BOARD_ROWS, Player, Section


MIDDLE_ROWS = {5, 6, 7, 8}
END_BASE_COLS = [1, 2, 3, 4, 5, 6]


def section_rows(state, section):
    if section == Section.TOP:
        return [0, 1, 2, 3, 4]
    return [9, 10, 11, 12, 13]


def section_cols(state, section):
    if section == Section.TOP:
        offset = state.top_offset
    else:
        offset = state.bottom_offset
    return [c + offset for c in END_BASE_COLS]


def valid_cell(state, row, col):
    if not (0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS):
        return False

    if row in MIDDLE_ROWS:
        return col in END_BASE_COLS

    if row in section_rows(state, Section.TOP):
        return col in section_cols(state, Section.TOP)

    if row in section_rows(state, Section.BOTTOM):
        return col in section_cols(state, Section.BOTTOM)

    return False


def render_board(state):
    grid = []
    for r in range(BOARD_ROWS):
        line = []
        for c in range(BOARD_COLS):
            if valid_cell(state, r, c):
                line.append(".")
            else:
                line.append(" ")
        grid.append(line)

    for vehicle in state.vehicles:
        for row, col in vehicle.cells():
            if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
                grid[row][col] = vehicle.vehicle_id

    lines = []
    lines.append(f"Current player: {state.current_player.value}")
    lines.append(f"Top shift: {state.top_offset} | Bottom shift: {state.bottom_offset}")
    lines.append("    0 1 2 3 4 5 6 7")
    for r in range(BOARD_ROWS):
        line = str(r).rjust(2) + "  "
        line += " ".join(grid[r])
        lines.append(line)
    lines.append("Top and bottom sections slide left/right. Gold exits at the bottom. Silver exits at the top.")
    return "\n".join(lines)


def render_hand(state, player):
    lines = [f"{player.value} hand:"]
    for i, card in enumerate(state.hands[player]):
        lines.append(f"  {i}: {card}")
    return "\n".join(lines)
