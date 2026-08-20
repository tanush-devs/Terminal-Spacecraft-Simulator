import curses
import time

from camera import Camera
from chunkmanager import CHUNK_SIZE, item_map
from telementary import Telementary


class Renderer:
    def __init__(self):
        self.screen_h = None
        self.screen_w = None
        self.pad_h = None
        self.pad_w = None
        self.camera = Camera()
        self.telementary = Telementary()
        self.lastRenderCy = None
        self.lastRenderCx = None
        self.reprint_pad = True


    def initialize_rendering(self,stdscr,appstate):
        self.stdscr = stdscr
        height,width = stdscr.getmaxyx()
        self.screen_h = height
        self.screen_w = width

        height, width = self.stdscr.getmaxyx()
        chunks_high = (height // CHUNK_SIZE) + 2
        chunks_wide = (width // (CHUNK_SIZE * 2)) + 2

        pad_height = chunks_high * CHUNK_SIZE
        pad_width = chunks_wide * CHUNK_SIZE * 2 # <--- multiplied by 2 for double-width tiles!
        self.pad_h = pad_height
        self.pad_w = pad_width

        self.viewport = curses.newpad(pad_height,pad_width)

        tele_width = min(30,width)
        tele_height = len(self.telementary.get_display_list(appstate,tele_width)) + 2
        self.tele = curses.newpad(tele_height, tele_width)
        self.telementary.max_offset = max(0, tele_height - height)

        self.overlay = curses.newwin(height, width, 0, 0)

    def resize_rendering(self,appstate):
        height, width = self.stdscr.getmaxyx()

        self.screen_h = height
        self.screen_w = width

        chunks_high = (height // CHUNK_SIZE) + 2
        chunks_wide = (width // (CHUNK_SIZE * 2)) + 2

        pad_height = chunks_high * CHUNK_SIZE
        pad_width = chunks_wide * CHUNK_SIZE * 2

        self.viewport.resize(pad_height, pad_width)

        tele_width = min(30,width)
        tele_height = len(self.telementary.get_display_list(appstate,tele_width)) + 2
        self.tele.clear()
        self.tele.resize(tele_height, tele_width)
        self.telementary.max_offset = max(0, tele_height - height)

        self.overlay.resize(height, width)

        self.render_world(appstate)


    def render_world(self, appstate):

        COLOR_ROCKET = 1
        curses.update_lines_cols()


        chunk_mgr = appstate.chunk_manager
        py, px = appstate.rocket.position
        current_cy, current_cx, *_ = chunk_mgr.world_to_chunk_coords(py, px)

        if not (self.lastRenderCy is None or self.lastRenderCx is None):
            delta_cy = current_cy - self.lastRenderCy
            delta_cx = current_cx - self.lastRenderCx
            self.reprint_pad = delta_cx != 0 or delta_cy != 0
        else:
            self.reprint_pad = True

        if self.reprint_pad:
            chunk_mgr.unload_inactive_chunks(current_cy,current_cx)
            top_cy, left_cx, pad_height, chunks_wide = self.camera.get_pad_top_chunk(appstate, self)

            for index, y in enumerate(range(pad_height)):
                d_cy = y // CHUNK_SIZE
                line = y % CHUNK_SIZE
                row_lists = [chunk_mgr.get_row_list(top_cy + d_cy, cx, line) for cx in range(left_cx, left_cx + chunks_wide)]

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
        
            self.reprint_pad = False    

        pad_offset_y,pad_offset_x,screen_player_y,screen_player_x = self.camera.get_view_bounds(appstate,self)

        self.stdscr.erase()
        self.overlay.erase()

        self.stdscr.noutrefresh()

        self.viewport.noutrefresh(
        pad_offset_y, pad_offset_x,
        0, 0,
        self.screen_h - 1, self.screen_w - 1
        )
        
        self.overlay.addstr(
            screen_player_y,
            screen_player_x,
            appstate.rocket.emoji,
            curses.color_pair(COLOR_ROCKET) | curses.A_BOLD,
        )
        self.overlay.overlay(self.stdscr)
        self.stdscr.noutrefresh()

        self.update_tele(appstate)

        self.stdscr.move(0,0)
        curses.doupdate()


    def update_tele(self,appstate):
        tmt = self.tele
        height,width = tmt.getmaxyx()
        tmt.box()
        lis = self.telementary.get_display_list(appstate,width)
        for index,line in enumerate(lis):
            tmt.addstr(index+1,1, line)

        tmt.noutrefresh(
        self.telementary.scroll_offset, 0,
        0, 0,
        min(height,self.screen_h - 1), min(30,width)
        )
