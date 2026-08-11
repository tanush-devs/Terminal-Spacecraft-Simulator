import math


class Rocket:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.angle = 0
        self.angular_velocity = 0
        self.thrust = 0
        self.max_thrust = 0
        self.emoji = "▲ "
        
    @property
    def position(self):
        return (self.y,self.x)
    
    @position.setter
    def position(self,pos):
        self.y , self.x = pos
    
    def current_speed(self):
        return math.hypot(self.vx, self.vy)
    
    def current_accelaration(self):
        return math.hypot(self.ax, self.ay)
    
    def get_display_position(self):
        return (-self.y,self.x)
    
    def update_position(self , dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        self.x += self.vx * dt
        self.y += self.vy * dt
        