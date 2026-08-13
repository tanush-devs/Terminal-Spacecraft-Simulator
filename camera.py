import math

from chunkmanager import CHUNK_SIZE


class Camera:
    def __init__(self, screen_h, screen_w):
        self.screen_h = screen_h
        self.screen_w = screen_w
        
    def update_size(self, screen_h, screen_w):
        self.screen_h = screen_h
        self.screen_w = screen_w


    def get_view_bounds(self, player_y, player_x):
        # 1. Screen center targets
        center_screen_y = self.screen_h // 2
        # Screen center in tile units (since 1 tile = 2 characters)
        center_screen_x_tiles = (self.screen_w // 2) // 2

        # 2. Continuous world coordinate of the top-left corner of the screen
        world_top_y = player_y - center_screen_y
        world_left_x = player_x - center_screen_x_tiles

        # 3. First chunk needed on the pad
        start_chunk_y = math.floor(world_top_y / CHUNK_SIZE)
        start_chunk_x = math.floor(world_left_x / CHUNK_SIZE)

        # 4. Top-left world coordinate of that starting chunk
        chunk_origin_y = start_chunk_y * CHUNK_SIZE
        chunk_origin_x = start_chunk_x * CHUNK_SIZE

        # 5. Exact pixel/character offset inside the pad to start drawing screen at (0,0)
        # Offset = (Screen Top Left World Pos) - (Pad Origin World Pos)
        pad_offset_y = round(world_top_y - chunk_origin_y)
        # Multiply x by 2 for double-width tiles!
        pad_offset_x = round(world_left_x - chunk_origin_x) * 2

        return (pad_offset_y,pad_offset_x)
    
    def get_pad_top_chunk(self, appstate):
        chunks_high = (self.screen_h // CHUNK_SIZE) + 2
        chunks_wide = (self.screen_w // CHUNK_SIZE) + 2

        pad_height = chunks_high * CHUNK_SIZE
        pad_width = chunks_wide * CHUNK_SIZE

        top_cord_y = appstate.rocket.y + pad_height // 2   # y coordinate of top point
        top_cord_x = appstate.rocket.x + pad_width // 2

        top_cy, top_cx , *_ = appstate.chunk_manager.world_to_chunk_coords(top_cord_y, top_cord_x)
        
        return(top_cy,top_cx, pad_height, chunks_wide)
