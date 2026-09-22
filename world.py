from math import floor

from celestial_body import REGION_SIZE, CelestialBodyManager
from chunkmanager import ChunkManager


class World:
    def __init__(self):
        self.seed = 2009
        self.chunk_manager = ChunkManager(self.seed)
        self.celestialbody_manager = CelestialBodyManager(self.seed)
        

    def check_region(self, py,px):
        celestial_region = (floor(py / REGION_SIZE), floor(px / REGION_SIZE))
        if self.celestialbody_manager.current_region != celestial_region:
            self.celestialbody_manager.region_changed = True
            self.celestialbody_manager.current_region = celestial_region
