import curses
import time

from app_state import AppState
from input_handler import InputHandler
from rendering import Renderer


def main(stdscr):
    stdscr.nodelay(True)
    
    renderer = Renderer(stdscr)
    input_handler = InputHandler(stdscr)
    appstate = AppState()
    
    FRAME_BUDGET = 1 / appstate.FPS

    while appstate.is_running:
        start_time = time.perf_counter()

        input_handler.poll_action(appstate)
        renderer.draw_world(appstate)

        appstate.frame += 1
        end_time = time.perf_counter()

        total_time = end_time - start_time
        delay_needed = FRAME_BUDGET - total_time

        if delay_needed > 0:
            time.sleep(delay_needed)

curses.wrapper(main)