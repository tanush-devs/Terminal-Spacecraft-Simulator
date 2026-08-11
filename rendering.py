import curses

from camera import Camera
from chunkmanager import CHUNK_SIZE, item_map


class Renderer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        height,width = stdscr.getmaxyx()
        self.camera = Camera(height,width)
        
        
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
        self.stdscr.refresh()
