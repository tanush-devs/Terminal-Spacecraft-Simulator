import math
import random

CHUNK_SIZE = 32



class item_map:
    # Tile IDs
    TILE_EMPTY = 0
    TILE_STAR = 1
    TILE_ASTEROID = 2


    TILE_MAP = {  # noqa: RUF012
        TILE_EMPTY: "  ",
        TILE_STAR: " ^",
        TILE_ASTEROID: " ▀",
    }
class ChunkManager:
    def __init__(self, seed = 2009):
        self.seed = seed
        self.chunks = {}
        self.modifications = {}
        self.last_cy = None
        self.last_cx = None
        
    def _get_or_create_chunk(self, cy, cx):
        key = (cy, cx)

        if key not in self.chunks:
            self.chunks[key] = self._generate_chunk(cy, cx)

        return self.chunks[key]

    def world_to_chunk_coords(self,world_y, world_x):
        """Generates Chunk and local coordinates from world coords"""
        iy = math.floor(world_y)
        ix = math.floor(world_x)

        chunk_y = iy // CHUNK_SIZE
        chunk_x = ix // CHUNK_SIZE

        local_y = iy % CHUNK_SIZE
        local_x = ix % CHUNK_SIZE
        
        return chunk_y, chunk_x, local_y, local_x

    def _generate_chunk(self, cy, cx):
        """Procedural star/asteroid generator per chunk."""

        rng = random.Random(hash((self.seed, cy, cx)))

        grid = [[item_map.TILE_EMPTY for _ in range(CHUNK_SIZE)] for _ in range(CHUNK_SIZE)]
        for y in range(CHUNK_SIZE):
            for x in range(CHUNK_SIZE):
                roll = rng.random()
                if roll < 0.0005:
                    grid[y][x] = item_map.TILE_STAR  # star
                elif roll < 1:
                    grid[y][x] = item_map.TILE_ASTEROID  # Asteroid
        return grid

    def update_active_chunks(self, appstate, radius_y, radius_x):
        py, px = appstate.rocket.position
        
        center_cy, center_cx, *_ = self.world_to_chunk_coords(py, px)
        
        min_cy = center_cy - radius_y
        max_cy = center_cy + radius_y
        min_cx = center_cx - radius_x
        max_cx = center_cx + radius_x
        
        if self.last_cy is None or self.last_cx is None:      # if loaded first time
            for cy in range(min_cy, max_cy + 1):
                for cx in range(min_cx, max_cx + 1):
                    _ = self._get_or_create_chunk(cy, cx)
                    
            self.last_cy = center_cy
            self.last_cx = center_cx
            return

        delta_cy = center_cy - self.last_cy
        delta_cx = center_cx - self.last_cx
        
        if abs(delta_cx) > 1 or abs(delta_cy) > 1:
            # Trigger a full reload fallback instead of single-edge delta shifting
            self.last_cy = None
            self.last_cx = None
            self.update_active_chunks(appstate, radius_y, radius_x)
            return

        if delta_cy == 1:
            self._load_row(max_cy, min_cx, max_cx)

        elif delta_cy == -1:
            self._load_row(min_cy, min_cx, max_cx)

        if delta_cx == 1:
            self._load_column(max_cx, min_cy, max_cy)

        elif delta_cx == -1:
            self._load_column(min_cx, min_cy, max_cy)


    def _load_column(self, cx, min_cy, max_cy):
        for cy in range(min_cy, max_cy + 1):
            self._get_or_create_chunk(cx, cy)

    def _unload_column(self, cx, min_cy, max_cy):
        for cy in range(min_cy, max_cy + 1):
            self.chunks.pop((cx, cy), None)

    def _load_row(self, cy, min_cx, max_cx):
        for cx in range(min_cx, max_cx + 1):
            self._get_or_create_chunk(cx, cy)

    def _unload_row(self, cy, min_cx, max_cx):
        for cx in range(min_cx, max_cx + 1):
            self.chunks.pop((cx, cy), None)
            
    def get_tile(self, world_y, world_x):
        cy, cx, ly, lx = self.world_to_chunk_coords(world_y, world_x)

        chunk = self.chunks.get((cy, cx))

        if chunk is not None:
            return chunk[ly][lx]  # Returns integer ID (0, 1, 2, etc.)

        return item_map.TILE_EMPTY  # Default fallback if out of bounds

    def get_row_lis(self, cy, cx, line):
        default_chunk = [[item_map.TILE_EMPTY] * CHUNK_SIZE for _ in range(CHUNK_SIZE)]
        chunk = self.chunks.get((cy, cx), default_chunk)

        return chunk[line]