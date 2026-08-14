import curses
import time

from appstate import AppState
from input_handler import InputHandler
from rendering import Renderer

st_main = time.perf_counter()
frame = 0

def main(stdscr):
    global frame

    stime = time.perf_counter()
    prev_t = time.perf_counter()

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
    
    appstate.rocket.vx = 500


    while appstate.is_running:
        start_time = time.perf_counter()
        inputhandler.poll_action(appstate)
                    
        current_time = time.perf_counter()
        dt = current_time - prev_t
        prev_t = time.perf_counter()

        appstate.rocket.update_position(dt)

        renderer.render_world(appstate)

        if appstate.rocket.x > 2000:
            etime = time.perf_counter()
            print(f"Total time: {etime - stime}")
            return

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