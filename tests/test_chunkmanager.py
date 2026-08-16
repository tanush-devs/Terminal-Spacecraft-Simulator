import unittest

from chunkmanager import CHUNK_SIZE, ChunkManager, item_map


class TestChunkCoordinates(unittest.TestCase):
    
    def setUp(self):
        self.chunk_manager = ChunkManager(seed=2026)
        
    def test_world_to_chunk_coords(self):
        self.assertEqual(self.chunk_manager.world_to_chunk_coords(1,31), (0,0, 1,31))
        self.assertEqual(self.chunk_manager.world_to_chunk_coords(31,31), (0,0, 31,31))
        self.assertEqual(self.chunk_manager.world_to_chunk_coords(1,32), (0,1, 1,0))
        self.assertEqual(self.chunk_manager.world_to_chunk_coords(32,32), (1,1, 0,0))
        self.assertEqual(self.chunk_manager.world_to_chunk_coords(0,0), (0,0, 0,0))
        self.assertEqual(self.chunk_manager.world_to_chunk_coords(-1,31), (-1,0, 31,31))
        self.assertEqual(self.chunk_manager.world_to_chunk_coords(-1,-1), (-1,-1, 31,31))
        self.assertEqual(self.chunk_manager.world_to_chunk_coords(-33,-33), (-2,-2, 31,31))
        self.assertEqual(self.chunk_manager.world_to_chunk_coords(-32,-32), (-1,-1, 0,0))


class TestChunkGeneration(unittest.TestCase):
    def setUp(self):
        self.manager1 = ChunkManager(seed=2026)
        self.manager2 = ChunkManager(seed=2026)
        self.manager3 = ChunkManager(seed=2025)
        

    def test_generate_chunk_same_seed(self):
        chunk1 = self.manager1._generate_chunk(2, 2)
        chunk2 = self.manager2._generate_chunk(2, 2)

        self.assertEqual(chunk1, chunk2)


    def test_generate_chunk_different_seed(self):
        chunk1 = self.manager1._generate_chunk(2, 2)
        chunk2 = self.manager3._generate_chunk(2, 2)

        self.assertNotEqual(chunk1, chunk2)


    def test_generate_chunk_valid_tiles(self):
        chunk = self.manager1._generate_chunk(4, 8)
        tiles = [tile for row in chunk for tile in row]

        for tile in tiles:
            self.assertIn(tile, item_map.TILE_MAP)


    def test_generate_chunk_dimensions(self):
        chunk = self.manager1._generate_chunk(4, 8)

        self.assertEqual(len(chunk), CHUNK_SIZE)

        for row in chunk:
            self.assertEqual(len(row), CHUNK_SIZE)


class TestChunkLazyGeneration(unittest.TestCase):
    
    def setUp(self):
        self.manager = ChunkManager(seed=2009)
    
    def test_does_not_generate_existing_chunks(self):
        '''No new chunks should be generated until the current one is ungenerated'''
        cy = 124
        cx = 123
        self.manager._get_or_create_chunk(cy, cx)
        self.assertEqual(len(self.manager.chunks), 1)
        
        self.manager._get_or_create_chunk(cy, cx)
        self.assertEqual(len(self.manager.chunks), 1)
        
        self.manager._get_or_create_chunk(cy, cx)
        self.assertEqual(len(self.manager.chunks), 1)
        
    def test_generates_missing_chunks_as_needed(self):
        '''New chunks should be generated if they arent currently loaded'''
        self.manager._get_or_create_chunk(123,241)
        self.assertEqual(len(self.manager.chunks), 1)
        
        self.manager._get_or_create_chunk(12,21541)
        self.assertEqual(len(self.manager.chunks), 2)
        
        self.manager._get_or_create_chunk(1224, 124)
        self.assertEqual(len(self.manager.chunks), 3)

class TestRowAccess(unittest.TestCase):

    def setUp(self):
        self.manager = ChunkManager(seed= 2009)

    def test_row_length(self):
        row = self.manager.get_row_list(231,1241,7)
        self.assertEqual(len(row), CHUNK_SIZE)
        
    def test_correct_row(self):
        cy = 12412
        cx =631
        line = 4

        chunk = self.manager._generate_chunk(cy,cx)
        row = self.manager.get_row_list(cy,cx,line)
        
        self.assertEqual(row,chunk[line])
        
    def test_invalid_line_raises(self):
        line_1 = CHUNK_SIZE + 5
        line_2 = -4

        with self.assertRaises(ValueError):
            self.manager.get_row_list(322,412, line_1)
        
        with self.assertRaises(ValueError):
            self.manager.get_row_list(322,412, line_2)
    
class TestTileAccess(unittest.TestCase):
    
    def setUp(self):
        self.manager = ChunkManager(seed = 2009)
        
    def test_get_tile_returns_correct_tile(self):
        cy = 12
        cx = 141
        ly = 11
        lx = 12
        
        world_y = cy * CHUNK_SIZE + ly
        world_x = cx * CHUNK_SIZE + lx

        self.manager._get_or_create_chunk(cy,cx)
        expected_tile = item_map.TILE_ADMIN
        self.manager.chunks[(cy,cx)][ly][lx] = expected_tile

        actual_tile = self.manager.get_tile(world_y,world_x)

        self.assertEqual(actual_tile,expected_tile)

    def test_get_tile_generates_missing_chunk(self):
        cy = 1214
        cx = 839
        ly = 11
        lx = 12

        world_y = cy * CHUNK_SIZE + ly
        world_x = cx * CHUNK_SIZE + lx

        self.assertNotIn((cy, cx), self.manager.chunks)

        tile = self.manager.get_tile(world_y, world_x)

        self.assertIn((cy, cx), self.manager.chunks)
        self.assertIn(tile, item_map.TILE_MAP)


    def test_get_tile_is_consistent(self):
        cy = 12
        cx = 141
        ly = 11
        lx = 12

        world_y = cy * CHUNK_SIZE + ly
        world_x = cx * CHUNK_SIZE + lx
        
        self.manager._get_or_create_chunk(cy,cx)
        self.manager.chunks[(cy,cx)][ly][lx] = item_map.TILE_ADMIN

        first_tile = self.manager.get_tile(world_y, world_x)
        second_tile = self.manager.get_tile(world_y, world_x)

        self.assertEqual(first_tile, second_tile)

class UnloadingChunks(unittest.TestCase):
    
    def setUp(self):
        self.manager = ChunkManager(seed = 8122009)
        
    def test_nearby_chunks_remain(self):
        current_cy = 0
        current_cx = 0

        radius_y = self.manager.RADIUS_Y
        radius_x = self.manager.RADIUS_X

        # Populate all the chunks in radius
        keys = [
    (0, 0),
    (radius_y, radius_x),
    (radius_y, -radius_x),
    (-radius_y, radius_x),
    (-radius_y, -radius_x),
    (0, radius_x),
    (0, -radius_x),
    (radius_y, 0),
    (-radius_y, 0),
]

        for key in keys:
            self.manager.chunks[key] = None

        # change last update chunk to trigger update
        self.manager.last_cleanup_cx = current_cy + 61
        self.manager.last_cleanup_cy = current_cx + 41
        self.manager.unload_inactive_chunks(current_cy,current_cx)

        for key in keys:
            self.assertIn(key, self.manager.chunks)


    def test_farther_chunks_unload(self):
        current_cy = 0
        current_cx = 0

        radius_y = self.manager.RADIUS_Y
        radius_x = self.manager.RADIUS_X

        # Populate chunks withing + outside the radius
        keys = [
            (radius_y + 1, radius_x + 1),
            (radius_y + 1, -radius_x-1),
            (-radius_y-1, radius_x+1),
            (-radius_y-1, -radius_x-1),
            (0, radius_x+1),
            (0, -radius_x-1),
            (radius_y+1, 0),
            (-radius_y-1, 0),
        ]
        
        for key in keys:
            self.manager.chunks[key] = None

        # change last update chunk to trigger update
        self.manager.last_cleanup_cx = current_cy + 61
        self.manager.last_cleanup_cy = current_cx + 41
        self.manager.unload_inactive_chunks(current_cy,current_cx)

        for key in keys:
            self.assertNotIn(key, self.manager.chunks)
    
    def test_does_not_run_before_interval_is_reached(self):
        current_cy = 0
        current_cx = 0

        radius_y = self.manager.RADIUS_Y
        radius_x = self.manager.RADIUS_X
        cleanup_interval = self.manager.CLEANUP_INTERVAL

        # Populate all the chunks in radius
        keys = [
            (0, 0),
            (radius_y, radius_x),
            (radius_y, -radius_x),
            (-radius_y, radius_x),
            (-radius_y, -radius_x),
            (0, radius_x),
            (0, -radius_x),
            (radius_y, 0),
            (-radius_y, 0),
            (radius_y + 1, radius_x + 1),
            (radius_y + 1, -radius_x-1),
            (-radius_y-1, radius_x+1),
            (-radius_y-1, -radius_x-1),
            (0, radius_x+1),
            (0, -radius_x-1),
            (radius_y+1, 0),
            (-radius_y-1, 0),
        ]

        for key in keys:
            self.manager.chunks[key] = None

        # change last update chunk to not trigger update < cleanup interval
        self.manager.last_cleanup_cy = current_cy + cleanup_interval - 1
        self.manager.last_cleanup_cx = current_cx + cleanup_interval - 3
        self.manager.unload_inactive_chunks(current_cy,current_cx)

        self.manager.last_cleanup_cy = current_cy - cleanup_interval + 3
        self.manager.last_cleanup_cx = current_cx - cleanup_interval + 2
        self.manager.unload_inactive_chunks(current_cy,current_cx)


        for key in keys:
            self.assertIn(key, self.manager.chunks)


