import curses


class InputHandler:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        # Turn ON non-blocking mode right here during setup
        self.stdscr.nodelay(True)

    def poll_action(self,appstate):
        """Non-blocking input check. Returns an action or None."""
        key = self.stdscr.getch()

        # With nodelay(True), -1 means NO key was pressed this frame
        if key == -1:
            return
        
        if key == curses.KEY_RESIZE or key == 410:
            curses.update_lines_cols()
            height, width = self.stdscr.getmaxyx()
            try:
                curses.resizeterm(height, width)
            except curses.error:
                pass
            self.stdscr.clear()

        # Map keys to actions
        if key in (ord('q'), ord('Q')):
            appstate.is_running = False