import math

from chunkmanager import CHUNK_SIZE


class Camera:
    def __init__(self, screen_h, screen_w):
        self.screen_h = screen_h
        self.screen_w = screen_w
        
    def update_size(self, screen_h, screen_w):
        self.screen_h = screen_h
        self.screen_w = screen_w


    def get_view_bounds(self, appstate, renderer):
        player_y, player_x = appstate.rocket.y , appstate.rocket.x

        center_screen_y = self.screen_h // 2
        center_screen_x_tiles = (self.screen_w // 2) // 2
        
        pad_height,pad_width = renderer.viewport.getmaxyx()
        
        center_pad_y = pad_height // 2
        center_pad_x = (pad_width // 2) // 2

        world_top_y = player_y - (center_screen_y)
        world_left_x = player_x - (center_screen_x_tiles)
        
        pad_top_y = player_y - center_pad_y
        pad_top_x = player_x - center_pad_x

        screen_player_y = round(player_y - world_top_y)
        screen_player_x = round(player_x - world_left_x) * 2

        pad_offset_y = round(pad_top_y - world_top_y)
        pad_offset_x = round(pad_top_x - world_left_x) * 2

        return (pad_offset_y,pad_offset_x,screen_player_y,screen_player_x)
    
    def get_pad_top_chunk(self, appstate, renderer):
        player_y, player_x = appstate.rocket.y , appstate.rocket.x

        pad_height,pad_width = renderer.viewport.getmaxyx()
        
        chunks_wide = pad_width // (CHUNK_SIZE * 2)

        center_pad_y = pad_height // 2
        center_pad_x = (pad_width // 2) // 2
        
        pad_top_y = player_y - center_pad_y
        pad_top_x = player_x - center_pad_x

        top_cy, left_cx , *_ = appstate.chunk_manager.world_to_chunk_coords(pad_top_y, pad_top_x)

        return(top_cy,left_cx, pad_height, chunks_wide)

    def print_values(self,appstate):
        player_y, player_x = appstate.rocket.y , appstate.rocket.x
        chunk_y,chunk_x,*_ = appstate.chunk_manager.world_to_chunk_coords(player_y,player_x)
        center_screen_y = self.screen_h // 2
        center_screen_x_tiles = (self.screen_w // 2) // 2
        
        world_top_y = player_y - (center_screen_y)
        world_left_x = player_x - (center_screen_x_tiles)

        start_chunk_y = math.floor(world_top_y / CHUNK_SIZE) - 1
        start_chunk_x = math.floor(world_left_x / CHUNK_SIZE) - 1
        
        chunk_origin_y = start_chunk_y * CHUNK_SIZE
        chunk_origin_x = start_chunk_x * CHUNK_SIZE

        pad_offset_y = round(world_top_y - chunk_origin_y)
        pad_offset_x = round(world_left_x - chunk_origin_x) * 2

        print(f"Current chunk(y,x) {chunk_y}, {chunk_x}")
        print(f"Pad top world(y,x) {chunk_origin_y}, {chunk_origin_x}")
        print(f"Pad top chunk(y,x) {start_chunk_y}, {start_chunk_x}")
        print(f"Screen top world(y,x) {round(world_top_y,3)}, {round(world_left_x,3)}")
        print(f"Pad viewport offset(y,x) {pad_offset_y}, {pad_offset_x}")
        print()


