from chunkmanager import ChunkManager
from rocket import Rocket


class AppState:
    def __init__(self):
        self.is_running = True
        self.target_fps = 9999999
        self.print_values = False
        self.rocket = Rocket()
        self.chunk_manager = ChunkManager(seed=2009)