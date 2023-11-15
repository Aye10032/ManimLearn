from manim import *
from manim.utils.unit import Percent, Pixels
import numpy as np


class Positioning(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)

        red_dot = Dot(color=RED)
        green_dot = Dot(color=GREEN)
        green_dot.next_to(red_dot, RIGHT + UP)
        self.add(red_dot, green_dot)

        s = Square(color=ORANGE)
        s.shift(2 * UP + 4 * RIGHT)
        self.add(s)

        c = Circle(color=PURPLE)
        c.move_to(np.array([-3, -2, 0]))
        self.add(c)

        c2 = Circle(radius=0.5, color=RED, fill_opacity=0.5)
        c3 = c2.copy().set_color(YELLOW)
        c4 = c2.copy().set_color(ORANGE)
        c2.align_to(s, UP)
        c3.align_to(s, RIGHT)
        c4.align_to(s, UP + RIGHT)
        self.add(c2, c3, c4)


class CriticalPoints(Scene):
    def construct(self):
        c = Circle(color=BLUE, fill_opacity=0.5)
        self.add(c)

        for d in [(0, 0, 0), UP, DOWN, LEFT, RIGHT, UR, UL, DR, DL]:
            self.add(Cross(scale_factor=0.1).move_to(c.get_critical_point(d)))

        s = Square(color=RED, fill_opacity=0.2)
        s.move_to(np.array([1, 0, 0]), aligned_edge=LEFT)
        self.add(s)


class UsefulUnits(Scene):
    def construct(self):
        for perc in range(5, 40, 5):
            self.add(Circle(radius=perc * Percent(X_AXIS)))
            self.add(Square(side_length=perc * 2 * Percent(Y_AXIS), color=YELLOW))

        d = Dot()
        d.shift(100 * Pixels * RIGHT)
        self.add(d)


class Group(Scene):
    def construct(self):
        red_dot = Dot(color=RED)
        green_dot = Dot(color=GREEN).next_to(red_dot, UP)
        blue_dot = Dot(color=BLUE).next_to(red_dot, RIGHT)

        dot_group = VGroup(red_dot, green_dot, blue_dot)
        dot_group.to_edge(RIGHT)
        self.add(dot_group)

        circles = VGroup(*[Circle(radius=0.2) for _ in range(10)])
        circles.arrange(UP, buff=0)
        self.add(circles)

        stars = VGroup(*[Star(color=BLUE, fill_opacity=0.8).scale(0.2) for _ in range(20)])
        stars.arrange_in_grid(4, 5, buff=0.2)
        self.add(stars)
