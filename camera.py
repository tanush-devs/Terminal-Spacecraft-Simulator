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

        pad_top_y = self.pad_top_chunk * CHUNK_SIZE
        pad_top_x = self.pad_left_chunk * CHUNK_SIZE

        world_top_y = player_y - center_screen_y
        world_left_x = player_x - center_screen_x_tiles

        screen_player_y = round(player_y - world_top_y)
        screen_player_x = round(player_x - world_left_x) * 2

        pad_offset_y = round(world_top_y - pad_top_y)
        pad_offset_x = round(world_left_x - pad_top_x) * 2

        return (pad_offset_y,pad_offset_x,screen_player_y,screen_player_x)
    
    def get_pad_top_chunk(self, appstate, renderer):
        player_y, player_x = appstate.rocket.y , appstate.rocket.x

        pad_height,pad_width = renderer.viewport.getmaxyx()
        
        chunks_wide = pad_width // (CHUNK_SIZE * 2)

        center_pad_y = pad_height // 2
        center_pad_x = (pad_width // 2) // 2

        pad_origin_y = player_y - center_pad_y
        pad_origin_x = player_x - center_pad_x

        top_cy, left_cx, *_ = appstate.chunk_manager.world_to_chunk_coords(
            pad_origin_y, pad_origin_x
)

        self.pad_top_chunk = top_cy
        self.pad_left_chunk = left_cx
        
        return(top_cy,left_cx, pad_height, chunks_wide)

    def print_values(self, appstate, renderer):
        player_y, player_x = appstate.rocket.y, appstate.rocket.x

        # Player chunk
        chunk_y, chunk_x, *_ = (
            appstate.chunk_manager.world_to_chunk_coords(player_y, player_x)
        )

        # -----------------------------
        # SCREEN GEOMETRY
        # -----------------------------

        screen_h = self.screen_h
        screen_w = self.screen_w

        center_screen_y = screen_h // 2
        center_screen_x_tiles = (screen_w // 2) // 2

        # -----------------------------
        # PAD GEOMETRY
        # -----------------------------

        pad_height, pad_width = renderer.viewport.getmaxyx()

        center_pad_y = pad_height // 2
        center_pad_x_tiles = (pad_width // 2) // 2

        chunks_tall = pad_height // CHUNK_SIZE
        chunks_wide = pad_width // (CHUNK_SIZE * 2)

        # -----------------------------
        # WORLD / SCREEN POSITION
        # -----------------------------

        world_top_y = player_y - center_screen_y
        world_left_x = player_x - center_screen_x_tiles

        # -----------------------------
        # PAD ORIGIN
        # -----------------------------

        top_cy, left_cx, *_ = self.get_pad_top_chunk(appstate, renderer)

        pad_origin_y = top_cy * CHUNK_SIZE
        pad_origin_x = left_cx * CHUNK_SIZE

        # -----------------------------
        # VIEWPORT OFFSET
        # -----------------------------

        pad_offset_y = round(world_top_y - pad_origin_y)
        pad_offset_x = round(world_left_x - pad_origin_x) * 2

        # -----------------------------
        # ACTUAL WORLD POSITION SHOWN
        # -----------------------------

        viewport_world_y = pad_origin_y + pad_offset_y
        viewport_world_x = pad_origin_x + (pad_offset_x / 2)

        error_y = viewport_world_y - world_top_y
        error_x = viewport_world_x - world_left_x

        # ==================================================
        # DEBUG OUTPUT
        # ==================================================

        print("========== PAD DEBUG ==========")

        print(f"SCREEN SIZE       : {screen_h} rows x {screen_w} cols")

        print(
            f"SCREEN CENTER     : "
            f"y={center_screen_y}, "
            f"x={center_screen_x_tiles} world"
        )

        print(
            f"PAD SIZE          : "
            f"{pad_height} rows x {pad_width} cols"
        )

        print(
            f"PAD CENTER        : "
            f"y={center_pad_y}, "
            f"x={center_pad_x_tiles} world"
        )

        print(
            f"CHUNKS FIT        : "
            f"y={chunks_tall}, "
            f"x={chunks_wide}"
        )

        print(
            f"PAD REMAINDER     : "
            f"y={pad_height % CHUNK_SIZE}, "
            f"x={pad_width % (CHUNK_SIZE * 2)} cols"
        )

        print("--------------------------------")

        print(
            f"PLAYER WORLD      : "
            f"({player_y:.3f}, {player_x:.3f})"
        )

        print(
            f"PLAYER CHUNK      : "
            f"({chunk_y}, {chunk_x})"
        )

        print(
            f"SCREEN TOP WORLD  : "
            f"({world_top_y:.3f}, {world_left_x:.3f})"
        )

        print(
            f"PAD TOP CHUNK     : "
            f"({top_cy}, {left_cx})"
        )

        print(
            f"PAD ORIGIN WORLD  : "
            f"({pad_origin_y}, {pad_origin_x})"
        )

        print(
            f"PAD OFFSET        : "
            f"({pad_offset_y}, {pad_offset_x})"
        )

        print(
            f"VIEWPORT WORLD    : "
            f"({viewport_world_y:.3f}, {viewport_world_x:.3f})"
        )

        print(
            f"SCREEN ERROR      : "
            f"({error_y:.3f}, {error_x:.3f})"
        )

        print("===============================")
        print()