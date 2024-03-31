from typing import Optional

import numpy as np
from manim import *


class OpeningManim(Scene):
    def construct(self):
        title = Tex(r"This is some \LaTeX")
        basel = MathTex(
            r"\text{Attention}(Q,K,V) &= \text{softmax}\left(\frac{QK^T}{\sqrt{d}}+\mathbf A_{mask}\right)V")
        VGroup(title, basel).arrange(DOWN)
        self.play(FadeIn(title))
        self.play(Write(basel))
        self.wait()

        transform_title = Tex("That is a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel])
        )
        self.wait()

        grid = NumberPlane()
        grid_title = Tex(r"This is a grid")
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)
        self.play(
            FadeOut(title),
            FadeIn(grid_title, shift=UP),
            Create(grid, run_time=3, lag_ratio=0.1)
        )
        self.wait()

        grid.prepare_for_nonlinear_transform()

        def trans_func(p):
            return p + np.array([np.sin(p[1]), np.sin(p[0]), 0])

        self.play(grid.animate.apply_function(trans_func), run_time=3)
        self.wait()

        grid_transform_title = Tex(r"That was a non-linear function \\ applied to the grid")
        grid_transform_title.move_to(grid_title, UL)
        self.play(Transform(grid_title, grid_transform_title))
        self.wait()


class SineCurveUnitCircle(Scene):
    def __init__(self, **kwargs):
        Scene.__init__(self, **kwargs)
        self.curve: VGroup = VGroup()
        self.t_offset: float = 0
        self.origin_point = np.array([-4, 0, 0])
        self.curve_start = np.array([-3, 0, 0])
        self.circle: Optional[Mobject] = None

    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw()
        self.wait()

    def show_axis(self):
        x_start = np.array([-6, 0, 0])
        x_end = np.array([6, 0, 0])

        y_start = np.array([-4, -2, 0])
        y_end = np.array([-4, 2, 0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        # self.play(
        #     Create(x_axis),
        #     Create(y_axis)
        # )
        self.add(x_axis, y_axis)
        self.add_x_labels()

    def add_x_labels(self):
        x_labels = [
            MathTex(r"\pi"),
            MathTex(r"2 \pi"),
            MathTex(r"3 \pi"),
            MathTex(r"4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1 + 2 * i, 0, 0]), DOWN)
            self.play(Create(x_labels[i]), run_time=0.5)

    def show_circle(self):
        circle = Circle(radius=1)
        circle.move_to(self.origin_point)
        self.play(Create(circle))
        self.circle = circle

    def move_dot_and_draw(self):
        orbit = self.circle
        origin_point = self.origin_point

        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(orbit.point_from_proportion(0))
        rate = 0.25

        def go_around_circle(mob: Mobject, dt: float):
            self.t_offset += (dt * rate)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]

            return Line(dot.get_center(), np.array([x, y, 0]), color=YELLOW_A, stroke_width=2)

        self.curve.add(Line(self.curve_start, self.curve_start))

        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]

            new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=YELLOW)
            self.curve.add(new_line)

            return self.curve

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(orbit, origin_to_circle_line, dot_to_curve_line, sine_curve_line)

        dot.add_updater(go_around_circle)
        self.wait(8.5)
        dot.remove_updater(go_around_circle)
