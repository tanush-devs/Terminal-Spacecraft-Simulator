import curses
import time

from camera import Camera
from chunkmanager import CHUNK_SIZE, item_map


class Renderer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        height,width = stdscr.getmaxyx()
        self.camera = Camera(height,width)
        self.lastRenderCy = None
        self.lastRenderCx = None
        self.last_time = time.perf_counter()


    def initialize_rendering(self):
        height, width = self.stdscr.getmaxyx()
        chunks_high = (height // CHUNK_SIZE) + 2
        chunks_wide = (width // (CHUNK_SIZE * 2)) + 2

        pad_height = chunks_high * CHUNK_SIZE
        pad_width = chunks_wide * CHUNK_SIZE * 2 # <--- multiplied by 2 for double-width tiles!

        self.viewport = curses.newpad(pad_height,pad_width)
        self.telementary = curses.newwin(25, 20, 0, 0)
        self.overlay = curses.newwin(height, width, 0, 0)

        

    def render_world(self, appstate):

        COLOR_ROCKET = 1
        curses.update_lines_cols()


        height,width = self.stdscr.getmaxyx()
        self.camera.update_size(height, width)

        chunk_mgr = appstate.chunk_manager
        is_first_frame = self.lastRenderCy is None or self.lastRenderCx is None
        
        py, px = appstate.rocket.position
        current_cy, current_cx, *_ = chunk_mgr.world_to_chunk_coords(py, px)
        if not is_first_frame:
            delta_cy = current_cy - self.lastRenderCy
            delta_cx = current_cx - self.lastRenderCy
        else:
            self.initialize_tlementary(appstate)
            delta_cy = 0
            delta_cx = 0

        if is_first_frame or delta_cx != 0 or delta_cy != 0:
            start = time.perf_counter()

            chunk_mgr.update_active_chunks(current_cy,current_cx)
            top_cy, left_cx, pad_height, chunks_wide = self.camera.get_pad_top_chunk(appstate, self)

            for index, y in enumerate(range(pad_height)):
                d_cy = y // CHUNK_SIZE
                line = y % CHUNK_SIZE
                row_lists = [chunk_mgr.get_row_lis(top_cy + d_cy, cx, line) for cx in range(left_cx, left_cx + chunks_wide)]

                row_lis = [item_map.TILE_MAP.get(tile, "  ")
                        for lis in row_lists
                        for tile in lis
                        ]

                row_str = "".join(row_lis)
                try:
                    self.viewport.addstr(index, 0, row_str)
                except curses.error:  
                    pass  # Ignores the harmless bottom-right overflow error

            self.lastRenderCy = current_cy
            self.lastRenderCx = current_cx

            print(f"Time taken for pad rebuild: {time.perf_counter() - start}")
            
        

        pad_offset_y,pad_offset_x,screen_player_y,screen_player_x = self.camera.get_view_bounds(appstate,self)
        
        self.stdscr.erase()
        self.overlay.erase()

        self.stdscr.noutrefresh()

        self.viewport.noutrefresh(
        pad_offset_y, pad_offset_x,
        0, 0,
        height - 1, width - 1
        )
        
        self.overlay.addstr(
            screen_player_y,
            screen_player_x,
            "▲ ",
            curses.color_pair(COLOR_ROCKET) | curses.A_BOLD,
        )
        self.overlay.overlay(self.stdscr)
        self.stdscr.noutrefresh()


        self.update_telementary(appstate)


        self.stdscr.move(0,0)
        curses.doupdate()

    def initialize_tlementary(self, appstate):
        tmt = self.telementary
        tmt.box()
        tmt.addstr(1, 5, "◈ TELEMETRY")
        tmt.addstr(3, 1, "─"*18)
        rocket = appstate.rocket
        tmt.addstr(5, 2, "POSITION")
        tmt.addstr(6, 2, f"X : {round(rocket.x,3): <5}")
        tmt.addstr(7, 2, f"Y : {round(-rocket.y,3): <5}")
        tmt.addstr(9, 2, "VELOCITY")
        tmt.addstr(11, 2, f"X : {round(rocket.vx,3): <5}")
        tmt.addstr(12, 2, f"Y : {round(-rocket.vy,3): <5}")
        tmt.addstr(13, 2, f"<V> : {round(rocket.current_speed(),3): <5}")
        tmt.addstr(15, 2, "ACCELARATION")
        tmt.addstr(17, 2, f"X : {round(rocket.ax,3): <5}")
        tmt.addstr(18, 2, f"Y : {round(-rocket.ay,3): <5}")
        tmt.addstr(19, 2, f"<A> : {round(rocket.current_accelaration(),3): <5}")
        tmt.addstr(21, 2, f"THRUST : {round(rocket.thrust),3}")
        chunk_y, chunk_x, *_ = appstate.chunk_manager.world_to_chunk_coords(rocket.y,rocket.x)
        tmt.addstr(23, 2, f"CHUNK : ({chunk_x},{-chunk_y})")
        tmt.noutrefresh()

    def update_telementary(self,appstate):
        tmt = self.telementary
        tmt.box()
        rocket = appstate.rocket
        tmt.addstr(6, 6, f"{round(rocket.x,3): <5}")
        tmt.addstr(7, 6, f"{round(-rocket.y,3): <5}")

        tmt.addstr(11, 6, f"{round(rocket.vx,3): <5}")
        tmt.addstr(12, 6, f"{round(-rocket.vy,3): <5}")
        tmt.addstr(13, 8, f"{round(rocket.current_speed(),3): <5}")
        
        tmt.addstr(17, 6, f"{round(rocket.ax,3): <5}")
        tmt.addstr(18, 6, f"{round(-rocket.ay,3): <5}")
        tmt.addstr(19, 8, f"{round(rocket.current_accelaration(),3): <5}")

        tmt.addstr(21, 11, f"{round(rocket.thrust),3}")

        chunk_y, chunk_x, *_ = appstate.chunk_manager.world_to_chunk_coords(rocket.y,rocket.x)
        tmt.addstr(23, 10, f"({chunk_x},{-chunk_y})")
        tmt.noutrefresh()
        
