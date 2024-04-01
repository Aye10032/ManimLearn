from typing import Tuple

import numpy as np
from manim import *
from manim import VGroup, Arrow


class Word2Vec(Scene):
    def construct(self):
        sentence_origin = Text("Tim like kitchen")
        self.play(Write(sentence_origin))

        sentence = Text("Tim like kitchen", font_size=30).move_to(3 * UP + RIGHT * 2)
        self.play(Transform(sentence_origin, sentence))

        word1 = Text("Tim ", font_size=30)
        word2 = Text("like ", font_size=30).next_to(word1, RIGHT)
        word3 = Text("kitchen", font_size=30).next_to(word2, RIGHT)
        sentence_word = VGroup(word1, word2, word3).move_to(sentence)

        plane = ComplexPlane()
        # self.add(plane)

        embedding_block = RoundedRectangle(
            corner_radius=0.2, width=4, height=1.5, color=GREEN).move_to(RIGHT * 2 + UP * 0.2)
        embedding_block_text = Tex(r"Input\\ Embedding", font_size=35).move_to(embedding_block)

        self.play(
            FadeIn(embedding_block_text, run_time=1),
            Create(embedding_block, run_time=1)
        )

        sentence = Text("Tim like kitchen", font_size=30, t2c={'Tim': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        a1, arrow_1 = self.draw_vector(word1, 1, "Tim", r"x^1")

        sentence = Text("Tim like kitchen", font_size=30, t2c={'like': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        a2, arrow_2 = self.draw_vector(word2, 2, "like", r"x^2")

        sentence = Text("Tim like kitchen", font_size=30, t2c={'kitchen': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        a3, arrow_3 = self.draw_vector(word3, 3, "kitchen", r"x^3")

        a1_t = a1.copy().scale(0.8).move_to(LEFT * 6.5 + UP * 2.8)
        a2_t = a2.copy().scale(0.8).move_to(LEFT * 6.5)
        a3_t = a3.copy().scale(0.8).move_to(LEFT * 6.5 + DOWN * 2.8)
        sentence = Text("Tim like kitchen", font_size=30).move_to(sentence)
        self.play(
            Transform(sentence_origin, sentence),
            Transform(a1, a1_t),
            Transform(a2, a2_t),
            Transform(a3, a3_t),
        )

        self.play(FadeOut(embedding_block, embedding_block_text, arrow_1, arrow_2, arrow_3))
        self.wait()

        question = Text("How to represent position information?", color=YELLOW)
        self.play(Write(question))
        self.wait(2)
        self.play(Unwrite(question))
        self.wait()

        position_tex = MathTex(r"""
        &\vec{p}_t^{(i)}=f(t)^{(i)}:=
        \begin{cases}{}\sin \left(\omega_k \cdot t\right) & if\ i=2k\\ 
        \cos \left(\omega_k \cdot t\right), & if\ i=2k+1
        \end{cases}
        \\
        \\
        &\text{where}\ \omega_k=\frac{1}{10000^{2k/d}}
        """, font_size=30)
        self.play(Write(position_tex))
        self.wait(2)

        position_encoding_block = embedding_block.copy()
        position_encoding_block_text = Tex(r"Position\\ Encoding", font_size=35).move_to(position_encoding_block)

        self.play(Transform(position_tex, position_encoding_block))
        self.play(FadeIn(position_encoding_block_text))
        self.wait(0.5)

        sentence = Text("Tim like kitchen", font_size=30, t2c={'Tim': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        d1, arrow_d1, arrows_d1 = self.draw_position(word1, [word2, word3], r"d^1")
        d1_rect_t = Rectangle(
            width=0.5, height=2, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=PURPLE
        )
        d1_tex_t = MathTex(r"d^1", color=PURPLE).next_to(d1_rect_t, DOWN)
        d1_t = VGroup(
            d1_rect_t,
            d1_tex_t
        ).scale(0.8).next_to(a1, RIGHT, buff=2)
        self.wait()
        self.play(
            Transform(d1, d1_t),
            FadeOut(arrow_d1, arrows_d1)
        )

        sentence = Text("Tim like kitchen", font_size=30, t2c={'like': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        d2, arrow_d2, arrows_d2 = self.draw_position(word2, [word1, word3], r"d^2")
        d2_rect_t = Rectangle(
            width=0.5, height=2, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=PURPLE
        )
        d2_tex_t = MathTex(r"d^2", color=PURPLE).next_to(d2_rect_t, DOWN)
        d2_t = VGroup(
            d2_rect_t,
            d2_tex_t
        ).scale(0.8).next_to(a2, RIGHT, buff=2)
        self.wait()
        self.play(
            Transform(d2, d2_t),
            FadeOut(arrow_d2, arrows_d2)
        )

        sentence = Text("Tim like kitchen", font_size=30, t2c={'kitchen': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        d3, arrow_d3, arrows_d3 = self.draw_position(word3, [word1, word2], r"d^3")
        d3_rect_t = Rectangle(
            width=0.5, height=2, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=PURPLE
        )
        d3_tex_t = MathTex(r"d^3", color=PURPLE).next_to(d3_rect_t, DOWN)
        d3_t = VGroup(
            d3_rect_t,
            d3_tex_t
        ).scale(0.8).next_to(a3, RIGHT, buff=2)
        self.wait()
        self.play(
            Transform(d3, d3_t),
            FadeOut(arrow_d3, arrows_d3)
        )

        self.wait()
        self.play(FadeOut(sentence_origin, position_tex, position_encoding_block_text))
        self.wait(0.5)

        tex1_plus = MathTex("+").next_to(a1, RIGHT, buff=0.8)
        tex2_plus = MathTex("+").next_to(a2, RIGHT, buff=0.8)
        tex3_plus = MathTex("+").next_to(a3, RIGHT, buff=0.8)
        tex1_eq = MathTex("=").next_to(a1, RIGHT, buff=3.2)
        tex2_eq = MathTex("=").next_to(a2, RIGHT, buff=3.2)
        tex3_eq = MathTex("=").next_to(a3, RIGHT, buff=3.2)

        self.play(
            Write(tex1_plus),
            Write(tex2_plus),
            Write(tex3_plus),
        )
        self.play(
            Write(tex1_eq),
            Write(tex2_eq),
            Write(tex3_eq),
        )
        self.wait()

        q1_rect = Rectangle(
            width=0.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=BLUE
        )
        q1_tex = MathTex(r"q^1", color=BLUE).next_to(q1_rect, DOWN)
        q1 = VGroup(q1_rect, q1_tex).scale(0.8).move_to(LEFT + UP * 2.8)

        q2_rect = Rectangle(
            width=0.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=BLUE
        )
        q2_tex = MathTex(r"q^2", color=BLUE).next_to(q2_rect, DOWN)
        q2 = VGroup(q2_rect, q2_tex).scale(0.8).move_to(LEFT)

        q3_rect = Rectangle(
            width=0.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=BLUE
        )
        q3_tex = MathTex(r"q^3", color=BLUE).next_to(q3_rect, DOWN)
        q3 = VGroup(q3_rect, q3_tex).scale(0.8).move_to(LEFT + DOWN * 2.8)

        self.play(
            Write(q1),
            Write(q2),
            Write(q3),
        )
        self.wait()

        self.play(Write(
            MathTex(
                r"&\text{...and here,}\\ &\text{we get the input vector }q^i",
                tex_to_color_map={r"q^i": BLUE}
            ).move_to(RIGHT * 3)
        ))

    def draw_vector(self, word_x: Mobject, seed: int, word_text: str, tex_text: str) -> Tuple[Mobject, Mobject]:
        start_pos = word_x.get_center()
        arrow_in = Arrow(start_pos, start_pos + 2.2 * DOWN, buff=0.3)
        self.play(GrowArrow(arrow_in))

        rect = Rectangle(width=1.0, height=4.0, grid_xstep=1.0, grid_ystep=1.0, color=RED).move_to(LEFT * 1.5)
        np.random.seed(seed)
        values = np.random.random((4,))
        value_group = VGroup(
            Tex(round(float(values[0]), 2)).move_to(LEFT * 1.5 + UP * 1.5),
            Tex(round(float(values[1]), 2)).move_to(LEFT * 1.5 + UP * 0.5),
            Tex(round(float(values[2]), 2)).move_to(LEFT * 1.5 + DOWN * 0.5),
            Tex(round(float(values[3]), 2)).move_to(LEFT * 1.5 + DOWN * 1.5),
        )

        equal = Tex("=").next_to(value_group, LEFT)

        word = Text(word_text, color=BLUE).next_to(equal, LEFT)
        word_origin = word_x.copy()

        self.play(Transform(word_origin, word))
        self.play(Write(equal))
        self.play(Create(rect), FadeIn(value_group))
        self.wait(0.4)

        ax_rect = Rectangle(
            width=0.5, height=2, grid_xstep=0.5, grid_ystep=0.5, color=RED, stroke_width=6
        ).move_to(word_x.get_center() + DOWN * 5)

        self.play(
            FadeOut(value_group, run_time=1),
            Transform(rect, ax_rect),
            FadeOut(word_origin, equal)
        )

        ax_tex = MathTex(tex_text, color=RED).next_to(ax_rect, DOWN)
        self.play(Write(ax_tex))

        output_group = VGroup(rect, ax_tex)
        return output_group, arrow_in

    def draw_position(self, word: Mobject, others: list[Mobject], tex_text: str) -> tuple[Mobject, Mobject, Mobject]:
        arrow_group = VGroup()
        start_pos = word.get_center()
        arrow_in = Arrow(start_pos, start_pos + 2.2 * DOWN, buff=0.3)
        # arrow_group.add(arrow_in)

        for mobj in others:
            _start_pos = mobj.get_center()
            _arrow_in = DashedVMobject(Arrow(_start_pos, _start_pos + 2.2 * DOWN, buff=0.3))
            arrow_group.add(_arrow_in)

        self.play(
            GrowArrow(arrow_in),
            Create(arrow_group)
        )

        d_rec = Rectangle(
            width=2, height=0.5, grid_xstep=0.5, grid_ystep=1, stroke_width=6, color=PURPLE
        ).move_to(RIGHT * 2 + DOWN * 1.5)

        d_tex = MathTex(tex_text, color=PURPLE).next_to(d_rec, DOWN)

        self.play(
            FadeIn(d_rec),
            Write(d_tex)
        )

        arrow_group.add(arrow_in)
        return VGroup(d_rec, d_tex), arrow_group, arrow_in
