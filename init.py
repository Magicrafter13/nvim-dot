#!/usr/bin/python3
"""Walks user through creating config.json file for use with build.py."""

import curses
import json
import os

from main.utils import read_file


def draw_single_selection_menu(stdscr, things: dict, title: str, initial: str):
    """Create a menu where the user selects a single option (either with space
    or enter)"""
    last_idx = len(things.keys()) - 1
    iterate = list(enumerate(things.keys()))

    highlighted_row = (
        list(things.keys()).index(initial)
        if initial and initial in things.keys()
        else 0)
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        h_center = width // 2
        v_center = height // 2

        stdscr.addstr(v_center - last_idx, h_center - len(title) // 2, title)
        for idx, option in iterate:
            _x = h_center - len(option) // 2
            # + 1 because the title is an entry
            _y = v_center - last_idx + (idx + 1) * 2

            if idx == highlighted_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(_y, _x, option)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(_y, _x, option)

        stdscr.refresh()

        key = stdscr.getch()
        if (key == curses.KEY_UP or key == ord('k')) and highlighted_row > 0:
            highlighted_row -= 1
        elif (key == curses.KEY_DOWN or
                key == ord('j')) and highlighted_row < last_idx:
            highlighted_row += 1
        elif key == ord('\n') or key == ord(' '):
            break

    return (highlighted_row, list(things.keys())[highlighted_row])


def draw_checkbox_menu(stdscr, things: dict, title: str, initial: list):
    """Create a menu where the user selects any options (or none) that they
    want with space, then press enter to confirm their selections - they may
    also press a to quickly check all options"""
    # pylint: disable=too-many-locals
    last_idx = len(things.keys()) - 1
    iterate = list(enumerate(things.keys()))

    highlighted_row = 0
    selected_rows = {list(things.keys()).index(i) for i in initial if i in things.keys()} or set()
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        h_center = width // 2
        v_center = height // 2

        stdscr.addstr(v_center - last_idx, h_center - len(title) // 2, title)
        for idx, option in iterate:
            # + 4 because of the length of '[X] ' and '[ ] '
            _x = h_center - (len(option) + 4) // 2
            # + 1 because the title is an entry
            _y = v_center - last_idx + (idx + 1) * 2

            option_text = f"[{'X' if idx in selected_rows else ' '}] {option}"

            if idx == highlighted_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(_y, _x, option_text)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(_y, _x, option_text)

        stdscr.refresh()

        key = stdscr.getch()
        if (key == curses.KEY_UP or key == ord('k')) and highlighted_row > 0:
            highlighted_row -= 1
        elif (key == curses.KEY_DOWN or
                key == ord('j')) and highlighted_row < last_idx:
            highlighted_row += 1
        elif key == ord(' '):
            if highlighted_row in selected_rows:
                selected_rows.remove(highlighted_row)
            else:
                selected_rows.add(highlighted_row)
        elif key == ord('\n'):
            break
        elif key == ord('a'):
            selected_rows.update(range(last_idx + 1))

    return [(idx, list(things.keys())[idx]) for idx in selected_rows]


def main(stdscr):
    """Main ncurses and software logic"""
    config = json.loads(read_file("config.json")) if os.path.exists("config.json") else {}

    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()      # Clear the screen

    #
    # [System]
    #

    base = draw_single_selection_menu(
        stdscr,
        json.loads(read_file("configs/base.json")),
        "=== Select System Base ===",
        config["base"] if config else "")

    envs = [token for idx, token in draw_checkbox_menu(
        stdscr,
        json.loads(read_file("configs/env.json")),
        "=== Select Environments ===",
        config["environment"] if config else [])]

    #
    # [Additional]
    #

    yes = [token for idx, token in draw_checkbox_menu(
        stdscr,
        json.loads(read_file("configs/yes.json")),
        "=== Select Feature-sets to Enable ===",
        config["yes"] if config else [])]

    programming = []
    dev = []
    if "programming" in yes:
        programming = [token for idx, token in draw_checkbox_menu(
            stdscr,
            { "lsp": {}, "completion": {} },
            "=== Select Programming Features ===",
            config["programming"] if config else []
            )]
        dev = [token for idx, token in draw_checkbox_menu(
            stdscr,
            json.loads(read_file("configs/dev.json")),
            "=== Select Development Languages ===",
            config["dev"] if config else [])]


    #
    # [Color]
    #

    colors = []
    with open("plugins.json", "r", encoding='UTF-8') as _f:
        colors_list = {
            _n: _p
            for _n, _p in json.loads(_f.read()).items()
            if "attributes" in _p and "colorscheme" in _p["attributes"]}
        selected_rows = draw_checkbox_menu(
            stdscr,
            colors_list,
            "=== Select Desired Colorschemes ===",
            config["colors"] if config else [])
        for _, token in selected_rows:
            colors.append(token)
        for idx in range(0, len(colors_list))[::-1]:
            if idx not in [idx for idx, _ in selected_rows]:
                colors_list.pop(list(colors_list.keys())[idx])

    color, _ = draw_single_selection_menu(
        stdscr,
        colors_list,
        "=== Preferred Colorscheme ===",
        config["colors"][0] if config else ""
    ) if len(colors) > 1 else (0 if len(colors) == 1 else -1, None)

    #
    # End
    #

    with open("config.json", "w", encoding="UTF-8") as config:
        if color > -1:
            colors.insert(0, colors.pop(color))
        config.write(f"""{{
    "base": "{base[1]}",
    "environment": [{", ".join(f'"{token}"' for token in envs)}],
    "yes": [{", ".join(f'"{token}"' for token in yes)}],
    "programming": [{", ".join(f'"{token}"' for token in programming)}],
    "dev": [{", ".join(f'"{token}"' for token in dev)}],
    "colors": [{", ".join(f'"{token}"' for token in colors)}]
}}
""")


if __name__ == "__main__":
    curses.wrapper(main)
