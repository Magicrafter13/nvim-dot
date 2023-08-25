#!/usr/bin/python3
"""..."""

import curses
import json


def draw_single_selection_menu(stdscr, things, title):
    """..."""
    highlighted_row = 0
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        stdscr.addstr(height // 2 - len(things.keys()) - 1, width // 2 - len(title) // 2, title)  # noqa: E501  pylint: disable=line-too-long
        for idx, option in enumerate(things.keys()):
            _x = width // 2 - len(option) // 2
            _y = height // 2 - len(things.keys()) - 1 + (idx + 1) * 2

            if idx == highlighted_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(_y, _x, option)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(_y, _x, option)

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and highlighted_row > 0:
            highlighted_row -= 1
        elif key == curses.KEY_DOWN and highlighted_row < len(things.keys()) - 1:  # noqa: E501
            highlighted_row += 1
        elif key == ord('\n') or key == ord(' '):
            break

    return (highlighted_row, list(things.keys())[highlighted_row])


def draw_checkbox_menu(stdscr, things, title):
    """..."""
    highlighted_row = 0
    selected_rows = set()
    while True:
        stdscr.clear()

        height, width = stdscr.getmaxyx()

        stdscr.addstr(height // 2 - len(things.keys()) - 1, width // 2 - len(title) // 2, title)  # noqa: E501  pylint: disable=line-too-long
        for idx, option in enumerate(things.keys()):
            _x = width // 2 - (len(option) + 4) // 2
            _y = height // 2 - len(things.keys()) - 1 + (idx + 1) * 2

            option_text = f"{'[X] ' if idx in selected_rows else '[ ] '}{option}"  # noqa: E501

            if idx == highlighted_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(_y, _x, option_text)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(_y, _x, option_text)

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and highlighted_row > 0:
            highlighted_row -= 1
        elif key == curses.KEY_DOWN and highlighted_row < len(things.keys()) - 1:  # noqa: E501
            highlighted_row += 1
        elif key == ord(' '):
            if highlighted_row in selected_rows:
                selected_rows.remove(highlighted_row)
            else:
                selected_rows.add(highlighted_row)
        elif key == ord('\n'):
            break
        elif key == ord('a'):
            selected_rows.update(range(len(things.keys())))

    return [(idx, list(things.keys())[idx]) for idx in selected_rows]


def main(stdscr):
    """..."""

    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()      # Clear the screen

    #
    # [System]
    #

    base = ""
    with open("configs/base.json", "r", encoding='UTF-8') as _f:
        _, base = draw_single_selection_menu(
            stdscr,
            json.loads(_f.read()),
            "=== Select System Base ===")
    # stdscr.addstr(0, 0, f"Base selected: {base}")
    # stdscr.getch()

    envs = []
    with open("configs/env.json", "r", encoding='UTF-8') as _f:
        envs = [token for idx, token in draw_checkbox_menu(
            stdscr,
            json.loads(_f.read()),
            "=== Select Environments ===")]
    # stdscr.addstr(0, 0, f"Envs selected: {envs}")
    # stdscr.getch()

    #
    # [Additional]
    #

    yes = []
    with open("configs/yes.json", "r", encoding='UTF-8') as _f:
        yes = [token for idx, token in draw_checkbox_menu(
            stdscr,
            json.loads(_f.read()),
            "=== Select Feature-sets to Enable ===")]
    # stdscr.addstr(0, 0, f"Envs selected: {yes}")
    # stdscr.getch()

    _no = []
    with open("configs/no.json", "r", encoding='UTF-8') as _f:
        _no = [token for idx, token in draw_checkbox_menu(
            stdscr,
            json.loads(_f.read()),
            "=== Select Feature-sets to Disable ===")]
    # stdscr.addstr(0, 0, f"Envs selected: {_no}")
    # stdscr.getch()

    dev = []
    with open("configs/dev.json", "r", encoding='UTF-8') as _f:
        dev = [token for idx, token in draw_checkbox_menu(
            stdscr,
            json.loads(_f.read()),
            "=== Select Development Languages ===")]
    # stdscr.addstr(0, 0, f"Envs selected: {dev}")
    # stdscr.getch()

    #
    # [Color]
    #

    colors = []
    with open("plugins.json", "r", encoding='UTF-8') as _f:
        colors_list = json.loads(_f.read())["colorschemes"]
        selected_rows = draw_checkbox_menu(
            stdscr,
            colors_list,
            "=== Select Desired Colorschemes ===")
        for _, token in selected_rows:
            colors.append(token)
        for idx in range(0, len(colors_list))[::-1]:
            if idx not in [idx for idx, _ in selected_rows]:
                colors_list.pop(list(colors_list.keys())[idx])
    # stdscr.addstr(0, 0, f"Envs selected: {colors}")
    # stdscr.getch()

    color, _ = draw_single_selection_menu(
        stdscr,
        colors_list,
        "=== Preferred Colorscheme ==="
    ) if len(colors) > 0 else (-1, _)

    #
    # End
    #

    with open("config.json", "w", encoding="UTF-8") as config:
        if color > -1:
            colors.insert(0, colors.pop(color))
        config.write(f"""{{
    "base": "{base}",
    "environment": [{", ".join(f'"{token}"' for token in envs)}],
    "yes": [{", ".join(f'"{token}"' for token in yes)}],
    "no": [{", ".join(f'"{token}"' for token in _no)}],
    "dev": [{", ".join(f'"{token}"' for token in dev)}],
    "colors": [{", ".join(f'"{token}"' for token in colors)}]
}}
""")


if __name__ == "__main__":
    curses.wrapper(main)
