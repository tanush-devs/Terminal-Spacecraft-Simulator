from pynput import keyboard
import os

class InputHandler:
    def __init__(self, appstate):
        self.game_is_running = True
        self.rotate_right = False
        self.rotate_left = False
        self.thrust_increase = False
        self.thrust_decrease = False
        self.counter_thrust = False
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        

    def poll_action(self):
        self.listener.start()


    def on_press(self,key):
        if getattr(key, 'char', None) in ['w','W']:
            self.thrust_increase = True

        if getattr(key, 'char', None) in ['s','S']:
            self.thrust_decrease = True

        if getattr(key, 'char', None) in ['x','X']:
            self.counter_thrust = True

        if getattr(key, 'char', None) in ['a','A']:
            self.rotate_left = True

        if getattr(key, 'char', None) in ['d','D']:
            self.rotate_right = True


        if key == keyboard.Key.esc:
            self.game_is_running = False

    def on_release(self,key):
        if getattr(key, 'char', None) in ['w','W']:
            self.thrust_increase = False

        if getattr(key, 'char', None) in ['s','S']:
            self.thrust_decrease = False

        if getattr(key, 'char', None) in ['x','X']:
            self.counter_thrust = False

        if getattr(key, 'char', None) in ['a','A']:
            self.rotate_left = False

        if getattr(key, 'char', None) in ['d','D']:
            self.rotate_right = False

        if key == keyboard.Key.esc:
            os._exit(0)