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

        # Map keys to actions
        if key in (ord('q'), ord('Q')):
            appstate.is_running = False
