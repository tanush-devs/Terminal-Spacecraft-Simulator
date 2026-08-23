import math


class EmojiDictionary:
    ROCKET_FACING_NORTH = "⬆ "
    ROCKET_FACING_NORTH_EAST = "↗ "
    ROCKET_FACING_EAST = "➡ "
    ROCKET_FACING_SOUTH_EAST = "↘ "
    ROCKET_FACING_SOUTH = "⬇ "
    ROCKET_FACING_SOUTH_WEST = "↙ "
    ROCKET_FACING_WEST = "⬅ "
    ROCKET_FACING_NORTH_WEST = "↖ "


class Rocket:

    def __init__(self):
        self.x = 16
        self.y = 16

        self.vx = 0
        self.vy = 0

        self.ax = 0
        self.ay = 0

        self.angle = 0
        self.angular_velocity = 0
        self.max_angular_velocity = 1
        self.angular_acceleration = 0

        self.thrust = 0
        self.Thrust_Buildup_Rate = 1
        self.Counter_Thrust_Buildup_Rate = 1
        self.max_thrust = 5
        self.max_counter_thrust = -3

        self.emoji = EmojiDictionary.ROCKET_FACING_NORTH

    def current_speed(self):
        return math.hypot(self.vx, self.vy)
    
    def current_acceleration(self):
        return math.hypot(self.ax, self.ay)

    def update_physics(self, dt, inputhandler):

        self.update_angle(inputhandler, dt)
        self.update_thrust(inputhandler, dt)
        self.update_accelaration()
        self.update_position(dt)

    def update_position(self, dt):
        self.vy += self.ay * dt
        self.vx += self.ax * dt

        self.y += self.vy * dt
        self.x += self.vx * dt

    def update_angle(self, inputhandler, dt):
        if inputhandler.rotate_right:
            # self. angle = (2*math.pi / 8)
            self.angular_acceleration = 0.3
        elif inputhandler.rotate_left:
            # self. angle = (10*math.pi / 8)
            self.angular_acceleration = -0.3
        else:
            self.angular_acceleration = 0.0

        new_vel = self.angular_velocity + (self.angular_acceleration * dt)
        self.angular_velocity = max(
    min(new_vel, self.max_angular_velocity),
    -self.max_angular_velocity
)

        self.angle += self.angular_velocity * dt
        self.angle = self.angle % (2 * math.pi)

        self.update_rocket_emoji()

    def update_rocket_emoji(self):
        if (15*math.pi / 8) < self.angle < (math.pi / 8) :
            self.emoji = EmojiDictionary.ROCKET_FACING_NORTH

        elif (math.pi / 8) < self.angle < (3*math.pi / 8):
            self.emoji = EmojiDictionary.ROCKET_FACING_NORTH_EAST

        elif (3*math.pi / 8) < self.angle < (5*math.pi / 8):
            self.emoji = EmojiDictionary.ROCKET_FACING_EAST

        elif (5*math.pi / 8) < self.angle < (7*math.pi / 8):
            self.emoji = EmojiDictionary.ROCKET_FACING_SOUTH_EAST

        elif (7*math.pi / 8) < self.angle < (9*math.pi / 8):
            self.emoji = EmojiDictionary.ROCKET_FACING_SOUTH

        elif (9*math.pi / 8) < self.angle < (11*math.pi / 8):
            self.emoji = EmojiDictionary.ROCKET_FACING_SOUTH_WEST

        elif (11*math.pi / 8) < self.angle < (13*math.pi / 8):
            self.emoji = EmojiDictionary.ROCKET_FACING_WEST

        elif (13*math.pi / 8) < self.angle < (15*math.pi / 8):
            self.emoji = EmojiDictionary.ROCKET_FACING_NORTH_WEST

    def update_accelaration(self):
        theta = self.angle
        dx = math.sin(theta)
        dy = math.cos(theta)
        
        self.ax = self.thrust * dx
        self.ay = -(self.thrust * dy)

    def update_thrust(self, inputhandler, dt):
        new_thrust = self.thrust
    
        if inputhandler.thrust_increase:
            new_thrust += self.Thrust_Buildup_Rate * dt
        if inputhandler.thrust_decrease:
            new_thrust -= self.Counter_Thrust_Buildup_Rate * dt

        self.thrust = max(
            min(new_thrust, self.max_thrust),
            self.max_counter_thrust
        )
