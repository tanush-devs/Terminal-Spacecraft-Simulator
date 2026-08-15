import math
import random
import time

CHUNK_SIZE = 32



class item_map:
    # Tile IDs
    TILE_EMPTY = 0
    TILE_STAR = 1
    TILE_ASTEROID = 2


    TILE_MAP = {  # noqa: RUF012
        TILE_EMPTY: "  ",
        TILE_STAR: " *",
        TILE_ASTEROID: " ▀",
    }
class ChunkManager:
    RADIUS_Y = 10
    RADIUS_X = 10
    CLEANUP_INTERVAL = 5

    def __init__(self, seed = 2009):
        self.seed = seed
        self.chunks = {}
        self.modifications = {}
        self.last_cleanup_cy = None
        self.last_cleanup_cx = None

    def _get_or_create_chunk(self, cy, cx):
        key = (cy, cx)

        if key not in self.chunks:
            self.chunks[key] = self._generate_chunk(cy, cx)

        return self.chunks[key]
    
    def _get_or_create_testing_chunk(self, cy, cx):
        key = (cy, cx)

        if key not in self.chunks:
            self.chunks[key] = self._generate_testing_chunk(cy, cx)

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
                if roll < 0.0004:
                    grid[y][x] = item_map.TILE_STAR  # star
                elif roll < 0.0008:
                    grid[y][x] = item_map.TILE_ASTEROID  # Asteroid
        return grid

    def _generate_testing_chunk(self, cy, cx):
        """Procedural star/asteroid generator per chunk."""
        grid = [
            [
                item_map.TILE_ASTEROID if i == CHUNK_SIZE - 1 else item_map.TILE_EMPTY
                for i in range(CHUNK_SIZE)
            ]
            for _ in range(CHUNK_SIZE)
        ]
        tmp = [item_map.TILE_ASTEROID for _ in range(CHUNK_SIZE)]
        grid[CHUNK_SIZE - 1] = tmp
        grid[0][0] = f"tile_{cy}"
        grid[1][0] = f"tile_{cx}"

        item_map.TILE_MAP[f"tile_{cy}"] = str(cy)
        item_map.TILE_MAP[f"tile_{cx}"] = str(cx)
        return grid

    def update_active_chunks(self,current_cy,current_cx):
        
        if self.last_cleanup_cy is None or self.last_cleanup_cx is None:
            update_pad_status = True
        else:
            update_pad_status = (abs(current_cy - self.last_cleanup_cy) >= self.CLEANUP_INTERVAL or abs(current_cx - self.last_cleanup_cx) >= self.CLEANUP_INTERVAL)
        
        if update_pad_status:
            start = time.perf_counter()
            min_cy = current_cy - self.RADIUS_Y
            max_cy = current_cy + self.RADIUS_Y
            min_cx = current_cx - self.RADIUS_X
            max_cx = current_cx + self.RADIUS_X

            loaded_chunks = {(cy, cx) for cy in range(min_cy, max_cy + 1) for cx in range(min_cx, max_cx + 1)}

            to_remove = [key for key in self.chunks if key not in loaded_chunks]

            for key in to_remove:
                self.chunks.pop(key, None)
            
            self.last_cleanup_cy = current_cy
            self.last_cleanup_cx = current_cx


    def get_tile(self, world_y, world_x):
        cy, cx, ly, lx = self.world_to_chunk_coords(world_y, world_x)

        chunk = self.chunks.get((cy, cx))

        if chunk is not None:
            return chunk[ly][lx]  # Returns integer ID (0, 1, 2, etc.)

        return item_map.TILE_EMPTY  # Default fallback if out of bounds
    

    def get_row_lis(self, cy, cx, line):
        chunk = self._get_or_create_chunk(cy,cx)

        return chunk[line]
    
    def get_row_lis_testing(self, cy, cx, line):
        chunk = self._get_or_create_testing_chunk(cy,cx)

        return chunk[line]