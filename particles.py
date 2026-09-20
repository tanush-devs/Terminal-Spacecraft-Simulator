import curses
import random


class Particle:
    def __init__(self, y,x, vy,vx, lifetime=4, color=1, age=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.age = age
        self.character = " ."
        self.color = color
        self.exists = True

    def update(self, dt):
        self.age += dt

        self.x += self.vx*dt
        self.y += self.vy*dt

        if self.age>self.lifetime:
            self.exists = False

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add(self, particle):
        self.particles.append(particle)

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)

        self.particles = [particle for particle in self.particles if particle.exists]

    def render_particles(self, renderer):
        for particle in self.particles:
            par_y,par_x = renderer.camera.get_relative_coordinates(particle.y,particle.x, renderer.screen_h, renderer.screen_w)
            
            if par_y is not None and par_x is not None and particle.exists:
                renderer.overlay.addstr(
                    par_y,
                    par_x,
                    particle.character,
                    curses.color_pair(particle.color)
                )

    def emit(self, y, x, vy, vx, lifetime, count=1, color=1, spread=1):  # 1 - defailt color
        for _ in range(count):
            particle_vy = random.uniform(vy - spread, vy + spread)
            particle_vx = random.uniform(vx - spread, vx + spread)
            particle_lifetime = lifetime + random.uniform(-0.5, 0.5)

            self.add(
                Particle(y, x, particle_vy, particle_vx, particle_lifetime, color)
            )