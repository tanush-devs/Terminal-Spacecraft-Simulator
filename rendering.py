import curses


class Renderer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        # Initialize color pairs once inside the renderer
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def draw_world(self, appstate):
        """Main render entrypoint called inside the loop."""
        self.stdscr.clear()
        
        self.stdscr.addstr(f"Frame: {appstate.frame}")

        self.stdscr.refresh()