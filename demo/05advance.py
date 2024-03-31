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
