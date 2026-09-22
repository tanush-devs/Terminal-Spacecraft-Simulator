import curses
import math
import random
import time

from chunkmanager import CHUNK_SIZE
from colors import PLANET_COLORS

REGION_SIZE = 2500

class CelestialBody:
    def __init__(self, y,x, radius, mass, color=30):
        self.y = y
        self.x = x
        self.radius = radius
        self.mass = mass
        self.box = "██"
        self.color = color

    def get_covered_coordinates(self, top_cy, left_cx, pad_h, pad_w):
        top_y = top_cy*CHUNK_SIZE
        left_x = left_cx*CHUNK_SIZE
        bottom_y= top_y+pad_h
        right_x= left_x+pad_w

        start_y = max(self.y - self.radius, top_y)
        end_y   = min(self.y + self.radius, bottom_y)

        planet_dict = {}
        
        for y in range(start_y, end_y + 1):
            half_chord = math.sqrt(self.radius**2 - abs(y - self.y)**2)
            chord_l = min(self.x + half_chord, right_x) - max(self.x - half_chord,left_x)
            planet_dict[(y, max(self.x - half_chord, left_x))] = self.box * int(chord_l)

        return planet_dict

    def get_dis(self, py,px):
        dis = math.sqrt((self.y - py)**2 + (self.x - px)**2)
        return dis
    
    def is_colliding(self, py,px):
        return self.get_dis(py,px) < self.radius


class CelestialBodyManager:
    LOADED_DIS = 5000

    def __init__(self, seed):
        self.seed = seed
        self.celestialbodies = {}
        self.current_region = None
        self.region_changed = False
        self.last_update = time.perf_counter()

    def add(self, y,x, radius, mass, color):
        self.celestialbodies[y,x] = (CelestialBody(y,x, radius, mass, color))

    def generate_celestial_body(self):
        if self.current_region is None:
            return
        
        planet_exists = False

        rng = random.Random(hash((self.seed, self.current_region)))
        roll = rng.random()
        if roll < 0.5:
            planet_exists = True
        else:
            return
        
        if planet_exists:
            body_y = self.current_region[0] * REGION_SIZE + rng.randint(0, REGION_SIZE-250)
            body_x = self.current_region[1] * REGION_SIZE + rng.randint(0, REGION_SIZE - 250)

            radius = rng.randint(20, 60)
            density = rng.uniform(0.5,1.5)

            mass = density * (4/3) * math.pi * radius**3
            
            color = rng.randint(30, 30+len(PLANET_COLORS))

            self.add(body_y,body_x,radius,mass,color)

    def process_celestialbodies(self, py,px):
        if self.region_changed:
            self.generate_celestial_body()

        if self.last_update > 1:
            self.celestialbodies = {key: body for key,body in self.celestialbodies.items() if (body.y - py)**2 + (body.x - px)**2 < self.LOADED_DIS**2 and (body.y*REGION_SIZE,body.x*REGION_SIZE) != self.current_region}
            self.last_update = time.perf_counter()

    def render_celestialbodies(self, renderer, top_cy, left_cx, pad_h, pad_w, py,px):
        active_bodies = [body for body in self.celestialbodies.values() if (body.y - py)**2 + (body.x - px)**2 < (renderer.pad_h+ body.radius)**2 + (renderer.pad_w+ body.radius)**2 ]

        for body in active_bodies:
            planet_dict = body.get_covered_coordinates(top_cy, left_cx, pad_h, pad_w)

            for coord,line in planet_dict.items():
                pad_y,pad_x = renderer.camera.get_relative_pad_coordinates(coord[0],coord[1], renderer)
                
                if pad_y is None or pad_x is None:
                    continue

                try:
                    renderer.viewport.addstr(pad_y, pad_x, line, curses.color_pair(body.color))
                except curses.error:  
                    pass  # Ignores the harmless bottom-right overflow error

    def nearest_body(self, py,px):
        min_dis = None
        for body in self.celestialbodies.values():
            dis = math.sqrt((body.y - py)**2 + (body.x - px)**2)
            if min_dis is None or dis < min_dis:
                min_dis = dis

        return min_dis

    def check_or_process_collision(self, rocket):
            for body in self.celestialbodies.values():
                if body.is_colliding(rocket.y, rocket.x):

                    dx = rocket.x - body.x
                    dy = rocket.y - body.y
                    
                    
                    distance = math.sqrt(dx**2 + dy**2)

                    if distance == 0: 
                        continue

                    dj = dy / distance     # unit vectors from centre to player
                    di = dx / distance

                    nx = dx / distance
                    ny = dy / distance

                    vel_along_normal = (rocket.vx * nx) + (rocket.vy * ny)

                    if vel_along_normal < 0:

                        rocket.vx -= vel_along_normal * nx
                        rocket.vy -= vel_along_normal * ny
                    
                    rocket.y = body.y + dj * body.radius
                    rocket.x = body.x + di * body.radius

