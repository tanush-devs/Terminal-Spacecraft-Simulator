class Physics:
    
    def calculate(self, rocket, celestialbody_manager, dt, inputhandler):
        rocket.update_angle(inputhandler, dt)
        rocket.update_thrust(inputhandler, dt)
        R_ay,R_ax = rocket.get_thrust_acc()

        rocket.ay = R_ay
        rocket.ax = R_ax

        self.update_position(rocket, dt)
        self.stop_rocket(rocket, inputhandler)


    def update_position(self, rocket, dt):
        rocket.vy += rocket.ay * dt
        rocket.vx += rocket.ax * dt

        rocket.y += rocket.vy * dt
        rocket.x += rocket.vx * dt

    def stop_rocket(self, rocket, inputhandler):
        if inputhandler.stop_rocket:
            rocket.vy = 0
            rocket.vx = 0

            rocket.ax = 0
            rocket.ay = 0

            rocket.angular_velocity = 0
            rocket.angular_acceleration = 0

            rocket.thrust = 0