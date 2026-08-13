from chunkmanager import ChunkManager
from rocket import Rocket


class AppState:
    def __init__(self):
        self.is_running = True
        self.target_fps = 300000000
        self.rocket = Rocket()
        self.chunk_manager = ChunkManager(seed=2009)