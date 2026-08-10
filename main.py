import curses
import time

import app_state

TARGET_FPS = 30
FRAME_BUDGET = 1 / TARGET_FPS

st_main = time.perf_counter()
g1 = app_state.AppState()

def main(stdscr):
    stdscr.nodelay(True)
    width,height = stdscr.getmaxyx()

    while True:
        start_time = time.perf_counter()
        text = stdscr.getch() 

        stdscr.clear()
        stdscr.addstr(f"{width},{height}")
        stdscr.addstr(f"\n Frames: {g1.frame}")

        if text == ord("q"):
            return

        stdscr.refresh()

        g1.frame += 1
        end_time = time.perf_counter()

        total_time = end_time - start_time
        delay_needed = FRAME_BUDGET - total_time

        if delay_needed > 0:
            time.sleep(delay_needed)


curses.wrapper(main)

end_main = time.perf_counter()
Actual_fps = g1.frame / (end_main - st_main)
print(f"Actual fps: {Actual_fps:.2f}")