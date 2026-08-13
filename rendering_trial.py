import curses

from camera import Camera
from chunkmanager import CHUNK_SIZE, item_map


class Renderer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        height,width = stdscr.getmaxyx()
        self.camera = Camera(height,width)

    def initialize_rendering(self):
        height, width = self.stdscr.getmaxyx()
        chunks_high = (height // CHUNK_SIZE) + 2
        chunks_wide = (width // (CHUNK_SIZE * 2)) + 2

        pad_height = chunks_high * CHUNK_SIZE
        pad_width = chunks_wide * CHUNK_SIZE * 2 # <--- multiplied by 2 for double-width tiles!

        self.viewport = curses.newpad(pad_height,pad_width)
        self.telementary = curses.newwin(25, 20, 0, 0)

    def render_world(self, appstate):
        COLOR_ROCKET = 1
        curses.update_lines_cols()

        player_y, player_x = appstate.rocket.position
        pad_offset_y,pad_offset_x,screen_player_y,screen_player_x = self.camera.get_view_bounds(player_y, player_x)

        height,width = self.stdscr.getmaxyx()
        self.camera.update_size(height, width)

        chunk_mgr = appstate.chunk_manager
        is_first_frame = chunk_mgr.last_cy is None or chunk_mgr.last_cx is None
        
        radius_y = (height // CHUNK_SIZE) + 2
        radius_x = (width // CHUNK_SIZE) + 2
        appstate.chunk_manager.update_active_chunks(appstate, radius_y,radius_x)

        py, px = appstate.rocket.position
        center_cy, center_cx, *_ = chunk_mgr.world_to_chunk_coords(py, px)
        
        if not is_first_frame:
            delta_cy = center_cy - chunk_mgr.last_cy
            delta_cx = center_cx - chunk_mgr.last_cx
        else:
            self.initialize_tlementary(appstate)
            delta_cy = 0
            delta_cx = 0
            

        if is_first_frame or delta_cx != 0 or delta_cy != 0:
            print(delta_cy,delta_cx)
            appstate.print_values = True
            top_cy, top_cx, pad_height, chunks_wide = self.camera.get_pad_top_chunk(appstate)

            for index, y in enumerate(range(pad_height)):
                d_cy = y // 32
                line = y % 32
                row_lists = [chunk_mgr.get_row_lis(top_cy + d_cy, cx, line) for cx in range(top_cx,top_cx + chunks_wide + 1)]
                row_lis = [item_map.TILE_MAP.get(tile, "  ")
                        for lis in row_lists
                        for tile in lis
                        ]

                row_str = "".join(row_lis)
                try:
                    self.viewport.addstr(index, 0, row_str)
                except curses.error:  
                    pass  # Ignores the harmless bottom-right overflow error
                
                chunk_mgr.last_cy = center_cy
                chunk_mgr.last_cx = center_cx

        self.stdscr.erase()
        self.stdscr.move(0,0)

        self.stdscr.noutrefresh()
        self.viewport.noutrefresh(
        pad_offset_y, pad_offset_x,
        0, 0,
        height - 1, width - 1
        )

        self.stdscr.addstr(
            screen_player_y,
            screen_player_x,
            "▲ ",
            curses.color_pair(COLOR_ROCKET) | curses.A_BOLD,
        )

        self.telementary.touchwin()
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
        
        tmt.addstr(11, 6, f"{round(rocket.ax,3): <5}")
        tmt.addstr(12, 6, f"{round(-rocket.ay,3): <5}")
        tmt.addstr(13, 8, f"{round(rocket.current_accelaration(),3): <5}")

        tmt.addstr(21, 11, f"{round(rocket.thrust),3}")

        chunk_y, chunk_x, *_ = appstate.chunk_manager.world_to_chunk_coords(rocket.y,rocket.x)
        tmt.addstr(23, 10, f"({chunk_x},{-chunk_y})")
        tmt.noutrefresh()
        
