from pynput import keyboard, mouse


class InputHandler:
    def __init__(self, renderer):
        self.game_is_running = True
        self.rotate_right = False
        self.rotate_left = False
        self.thrust_increase = False
        self.thrust_decrease = False
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.mouse_listener = mouse.Listener(on_scroll= renderer.telementary.scroll)
        self.stop_rocket = False


    def poll_action(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()


    def on_press(self,key):
        if getattr(key, 'char', None) in ['w','W']:
            self.thrust_increase = True

        if getattr(key, 'char', None) in ['s','S']:
            self.thrust_decrease = True

        if getattr(key, 'char', None) in ['a','A']:
            self.rotate_left = True

        if getattr(key, 'char', None) in ['d','D']:
            self.rotate_right = True

        if getattr(key, 'char', None) in ['l','L']:
            self.stop_rocket = True
            

        if key == keyboard.Key.esc:
            self.game_is_running = False

    def on_release(self,key):
        if getattr(key, 'char', None) in ['w','W']:
            self.thrust_increase = False

        if getattr(key, 'char', None) in ['s','S']:
            self.thrust_decrease = False

        if getattr(key, 'char', None) in ['a','A']:
            self.rotate_left = False

        if getattr(key, 'char', None) in ['d','D']:
            self.rotate_right = False

        if getattr(key, 'char', None) in ['l','L']:
            self.stop_rocket = False

        if key == keyboard.Key.esc:
            self.game_is_running = False