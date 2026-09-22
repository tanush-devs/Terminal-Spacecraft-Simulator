from rocket import Rocket


class AppState:
    def __init__(self):
        self.is_running = True
        self.target_fps = 99999999
        self.rocket = Rocket()
        self.current_fps = 0