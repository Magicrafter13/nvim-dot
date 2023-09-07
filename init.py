#!/usr/bin/python3
"""Walks user through creating config.json file for use with build.py."""

import curses
import json
import os

from main.utils import read_file


def get_center(stdscr: curses.window):
    """Get the center values of a curses screen."""
    height, width = stdscr.getmaxyx()
    return width // 2, height // 2


def display_list_option(
    stdscr: curses.window,
    option: str,
    highlighted: bool,
    _x: int,
    _y: int
):
    """Show a list option with optional highlight."""
    if highlighted:
        stdscr.attron(curses.A_REVERSE)
    stdscr.addstr(_y, _x, option)
    stdscr.attroff(curses.A_REVERSE)


def get_menu_input(stdscr: curses.window, space_is_enter: bool):
    """Wait for user to press a valid key, and returns a common code."""
    while True:
        key = stdscr.getch()
        if key in {curses.KEY_UP, ord('k')}:
            return 'k'
        if key in {curses.KEY_DOWN, ord('j')}:
            return 'j'
        if key in {curses.KEY_RIGHT, ord('l'), curses.KEY_ENTER}:
            return 'l'
        if key == ord(' '):
            return 'l' if space_is_enter else ' '
        if key == ord('a'):
            return 'a'


def draw_single_selection_menu(
    stdscr: curses.window,
    things: dict,
    title: str,
    initial: str
):
    """Single option menu screen.

    Creates a menu where the user may select one of the provided options, and
    then returns that option as a tuple, where the first item is the string,
    and the second item is the dictionary entry. The user may navigate using
    the up/down arrow keys, or j/k (vi style). They may select an option with
    space or enter.
    """
    last_idx = len(things.keys()) - 1

    highlighted_row = (
        list(things.keys()).index(initial)
        if initial and initial in things.keys()
        else 0)
    while True:
        stdscr.clear()
        h_center, v_center = get_center(stdscr)

        stdscr.addstr(v_center - last_idx, h_center - len(title) // 2, title)
        for idx, option in list(enumerate(things.keys())):
            # for _y:
            # + 1 because the title is an entry
            display_list_option(
                stdscr,
                option,
                idx == highlighted_row,
                h_center - len(option) // 2,
                v_center - last_idx + (idx + 1) * 2)

        stdscr.refresh()

        match get_menu_input(stdscr, True):
            case 'k':
                if highlighted_row > 0:
                    highlighted_row -= 1
            case 'j':
                if highlighted_row < last_idx:
                    highlighted_row += 1
            case 'l':
                break

    return (highlighted_row, list(things.keys())[highlighted_row])


def draw_checkbox_menu(
    stdscr: curses.window,
    things: dict,
    title: str,
    initial: list
):
    """Multiple option menu screen.

    Creates a menu where the user may select any of the provided options (or
    none), and then returns those options as an array of tuples, where the
    first item in each tuple is the array index, and the second item in each
    tuple is the dictionary key. The user may navigate using the up/down arrow
    keys, or j/k (vi style). They may select an option with space, and confirm
    their choices with enter.
    """
    # pylint: disable=too-many-locals
    last_idx = len(things.keys()) - 1

    highlighted_row = 0
    selected_rows = {
        list(things.keys()).index(i)
        for i in initial
        if i in things.keys()
    } or set()
    while True:
        stdscr.clear()
        h_center, v_center = get_center(stdscr)

        stdscr.addstr(v_center - last_idx, h_center - len(title) // 2, title)
        for idx, option in list(enumerate(things.keys())):
            # for _x and _y:
            # + 4 because of the length of '[X] ' and '[ ] '
            # + 1 because the title is an entry
            display_list_option(
                stdscr,
                f"[{'X' if idx in selected_rows else ' '}] {option}",
                idx == highlighted_row,
                h_center - (len(option) + 4) // 2,
                v_center - last_idx + (idx + 1) * 2)

        stdscr.refresh()

        match get_menu_input(stdscr, False):
            case 'k':
                if highlighted_row > 0:
                    highlighted_row -= 1
            case 'j':
                if highlighted_row < last_idx:
                    highlighted_row += 1
            case 'l':
                break
            case ' ':
                if highlighted_row in selected_rows:
                    selected_rows.remove(highlighted_row)
                else:
                    selected_rows.add(highlighted_row)
            case 'a':
                selected_rows.update(range(last_idx + 1))

    return [(idx, list(things.keys())[idx]) for idx in selected_rows]


def main(stdscr: curses.window):
    """Run main curses screen and software logic.

    Reads the user's config.json file if it exists, so that the options they
    selected last time this script was run, will already be selected when they
    get to each screen.

    Prompts the user to select options for their config.json file - to see the
    order this happens, refer to the # [...] comments below.
    """
    config = (
        json.loads(read_file("config.json"))
        if os.path.exists("config.json")
        else {})

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
            {"lsp": {}, "completion": {}},
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
    colors_list = {
        _n: _p
        for _n, _p in json.loads(read_file("plugins.json")).items()
        if "attributes" in _p and "colorscheme" in _p["attributes"]}
    selected_rows = draw_checkbox_menu(
        stdscr,
        colors_list,
        "=== Select Desired Colorschemes ===",
        config["colors"] if config else [])
    colors = [token for _, token in selected_rows]
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
