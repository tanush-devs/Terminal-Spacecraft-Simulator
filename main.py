import curses
import time

from appstate import AppState
from input_handler import InputHandler
from rendering import Renderer


def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    stime = time.perf_counter()
    last_calc = time.perf_counter()

    height, width = stdscr.getmaxyx()
    
    try:
        curses.resize_term(height, width)
        stdscr.resize(height, width)
        curses.update_lines_cols()
    except Exception:  # noqa: BLE001, S110
        pass

    appstate = AppState()
    inputhandler = InputHandler(stdscr)
    renderer = Renderer(stdscr)
    renderer.initialize_rendering()

    FRAME_BUDGET = 1 / appstate.target_fps
    
    while appstate.is_running:
        start_time = time.perf_counter()

        inputhandler.poll_action(appstate)
        
        dt = time.perf_counter() - last_calc
        last_calc = time.perf_counter()

        appstate.rocket.update_position(dt)


        renderer.render_world(appstate)

        if appstate.rocket.x > 600:
            etime = time.perf_counter()
            print(f"Total time: {etime - stime}")
            return

        end_time = time.perf_counter()
        total_time = end_time - start_time
        delay_needed = FRAME_BUDGET - total_time

        if delay_needed > 0:
            time.sleep(delay_needed)

curses.wrapper(main)
