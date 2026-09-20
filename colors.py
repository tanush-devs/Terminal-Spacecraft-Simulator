import curses


class Colours:
    def __init__(self):
        curses.start_color()
        curses.use_default_colors()

        self.space = 1
        self.default = 2
        self.rocket = 3
        self.exhaust = 4
    
    def initialize(self, stdscr):
        ORANGE = 20
        VSCODE_BG = 21

        curses.init_color(ORANGE, 1000, 500, 0)
        curses.init_color(VSCODE_BG, 98, 102, 106)

        curses.init_pair(self.default, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(self.rocket, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.exhaust, ORANGE, VSCODE_BG)

