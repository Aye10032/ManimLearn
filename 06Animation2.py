from manim import *
import numpy as np
from manim import Circle


class BasicAnimation(Scene):
    def construct(self):
        colors = color_gradient([BLUE, RED], 5)
        polys = VGroup(*[RegularPolygon(5, radius=1, fill_opacity=0.5,
                                        color=colors[j]
                                        ) for j in range(5)]
                       ).arrange(RIGHT)
        self.play(DrawBorderThenFill(polys))
        self.play(
            Rotate(polys[0], PI, rate_func=lambda t: t),
            Rotate(polys[1], PI, rate_func=smooth),
            Rotate(polys[2], PI, rate_func=np.sin),
            Rotate(polys[3], PI, rate_func=there_and_back),
            Rotate(polys[4], PI, rate_func=lambda t: 1 - abs(1 - 2 * t)),
            run_time=2
        )


class LaggingGroup(Scene):
    def construct(self):
        colors = color_gradient([BLUE, RED], 20)
        squares = (VGroup(*[Square(color=colors[j], fill_opacity=0.5) for j in range(20)])
                   .arrange_in_grid(4, 5)
                   .scale(0.5))

        self.play(AnimationGroup(*[FadeIn(s) for s in squares], lag_ratio=0.2))
        self.wait(1)
        self.play(AnimationGroup(*[FadeOut(s) for s in squares], lag_ratio=0.2))


class AnimateSyntax(Scene):
    def construct(self):
        s = Square(color=RED, fill_opacity=0.5)
        c = Circle(color=BLUE, fill_opacity=0.5)

        self.add(s, c)
        self.play(s.animate.shift(UP), c.animate.shift(DOWN))
        self.play(VGroup(s, c).animate.arrange(RIGHT))
        self.play(c.animate(rate_functions=linear).shift(RIGHT).scale(2))


class AnimateDiff(Scene):
    def construct(self):
        l_s = Square()
        r_s = Square()
        VGroup(l_s, r_s).arrange(RIGHT, buff=1)
        self.add(l_s, r_s)
        self.play(l_s.animate.rotate(PI), Rotate(r_s, PI), run_time=2)
        self.wait(1)


class AnimateTarget(Scene):
    def construct(self):
        c = Circle()

        c.generate_target()
        c.target.set_fill(color=GREEN, opacity=0.5)
        c.target.shift(2 * RIGHT, UR).scale(0.5)

        self.add(c)
        self.wait(1)
        self.play(MoveToTarget(c))

        s = Square()
        s.save_state()

        self.play(FadeIn(s))
        self.play(s.animate.set_color(BLUE).shift(2 * LEFT).scale(3))
        self.play(s.animate.shift(5 * DOWN).rotate(PI / 4))
        self.wait()
        self.play(Restore(s), run_time=2)
        self.wait(1)


class CustomAnimate(Scene):
    def construct(self):
        def spiral_out(mobject: Mobject, t):
            radius = 4 * t
            angle = 2 * t * 2 * PI

            mobject.move_to(radius * (np.cos(angle) * RIGHT + np.sin(angle) * UP))
            # mobject.set_color(ManimColor(int(t)))
            mobject.set_opacity(1 - t)

        d = Dot(color=WHITE)
        self.add(d)
        self.play(UpdateFromAlphaFunc(d, spiral_out, run_time=3))
