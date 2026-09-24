import math

LINES_TO_SCROLL = 1

class Telementary:
    
    def __init__(self):
        self.max_offset = 0
        self.scroll_offset = 0
    
    def get_telementary_data(self, appstate, world):
        rocket = appstate.rocket

        nearest_planet_dis = world.celestialbody_manager.nearest_body(rocket.y,rocket.x)
        if nearest_planet_dis is None:
            nearest_planet_dis = "Unknown"
        else:
            nearest_planet_dis = round(nearest_planet_dis,3)
        chunk_y, chunk_x, *_ = (
        world.chunk_manager.world_to_chunk_coords(
            rocket.y,
            rocket.x
        )
    )
        return {
        "GAME": {
            "FPS": appstate.current_fps
        },
        "POSITION": {
            "X": round(rocket.x, 3),
            "Y": round(-rocket.y, 3),
        },

        "VELOCITY": {
            "X": round(rocket.vx, 3),
            "Y": round(-rocket.vy, 3),
            "Speed": round(rocket.current_speed(), 3),
        },

        "ACCELERATION": {
            "X": round(rocket.ax, 3),
            "Y": round(-rocket.ay, 3),
            "Magnitude": round(rocket.current_acceleration(), 3),
        },
        "ORIENTATION":{
            "Angle": round(math.degrees(rocket.angle), 2),
            "Angular":"",
            "  Velocity": round(math.degrees(rocket.angular_velocity), 2),
            "  Accelaration": round(math.degrees(rocket.angular_acceleration), 2),
        },

        "GENERAL": {
            "Thrust": round(rocket.thrust, 3),
            "Chunk": (chunk_x, -chunk_y),
        },
        "PLANETS": {
            "Nearest" : nearest_planet_dis,
            "Total": len(world.celestialbody_manager.celestialbodies)
        },
    }

    def get_display_list(self, appstate, world, width):
        data = self.get_telementary_data(appstate, world)
        display_list = ["\t◈ TELEMETRY","─"*(width-2)]
        for section,fields in data.items():
            display_list.append(section)
            for field,value in fields.items():
                display_list.append(f"    {field}: {value}")            
            display_list.append("")
            
        return display_list

    def scroll(self, x, y, dx, dy):
        self.scroll_offset = max(
            0,
            min(self.scroll_offset - dy, self.max_offset)
        )
