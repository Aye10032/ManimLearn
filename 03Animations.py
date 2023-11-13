from manim import *


class AnimationExample(Scene):
    def construct(self):
        ax = Axes(x_range=(-3, 3), y_range=(-3, 3))
        curve = ax.plot(lambda x: (x + 2) * x * (x - 2) / 2, color=RED)

        area = ax.get_area(curve, x_range=(-2, 0), color=BLUE)
        self.play(Create(ax, run_time=2))
        self.play(Create(curve, run_time=3))
        # self.play(Create(ax, run_time=2), Create(curve, run_time=4))  # 同时播放
        self.play(FadeIn(area))
        self.wait(2)


# manim.exe -qm -p .\03Animations.py Square2Circle
class Square2Circle(Scene):
    def construct(self):
        green_square = Square(color=GREEN, fill_opacity=0.7)
        self.play(DrawBorderThenFill(green_square, run_time=2))

        blue_circle = Circle(color=BLUE, fill_opacity=0.7)
        self.play(ReplacementTransform(green_square, blue_circle))
        self.wait(1)
        self.play(Indicate(blue_circle))
        self.wait(1)
        self.play(FadeOut(blue_circle))
        self.wait(1)
