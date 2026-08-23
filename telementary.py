import math


LINES_TO_SCROLL = 1

class Telementary:
    
    def __init__(self):
        self.max_offset = 0
        self.scroll_offset = 0
    
    def get_telementary_data(self,appstate):
        rocket = appstate.rocket
        
        chunk_y, chunk_x, *_ = (
        appstate.chunk_manager.world_to_chunk_coords(
            rocket.y,
            rocket.x
        )
    )
        return {
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
    }

    def get_display_list(self,appstate,width):
        data = self.get_telementary_data(appstate)
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
