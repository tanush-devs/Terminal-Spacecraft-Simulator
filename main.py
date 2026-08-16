import curses
import time

from appstate import AppState
from input_handler import InputHandler
from rendering import Renderer


def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    prev_t = time.perf_counter()


    appstate = AppState()
    inputhandler = InputHandler(stdscr)
    renderer = Renderer()
    renderer.initialize_rendering(stdscr)

    FRAME_BUDGET = 1 / appstate.target_fps
    
    while appstate.is_running:
        start_time = time.perf_counter()

        inputhandler.poll_action(appstate,renderer)

        dt = min(time.perf_counter() - prev_t, 0.06)
        prev_t = time.perf_counter()

        appstate.rocket.update_position(dt)

        renderer.render_world(appstate)

        end_time = time.perf_counter()
        total_time = end_time - start_time
        delay_needed = FRAME_BUDGET - total_time

        if delay_needed > 0:
            time.sleep(delay_needed)

curses.wrapper(main)