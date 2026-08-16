import curses


class InputHandler:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.nodelay(True)
        stdscr.keypad(True)

    def poll_action(self,appstate,renderer):
        """Non-blocking input check. Returns an action or None."""
        key = self.stdscr.getch()

        # With nodelay(True), -1 means NO key was pressed this frame
        if key == curses.KEY_RESIZE or key == 410:
            renderer.resize_rendering(appstate)

        # Map keys to actions
        if key in (ord('q'), ord('Q')):
            appstate.is_running = False
