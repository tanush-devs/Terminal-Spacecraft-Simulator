import curses


class Colours:
    def __init__(self):
        curses.start_color()
        curses.use_default_colors()

        self.space = 1
        self.default = 2
        self.rocket = 3
        self.exhaust = 4
    
    def initialize(self):
        ORANGE = 20
        self.VSCODE_BG = 21

        curses.init_color(ORANGE, 1000, 500, 0)
        curses.init_color(self.VSCODE_BG, 98, 102, 106)

        curses.init_pair(self.default, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(self.rocket, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.exhaust, ORANGE, self.VSCODE_BG)

    def init_planet_palette(self, bg_color=-1):
        """Safely initializes custom RGB planet colors and their color pairs with ANSI fallback."""
        for color_id, _name, r, g, b, fallback_color in PLANET_COLORS:
            # Attempt to set custom RGB color (will fail safely on unsupported terminals)
            try:
                curses.init_color(color_id, r, g, b)
                fg_color = color_id
            except curses.error:
                fg_color = fallback_color

            # Initialize pair using custom color ID (or fallback ANSI color if custom RGB failed)
            try:
                curses.init_pair(color_id, fg_color, self.VSCODE_BG)
            except curses.error:
                pass






PLANET_COLORS = [
    (30, "Desert Gold",  800, 600, 200, curses.COLOR_YELLOW),
    (31, "Forest Moss",  200, 500, 200, curses.COLOR_GREEN),
    (32, "Cobalt Ocean", 200, 400, 800, curses.COLOR_BLUE),
    (33, "Molten Red",   700, 200, 200, curses.COLOR_RED),
    (34, "Rust Iron",    600, 400, 200, curses.COLOR_YELLOW),
    (35, "Lilac Gas",    700, 500, 700, curses.COLOR_MAGENTA),
    (36, "Storm Grey",   600, 600, 600, curses.COLOR_WHITE),
    (37, "Slate Teal",   200, 600, 600, curses.COLOR_CYAN),
]
