from manim import *
import numpy as np


class ManimCELogo(Scene):
    def construct(self):
        self.camera.background_color = '#ece6e2'
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        logo_black = "#343434"

        ds_m = MathTex(r'\mathbb{M}', fill_color=logo_black).scale(7)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)

        circle = Circle(color=logo_green, fill_opacity=1).shift(LEFT)
        square = Square(color=logo_blue, fill_opacity=1).shift(UP)
        triangle = Triangle(color=logo_red, fill_opacity=1).shift(RIGHT)

        logo = VGroup(triangle, square, circle, ds_m)
        logo.move_to(ORIGIN)

        self.add(logo)


class BraceAnnotation(Scene):
    def construct(self):
        dot1 = Dot(np.array([0, 0, 0]))
        dot2 = Dot(np.array([4, 2, 0]))
        dot2_tex = MathTex(r'(4, 2)', color=BLUE).next_to(dot2, RIGHT)

        ax = Axes()
        line = Line(dot1.get_center(), dot2.get_center()).set_color(ORANGE)
        b1 = Brace(line).set_color(TEAL)
        b1_text = b1.get_text('Horizontal distance').set_color(YELLOW)

        b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector()).set_color(TEAL)
        b2_text = b2.get_tex(r'x-x_1')

        self.add(ax, line, dot1, dot2, dot2_tex, b1, b1_text, b2, b2_text)


class VectorArrow(Scene):
    def construct(self):
        dot1 = Dot(ORIGIN)
        dot2 = Dot(np.array([2, 2, 0]))
        arrow = Arrow(dot1, dot2, buff=0)

        number_plane = NumberPlane()

        text1 = Text('(0, 0)').next_to(dot1, DOWN)
        text2 = Text('(2, 2)').next_to(dot2, RIGHT)

        self.add(number_plane, dot1, arrow, text1, text2)


class GradientImageFromArray(Scene):
    def construct(self):
        n = 256
        image_array = np.uint8([[i * 256 / n for i in range(0, n)] for _ in range(0, n)])
        print(image_array.shape)

        image = ImageMobject(image_array).scale(2)
        image.background_rectangle = SurroundingRectangle(image, GREEN)

        self.add(image, image.background_rectangle)
