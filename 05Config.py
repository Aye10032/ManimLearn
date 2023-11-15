from manim import *

config.background_color = WHITE
config.frame_width = 16
config.frame_height = 9


class TestConfig(Scene):
    def construct(self):
        plane = NumberPlane()
        triangle = Triangle(color=BLUE, fill_opacity=0.8)
        self.add(plane, triangle)
        self.add(Text('测试'))
