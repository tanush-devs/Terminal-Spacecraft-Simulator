import curses
import time

from appstate import AppState
from colors import Colours
from input_handler import InputHandler
from particles import ParticleSystem
from physics import Physics
from rendering import Renderer
from world import World


def main(stdscr):
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    
    

    # stime = time.perf_counter()
    prev_t = time.perf_counter()
    fps_calc_stime = time.perf_counter()
    
    frame = 0

    height, width = stdscr.getmaxyx()
    try:
        curses.resize_term(height, width)
        stdscr.resize(height, width)
        curses.update_lines_cols()
    except Exception:  # noqa: BLE001, S110
        pass

    appstate = AppState()
    particle_system = ParticleSystem()
    renderer = Renderer()
    inputhandler = InputHandler(renderer)
    color_manager = Colours()
    world = World()
    physics = Physics()

    renderer.initialize_rendering(stdscr, appstate, world)
    color_manager.initialize()
    color_manager.init_planet_palette()

    FRAME_BUDGET = 1 / appstate.target_fps
    inputhandler.poll_action()
    

    while inputhandler.game_is_running:

        start_time = time.perf_counter()

        current_time = time.perf_counter()
        dt = current_time - prev_t
        prev_t = current_time

        physics.calculate(appstate.rocket, world.celestialbody_manager, dt, inputhandler)
        world.celestialbody_manager.check_or_process_collision(appstate.rocket)
        appstate.rocket.emit_exhaust(particle_system, dt, color_manager)
        particle_system.update(dt)

        renderer.render_world(appstate, particle_system, color_manager, world)

        fps_calc_etime = time.perf_counter()
        if fps_calc_etime - fps_calc_stime > 0.5:
            appstate.current_fps = round(frame / (fps_calc_etime - fps_calc_stime))
            fps_calc_stime = fps_calc_etime
            frame = 0

        frame += 1
        end_time = time.perf_counter()
        total_time = end_time - start_time
        delay_needed = FRAME_BUDGET - total_time

        if delay_needed > 0:
            time.sleep(delay_needed)
        

curses.wrapper(main)
