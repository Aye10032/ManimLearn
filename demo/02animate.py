from manim import *
import numpy as np


class BooleanOperations(Scene):
    def construct(self):
        ellipse1 = Ellipse(width=4.0, height=5.0, fill_opacity=0.5, color=BLUE, stroke_width=10).move_to(LEFT)
        ellipse2 = ellipse1.copy().set_color(color=RED).move_to(RIGHT)
        title_text = MarkupText("Boolean Operation").next_to(ellipse1, UP * 3)
        ellipse_group = Group(title_text, ellipse1, ellipse2).move_to(LEFT * 3)
        self.play(FadeIn(ellipse_group))

        i = Intersection(ellipse1, ellipse2, color=GREEN, fill_opacity=0.5)
        self.play(i.animate.scale(0.25).move_to(RIGHT * 5 + UP * 2.5))
        intersection_text = Text('Intersection', font_size=23).next_to(i, UP)
        self.play(FadeIn(intersection_text))

        u = Union(ellipse1, ellipse2, color=ORANGE, fill_opacity=0.5)
        union_text = Text('Union', font_size=23)
        self.play(u.animate.scale(0.3).next_to(i, DOWN, buff=union_text.height * 3))
        union_text.next_to(u, UP)
        self.play(FadeIn(union_text))

        e = Exclusion(ellipse1, ellipse2, color=YELLOW, fill_opacity=0.5)
        exclusion_text = Text('Exclusion', font_size=23)
        self.play(e.animate.scale(0.25).next_to(u, DOWN, buff=exclusion_text.height * 3))
        exclusion_text.next_to(e, UP)
        self.play(FadeIn(exclusion_text))

        d = Difference(ellipse1, ellipse2, color=PINK, fill_opacity=0.5)
        different_text = Text('Different', font_size=23)
        self.play(d.animate.scale(0.25).next_to(u, LEFT, buff=0.8))
        different_text.next_to(d, UP)
        self.play(FadeIn(different_text))


class PointMovingOnShapes(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot1 = Dot()
        dot2 = dot1.copy().shift(RIGHT)
        self.add(dot1)

        self.play(GrowFromCenter(circle))
        self.play(Transform(dot1, dot2))
        self.play(MoveAlongPath(dot1, circle), run_time=2, rate_func=smooth)

        self.play(Rotating(dot1, about_point=[2, 0, 0]), run_time=1.5)
        self.wait()


class MovingAround(Scene):
    def construct(self):
        square = Square(color=BLUE, fill_opacity=1)

        self.play(square.animate.shift(LEFT * 3))
        self.play(square.animate.set_fill(ORANGE))
        self.play(square.animate.scale(0.4))
        self.play(square.animate.rotate(PI / 4))


class MovingAngle(Scene):
    def construct(self):
        rotation_center = LEFT

        theta_tracker = ValueTracker(110)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_ref = line_moving.copy()

        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )

        a = Angle(line1, line_moving, radius=0.5, other_angle=False)

        tex = MathTex(r'\theta').move_to(
            Angle(line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        )

        self.add(line1, line_moving, a, tex)
        self.wait()

        line_moving.add_updater(lambda x: x.become(line_ref.copy()).rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        ))

        a.add_updater(lambda x: x.become(Angle(line1, line_moving, radius=0.5, other_angle=False)))

        tex.add_updater(lambda x: x.move_to(
            Angle(line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        ))

        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))


class MovingDots(Scene):
    def construct(self):
        d1, d2 = Dot(color=BLUE), Dot(color=GREEN)
        dg = VGroup(d1, d2).arrange(RIGHT, buff=1)
        l1 = Line(d1.get_center(), d2.get_center()).set_color(RED)

        self.add(dg, l1)

        x = ValueTracker(0)
        y = ValueTracker(0)

        d1.add_updater(lambda z: z.set_x(x.get_value()))
        d2.add_updater(lambda z: z.set_y(y.get_value()))
        l1.add_updater(lambda z: z.become(
            Line(d1.get_center(), d2.get_center())
        ))

        self.play(x.animate.set_value(5))
        self.play(y.animate.set_value(4))
        self.play(x.animate.set_value(-3))
        self.play(y.animate.set_value(0))
        self.wait()
