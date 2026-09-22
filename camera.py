from chunkmanager import CHUNK_SIZE


class Camera:

    def get_view_bounds(self, appstate, renderer):
        player_y, player_x = appstate.rocket.y , appstate.rocket.x

        center_screen_y = renderer.screen_h // 2
        center_screen_x_tiles = (renderer.screen_w // 2) // 2

        pad_top_y = self.pad_top_chunk * CHUNK_SIZE
        pad_top_x = self.pad_left_chunk * CHUNK_SIZE

        self.screen_top_y = player_y - center_screen_y
        self.screen_top_x = player_x - center_screen_x_tiles

        screen_player_y = round(player_y - self.screen_top_y)
        screen_player_x = round(player_x - self.screen_top_x) * 2

        pad_offset_y = round(self.screen_top_y - pad_top_y)
        pad_offset_x = round(self.screen_top_x - pad_top_x) * 2

        return (pad_offset_y,pad_offset_x,screen_player_y,screen_player_x)

    def get_pad_top_chunk(self, appstate, renderer, world):
        player_y, player_x = appstate.rocket.y , appstate.rocket.x
        
        chunks_wide = renderer.pad_w // (CHUNK_SIZE * 2)

        center_pad_y = renderer.pad_h // 2
        center_pad_x = (renderer.pad_w // 2) // 2

        pad_origin_y = player_y - center_pad_y
        pad_origin_x = player_x - center_pad_x

        top_cy, left_cx, *_ = world.chunk_manager.world_to_chunk_coords(
            pad_origin_y, pad_origin_x
)
        self.pad_top_chunk = top_cy
        self.pad_left_chunk = left_cx

        return(top_cy,left_cx, renderer.pad_h, chunks_wide)

    def get_relative_screen_coordinates(self, y,x, screen_h,screen_w):

        relative_y = -(self.screen_top_y - y)   # different system so diff sign
        relative_x = x - self.screen_top_x
        
        if 0 < relative_y < screen_h-1:
            screen_y = int(relative_y)
        else:
            screen_y = None

        if 0 < relative_x*2 < screen_w-1:
            screen_x = int(relative_x*2)
        else:
            screen_x = None

        return screen_y,screen_x

    def get_relative_pad_coordinates(self, y,x, renderer):
        top_y = self.pad_top_chunk * CHUNK_SIZE
        top_x = self.pad_left_chunk * CHUNK_SIZE

        relative_y = -(top_y - y)   # different system so diff sign
        relative_x = x - top_x

        if 0 < relative_y < renderer.pad_h-1:
            pad_y = int(relative_y)
        else:
            pad_y = None

        if 0 < relative_x*2 < renderer.pad_w-1:
            pad_x = int(relative_x*2)
        else:
            pad_x = None

        return pad_y,pad_x