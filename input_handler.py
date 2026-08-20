import curses


class InputHandler:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.nodelay(True)
        stdscr.keypad(True)

    def poll_action(self,appstate,renderer):
        """Non-blocking input check. Returns an action or None."""
        key = self.stdscr.getch()

        if key == curses.KEY_MOUSE:
            _, x, y, _, button_state = curses.getmouse()

            if button_state & curses.BUTTON4_PRESSED:
                renderer.telementary.scroll(-1)

            elif button_state & curses.BUTTON5_PRESSED:
                renderer.telementary.scroll(+1)

        elif key == curses.KEY_RESIZE or key == 410:
            renderer.resize_rendering(appstate)

        elif key in (ord('q'), ord('Q')):
            appstate.is_running = False

