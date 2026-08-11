import math


class Camera:
    def __init__(self, screen_h, screen_w):
        self.screen_h = screen_h
        self.screen_w = screen_w
        
    def update_size(self, screen_h, screen_w):
        self.screen_h = screen_h
        self.screen_w = screen_w


    def get_view_bounds(self, player_y, player_x):
        desired_y = self.screen_h // 2
        desired_x = self.screen_w // 4

        top_y = math.floor(player_y) - desired_y
        left_x = math.floor(player_x) - desired_x
        
        return(top_y,left_x)