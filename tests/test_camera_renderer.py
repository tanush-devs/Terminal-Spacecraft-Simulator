import unittest

from appstate import AppState
from camera import Camera
from chunkmanager import CHUNK_SIZE
from rendering import Renderer


class TestCamera(unittest.TestCase):
    
    def setUp(self):
        self.appstate = AppState()
        self.renderer = Renderer()
        self.camera = Camera()
        self.appstate.rocket.x = 16
        self.appstate.rocket.y = 16
        self.renderer.pad_h = CHUNK_SIZE * 3
        self.renderer.pad_w = CHUNK_SIZE * 3 * 2
        self.renderer.screen_h = CHUNK_SIZE
        self.renderer.screen_w = CHUNK_SIZE * 2
    
    def test_top_chunks(self):
        self.assertEqual(self.camera.get_pad_top_chunk(self.appstate,self.renderer),(-1,-1, self.renderer.pad_h, 3))
        self.appstate.rocket.x = 48
        self.appstate.rocket.y = 48
        self.assertEqual(self.camera.get_pad_top_chunk(self.appstate,self.renderer),(0,0, self.renderer.pad_h, 3))

    def test_view_bound(self):
        self.appstate.rocket.x = 16
        self.appstate.rocket.y = 16
        self.camera.pad_top_chunk = -1
        self.camera.pad_left_chunk = -1
        expected_output = (CHUNK_SIZE, CHUNK_SIZE*2, self.renderer.screen_h // 2, self.renderer.screen_w // 2)
        self.assertEqual(self.camera.get_view_bounds(self.appstate,self.renderer), expected_output)

        self.appstate.rocket.y = 20
        self.appstate.rocket.x = 20
        expected_output = (CHUNK_SIZE + 4, CHUNK_SIZE*2 + 8, self.renderer.screen_h // 2, self.renderer.screen_w // 2)
        self.assertEqual(self.camera.get_view_bounds(self.appstate,self.renderer), expected_output)
        
        self.appstate.rocket.y = 10
        self.appstate.rocket.x = 10
        expected_output = (CHUNK_SIZE - 6, CHUNK_SIZE*2 - 12, self.renderer.screen_h // 2, self.renderer.screen_w // 2)
        self.assertEqual(self.camera.get_view_bounds(self.appstate,self.renderer), expected_output)