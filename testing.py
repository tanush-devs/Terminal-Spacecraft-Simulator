import curses
import time

from appstate import AppState
from input_handler import InputHandler
from rendering import Renderer

st_main = time.perf_counter()
frame = 0

def main(stdscr):
    global frame
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    # stime = time.perf_counter()
    prev_t = time.perf_counter()

    height, width = stdscr.getmaxyx()
    try:
        curses.resize_term(height, width)
        stdscr.resize(height, width)
        curses.update_lines_cols()
    except Exception:  # noqa: BLE001, S110
        pass

    appstate = AppState()
    inputhandler = InputHandler(appstate)
    renderer = Renderer()
    renderer.initialize_rendering(stdscr,appstate)

    FRAME_BUDGET = 1 / appstate.target_fps
    inputhandler.poll_action()

    while inputhandler.game_is_running:
        start_time = time.perf_counter()

        current_time = time.perf_counter()
        dt = current_time - prev_t
        prev_t = current_time

        appstate.rocket.update_physics(dt, inputhandler)

        renderer.render_world(appstate)

        frame += 1
        end_time = time.perf_counter()
        total_time = end_time - start_time
        delay_needed = FRAME_BUDGET - total_time

        if delay_needed > 0:
            time.sleep(delay_needed)

curses.wrapper(main)

end_main = time.perf_counter()
Actual_fps = frame / (end_main - st_main)
print(f"Actual fps: {Actual_fps:.2f}")