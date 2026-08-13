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
        chunks_high = (height // CHUNK_SIZE) + 1
        chunks_wide = (width // CHUNK_SIZE) + 1
        
        pad_height = chunks_high * CHUNK_SIZE
        pad_width = chunks_wide * CHUNK_SIZE * 2 # <--- multiplied by 2 for double-width tiles!
        
        self.viewport = curses.newpad(pad_height,pad_width)
        self.telementary = curses.newwin(25, 20, 0, 0)

    def render_world(self, appstate):
        COLOR_ROCKET = 1
        curses.init_pair(COLOR_ROCKET, curses.COLOR_RED, curses.COLOR_BLACK)


        curses.update_lines_cols()
        self.stdscr.erase()
        
        player_y, player_x = appstate.rocket.position
        top_y,left_x = self.camera.get_view_bounds(player_y, player_x)
        
        height,width = self.stdscr.getmaxyx()
        self.camera.update_size(height, width)  
        
        radius_y = (height // CHUNK_SIZE) + 2
        radius_x = (width // CHUNK_SIZE) + 2
        appstate.chunk_manager.update_active_chunks(appstate, radius_y,radius_x)
        
        chunk_mgr = appstate.chunk_manager
        tiles_wide = width // 2
        is_first_frame = chunk_mgr.last_cy is None or chunk_mgr.last_cx is None
        print(is_first_frame)
        if is_first_frame:
            self.initialize_tlementary(appstate)

        for index, y in enumerate(range(top_y,top_y + height)):
            row_lis = [item_map.TILE_MAP.get(chunk_mgr.get_tile(y, x), "  ")
                       for x in range(left_x,left_x + tiles_wide)
                    ]

            row_str = "".join(row_lis)
            try:
                self.stdscr.addstr(index, 0, row_str)
            except curses.error:  
                pass  # Ignores the harmless bottom-right overflow error
        

        # Bold makes standard curses cyan much brighter/thicker!
        self.stdscr.addstr(
            int(height // 1.5),
            width // 2,
            "▲ ",
            curses.color_pair(COLOR_ROCKET) | curses.A_BOLD,
        )
        
        self.stdscr.move(0,0)
        self.stdscr.noutrefresh()
        self.initialize_tlementary(appstate)
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
        tmt.addstr(13, 2, f"<V> : {round(rocket.current_accelaration(),3): <5}")
        tmt.noutrefresh()

    def update_telementary(self,appstate):
        tmt = self.telementary
        rocket = appstate.rocket
        tmt.addstr(6, 6, f"{round(rocket.x,3): <5}")
        tmt.addstr(7, 6, f"{round(-rocket.y,3): <5}")

        tmt.addstr(11, 6, f"{round(rocket.vx,3): <5}")
        tmt.addstr(12, 6, f"{round(-rocket.vy,3): <5}")
        tmt.addstr(13, 8, f"{round(rocket.current_accelaration(),3): <5}")
        tmt.noutrefresh()