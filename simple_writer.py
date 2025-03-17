# Written by github.com/Gotoro
# Under MIT license

from curses import wrapper
from os.path import isfile
import curses

# simple class representing current cursor position
class Pos:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __add__(self, foreign_pos):
        return Pos(
            y = self.y + foreign_pos.y,
            x = self.x + foreign_pos.x
        )

def main(stdscr):
    # define background
    curses.use_default_colors()
    # use default terminal fg and bg
    curses.init_pair(1, -1, -1)
    # fill the background with Space " " symbol
    stdscr.bkgd(" ", curses.color_pair(1))

    # define directional (arrow) keys
    dir_keys = {
        "KEY_LEFT": Pos(0, -1),
        "KEY_RIGHT": Pos(0, 1),
        "KEY_UP": Pos(-1, 0),
        "KEY_DOWN": Pos(1, 0),
    }

    # clear screen
    stdscr.clear()

    # init coordinates
    cur_pos = Pos(y = 0, x = 0)
    stdscr.addstr(0, 0, f"x, y: {cur_pos.x}, {cur_pos.y}")

    while (cur_key := stdscr.getkey(cur_pos.y, cur_pos.x)) != "Q":

        # arrow handling, update current cursor coordinates
        if cur_key in dir_keys:
            cur_pos += dir_keys[cur_key]

            if cur_pos.x < 0:
                cur_pos.x = 0
            if cur_pos.y < 0:
                cur_pos.y = 0
        # delete the character to the left
        elif cur_key == "KEY_BACKSPACE":
            cur_pos += dir_keys["KEY_LEFT"]
            stdscr.addstr(cur_pos.y, cur_pos.x, " ")
        # if we didn't get any arrow keys, type the character
        else:
            stdscr.addstr(cur_pos.y, cur_pos.x, cur_key)
            cur_pos += dir_keys["KEY_RIGHT"]

        # print current coordinates
        stdscr.addstr(0, 0, f"x, y: {cur_pos.x}, {cur_pos.y}")

        stdscr.refresh()


if __name__ == "__main__":
    # create file if it doesn't exist
    if not isfile("todo.txt"):
        with open("todo.txt", "w") as txt:
            txt.write("")

    # read all lines into a list
    with open("todo.txt") as txt:
        out_txt = txt.read().splitlines()

    wrapper(main)

