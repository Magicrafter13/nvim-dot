#!/usr/bin/python3
"""..."""

import curses
import json


def draw_single_selection_menu(stdscr, selected_row, things, title):
    """..."""
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    stdscr.addstr(height // 2 - len(things.keys()) - 1, width // 2 - len(title) // 2, title)  # noqa: E501  pylint: disable=line-too-long
    for idx, option in enumerate(things.keys()):
        _x = width // 2 - len(option) // 2
        _y = height // 2 - len(things.keys()) - 1 + (idx + 1) * 2

        if idx == selected_row:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(_y, _x, option)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(_y, _x, option)

    stdscr.refresh()


def draw_checkbox_menu(stdscr, highlighted_row, selected_rows, things, title):
    """..."""
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    stdscr.addstr(height // 2 - len(things.keys()) - 1, width // 2 - len(title) // 2, title)  # noqa: E501  pylint: disable=line-too-long
    for idx, option in enumerate(things.keys()):
        _x = width // 2 - (len(option) + 4) // 2
        _y = height // 2 - len(things.keys()) - 1 + (idx + 1) * 2

        option_text = f"{'[X] ' if idx in selected_rows else '[ ] '}{option}"

        if idx == highlighted_row:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(_y, _x, option_text)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(_y, _x, option_text)

    stdscr.refresh()


def main(stdscr):
    # pylint: disable=too-many-branches,too-many-locals,too-many-statements
    """..."""

    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()      # Clear the screen

    #
    # [System]
    #

    bases = {}
    with open("configs/base.json", "r", encoding='UTF-8') as _f:
        bases = json.loads(_f.read())

    selected_row = 0
    while True:
        draw_single_selection_menu(stdscr, selected_row, bases, "=== Select System Base ===")  # noqa: E501  pylint: disable=line-too-long

        key = stdscr.getch()
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(bases.keys()) - 1:
            selected_row += 1
        elif key == ord('\n') or key == ord(' '):
            break

    base = list(bases.keys())[selected_row]
    # stdscr.addstr(0, 0, f"Base selected: {base}")
    # stdscr.getch()

    envs_list = {}
    with open("configs/env.json", "r", encoding='UTF-8') as _f:
        envs_list = json.loads(_f.read())

    selected_row = 0  # highlighted_row
    selected_rows = set()
    while True:
        draw_checkbox_menu(stdscr, selected_row, selected_rows, envs_list, "=== Select Environments ===")  # noqa: E501  pylint: disable=line-too-long

        key = stdscr.getch()
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(envs_list.keys()) - 1:  # noqa: E501
            selected_row += 1
        elif key == ord(' '):
            if selected_row in selected_rows:
                selected_rows.remove(selected_row)
            else:
                selected_rows.add(selected_row)
        elif key == ord('\n'):
            break

    envs = []
    for idx in selected_rows:
        envs.append(list(envs_list.keys())[idx])
    # stdscr.addstr(0, 0, f"Envs selected: {envs}")
    # stdscr.getch()

    #
    # [Additional]
    #

    yes_list = {}
    with open("configs/yes.json", "r", encoding='UTF-8') as _f:
        yes_list = json.loads(_f.read())

    selected_row = 0  # highlighted_row
    selected_rows = set()
    while True:
        draw_checkbox_menu(stdscr, selected_row, selected_rows, yes_list, "=== Select Feature-sets to Enable ===")  # noqa: E501  pylint: disable=line-too-long

        key = stdscr.getch()
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(yes_list.keys()) - 1:  # noqa: E501
            selected_row += 1
        elif key == ord(' '):
            if selected_row in selected_rows:
                selected_rows.remove(selected_row)
            else:
                selected_rows.add(selected_row)
        elif key == ord('\n'):
            break

    yes = []
    for idx in selected_rows:
        yes.append(list(yes_list.keys())[idx])
    # stdscr.addstr(0, 0, f"Envs selected: {yes}")
    # stdscr.getch()

    no_list = {}
    with open("configs/no.json", "r", encoding='UTF-8') as _f:
        no_list = json.loads(_f.read())

    selected_row = 0  # highlighted_row
    selected_rows = set()
    while True:
        draw_checkbox_menu(stdscr, selected_row, selected_rows, no_list, "=== Select Feature-sets to Disable ===")  # noqa: E501  pylint: disable=line-too-long

        key = stdscr.getch()
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(no_list.keys()) - 1:  # noqa: E501
            selected_row += 1
        elif key == ord(' '):
            if selected_row in selected_rows:
                selected_rows.remove(selected_row)
            else:
                selected_rows.add(selected_row)
        elif key == ord('\n'):
            break

    _no = []
    for idx in selected_rows:
        _no.append(list(no_list.keys())[idx])
    # stdscr.addstr(0, 0, f"Envs selected: {_no}")
    # stdscr.getch()

    dev_list = {}
    with open("configs/dev.json", "r", encoding='UTF-8') as _f:
        dev_list = json.loads(_f.read())

    selected_row = 0  # highlighted_row
    selected_rows = set()
    while True:
        draw_checkbox_menu(stdscr, selected_row, selected_rows, dev_list, "=== Select Development Languages ===")  # noqa: E501  pylint: disable=line-too-long

        key = stdscr.getch()
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(dev_list.keys()) - 1:  # noqa: E501
            selected_row += 1
        elif key == ord(' '):
            if selected_row in selected_rows:
                selected_rows.remove(selected_row)
            else:
                selected_rows.add(selected_row)
        elif key == ord('\n'):
            break

    dev = []
    for idx in selected_rows:
        dev.append(list(dev_list.keys())[idx])
    # stdscr.addstr(0, 0, f"Envs selected: {dev}")
    # stdscr.getch()

    #
    # [Color]
    #

    colors_list = {}
    with open("plugins.json", "r", encoding='UTF-8') as _f:
        colors_list = json.loads(_f.read())["colorschemes"]

    selected_row = 0  # highlighted_row
    selected_rows = set()
    while True:
        draw_checkbox_menu(stdscr, selected_row, selected_rows, colors_list, "=== Select Desired Colorschemes ===")  # noqa: E501  pylint: disable=line-too-long

        key = stdscr.getch()
        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(colors_list.keys()) - 1:  # noqa: E501
            selected_row += 1
        elif key == ord(' '):
            if selected_row in selected_rows:
                selected_rows.remove(selected_row)
            else:
                selected_rows.add(selected_row)
        elif key == ord('\n'):
            break

    colors = []
    for idx in selected_rows:
        colors.append(list(colors_list.keys())[idx])
    for idx in range(0, len(colors_list))[::-1]:
        if idx not in selected_rows:
            colors_list.pop(list(colors_list.keys())[idx])
    # stdscr.addstr(0, 0, f"Envs selected: {colors}")
    # stdscr.getch()

    color = 0
    if len(colors) > 0:
        selected_row = 0  # highlighted_row
        while True:
            draw_single_selection_menu(stdscr, selected_row, colors_list, "=== Preferred Colorscheme ===")  # noqa: E501  pylint: disable=line-too-long

            key = stdscr.getch()
            if key == curses.KEY_UP and selected_row > 0:
                selected_row -= 1
            elif key == curses.KEY_DOWN and selected_row < len(colors_list.keys()) - 1:  # noqa: E501  pylint: disable=line-too-long
                selected_row += 1
            elif key == ord(' '):
                if selected_row in selected_rows:
                    selected_rows.remove(selected_row)
                else:
                    selected_rows.add(selected_row)
            elif key == ord('\n'):
                break

        color = selected_row

    #
    # End
    #

    with open("config.json", "w", encoding="UTF-8") as config:
        if len(colors) > 0:
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
