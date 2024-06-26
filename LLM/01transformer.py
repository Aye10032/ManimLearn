import math
from typing import Tuple

import numpy as np
from manim import *
from manim import VGroup, Arrow
from manim.typing import Vector3


class Word2Vec(Scene):
    def construct(self):
        # self.add(ComplexPlane())

        title = Title("Step1. Word to vector", color=YELLOW)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(Unwrite(title))

        commentary1 = Text("Here is a sentence.", color=YELLOW, font_size=35).to_edge(UL, buff=0.5)
        self.play(Create(commentary1))
        self.wait(0.5)

        sentence_origin = Text("Tim like kitchen")
        self.play(Write(sentence_origin))

        commentary2 = Tex(
            r"...first,\\ we use word embeddings to transform them into a set of vectors",
            color=YELLOW, font_size=35).to_edge(DL, buff=0.5)
        self.play(Create(commentary2))
        self.wait(2)
        self.play(FadeOut(commentary1, commentary2))

        sentence = Text("Tim like kitchen", font_size=30).move_to(3 * UP + RIGHT * 2)
        self.play(Transform(sentence_origin, sentence))

        word1 = Text("Tim ", font_size=30, color=BLUE)
        word2 = Text("like ", font_size=30, color=BLUE).next_to(word1, RIGHT)
        word3 = Text("kitchen", font_size=30, color=BLUE).next_to(word2, RIGHT)
        sentence_word = VGroup(word1, word2, word3).move_to(sentence)

        embedding_block = RoundedRectangle(
            corner_radius=0.2, width=4, height=1.5, color=GREEN).move_to(RIGHT * 2 + UP * 0.2)
        embedding_block_text = Tex(r"Input\\ Embedding", font_size=35).move_to(embedding_block)

        self.play(
            FadeIn(embedding_block_text, run_time=1),
            Create(embedding_block, run_time=1)
        )

        sentence = Text("Tim like kitchen", font_size=30, t2c={'Tim': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        a1, arrow_1 = self.draw_vector(word1, 1, "Tim", r"x^{'1}")

        sentence = Text("Tim like kitchen", font_size=30, t2c={'like': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        a2, arrow_2 = self.draw_vector(word2, 2, "like", r"x^{'2}")

        sentence = Text("Tim like kitchen", font_size=30, t2c={'kitchen': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        a3, arrow_3 = self.draw_vector(word3, 3, "kitchen", r"x^{'3}")

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

        question = Tex(
            r"...now we are facing with a new problem:\\ How to represent position information?",
            color=YELLOW,
            font_size=38
        )
        self.play(Write(question))
        self.wait(2)
        self.play(FadeOut(question))
        self.wait()

        commentary1 = Text("We use this formula to calculate the position encoding", color=YELLOW, font_size=35)

        position_tex = MathTex(r"""
        &\vec{p}_t^{(i)}=f(t)^{(i)}:=
        \begin{cases}{}\sin \left(\omega_k \cdot t\right) & if\ i=2k\\ 
        \cos \left(\omega_k \cdot t\right), & if\ i=2k+1
        \end{cases}
        \\
        \\
        &\text{where}\ \omega_k=\frac{1}{10000^{2k/d}}
        """, font_size=30).next_to(commentary1, DOWN)

        VGroup(commentary1, position_tex).move_to(ORIGIN)
        self.play(Create(commentary1))
        self.play(Write(position_tex))
        self.wait(2)

        position_encoding_block = embedding_block.copy()
        position_encoding_block_text = Tex(r"Position\\ Encoding", font_size=35).move_to(position_encoding_block)

        self.play(FadeOut(commentary1))
        self.play(Transform(position_tex, position_encoding_block))
        self.play(FadeIn(position_encoding_block_text))
        self.wait(0.5)

        sentence = Text("Tim like kitchen", font_size=30, t2c={'Tim': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        d1, arrow_d1, arrows_d1 = self.draw_position(word1, [word2, word3], r"d^1")
        d1_rect_t = Rectangle(
            width=0.5, height=2, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=TEAL_C
        )
        d1_tex_t = MathTex(r"d^1", color=TEAL_C).next_to(d1_rect_t, DOWN)
        d1_t = VGroup(
            d1_rect_t,
            d1_tex_t
        ).scale(0.8).next_to(a1, RIGHT, buff=2)
        self.wait()
        self.play(
            TransformMatchingShapes(d1, d1_t),
            FadeOut(arrow_d1, arrows_d1)
        )

        sentence = Text("Tim like kitchen", font_size=30, t2c={'like': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        d2, arrow_d2, arrows_d2 = self.draw_position(word2, [word1, word3], r"d^2")
        d2_rect_t = Rectangle(
            width=0.5, height=2, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=TEAL_C
        )
        d2_tex_t = MathTex(r"d^2", color=TEAL_C).next_to(d2_rect_t, DOWN)
        d2_t = VGroup(
            d2_rect_t,
            d2_tex_t
        ).scale(0.8).next_to(a2, RIGHT, buff=2)
        self.wait()
        self.play(
            TransformMatchingShapes(d2, d2_t),
            FadeOut(arrow_d2, arrows_d2)
        )

        sentence = Text("Tim like kitchen", font_size=30, t2c={'kitchen': BLUE}).move_to(sentence)
        self.play(Transform(sentence_origin, sentence))
        d3, arrow_d3, arrows_d3 = self.draw_position(word3, [word1, word2], r"d^3")
        d3_rect_t = Rectangle(
            width=0.5, height=2, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=TEAL_C
        )
        d3_tex_t = MathTex(r"d^3", color=TEAL_C).next_to(d3_rect_t, DOWN)
        d3_t = VGroup(
            d3_rect_t,
            d3_tex_t
        ).scale(0.8).next_to(a3, RIGHT, buff=2)
        self.wait()
        self.play(
            TransformMatchingShapes(d3, d3_t),
            FadeOut(arrow_d3, arrows_d3)
        )

        self.wait()
        self.play(FadeOut(sentence_origin, position_tex, position_encoding_block_text))
        self.wait(0.5)

        commentary1 = Text("then we just need to add them together", color=YELLOW, font_size=32).move_to(RIGHT)
        self.play(Write(commentary1))
        self.wait()
        self.play(FadeOut(commentary1))

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

        q1_rect = Rectangle(
            width=0.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=PURPLE_A
        )
        q1_tex = MathTex(r"x^1", color=PURPLE_A).next_to(q1_rect, DOWN)
        q1 = VGroup(q1_rect, q1_tex).scale(0.8).move_to(LEFT + UP * 2.8)

        q2_rect = Rectangle(
            width=0.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=PURPLE_A
        )
        q2_tex = MathTex(r"x^2", color=PURPLE_A).next_to(q2_rect, DOWN)
        q2 = VGroup(q2_rect, q2_tex).scale(0.8).move_to(LEFT)

        q3_rect = Rectangle(
            width=0.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=PURPLE_A
        )
        q3_tex = MathTex(r"x^3", color=PURPLE_A).next_to(q3_rect, DOWN)
        q3 = VGroup(q3_rect, q3_tex).scale(0.8).move_to(LEFT + DOWN * 2.8)

        self.play(
            Write(q1),
            Write(q2),
            Write(q3),
        )
        self.wait()

        commentary1 = MathTex(
            r"&\text{...and here,}\\ &\text{we get the input vector }x^i",
            tex_to_color_map={r"x^i": PURPLE_A}
        ).move_to(RIGHT * 3)
        self.play(Write(commentary1))
        self.play(
            FadeOut(a1, a2, a3),
            FadeOut(tex1_plus, tex2_plus, tex3_plus),
            # FadeOut(d1, d2, d3),
            FadeOut(d1_t, d2_t, d3_t),
            FadeOut(tex1_eq, tex2_eq, tex3_eq),
        )

        self.wait(2)

        self.play(
            FadeOut(q1, q2, q3),
            FadeOut(commentary1)
        )
        self.wait(2)

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
        self.play(Create(rect))
        self.play(FadeIn(value_group))
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
            width=2, height=0.5, grid_xstep=0.5, grid_ystep=1, stroke_width=6, color=TEAL_C
        ).move_to(RIGHT * 2 + DOWN * 1.5)

        d_tex = MathTex(tex_text, color=TEAL_C).next_to(d_rec, DOWN)

        self.play(
            FadeIn(d_rec),
            Write(d_tex)
        )

        arrow_group.add(arrow_in)
        return VGroup(d_rec, d_tex), arrow_group, arrow_in


class AttentionLayer(Scene):
    def __init__(self, **kwargs):
        Scene.__init__(self, **kwargs)

        x1_rect = Rectangle(width=0.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=PURPLE_A)
        x1_tex = MathTex(r"x^1", color=PURPLE_A).next_to(x1_rect, DOWN)
        self.x1 = VGroup(x1_rect, x1_tex)

        x2_rect = x1_rect.copy()
        x2_tex = MathTex(r"x^2", color=PURPLE_A).next_to(x2_rect, DOWN)
        self.x2 = VGroup(x2_rect, x2_tex)

        x3_rect = x1_rect.copy()
        x3_tex = MathTex(r"x^3", color=PURPLE_A).next_to(x3_rect, DOWN)
        self.x3 = VGroup(x3_rect, x3_tex)

        self.w_matrix = Rectangle(width=1.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5).move_to(LEFT * 1.5)
        self.result_vector = Rectangle(
            width=1.5, height=0.5, grid_xstep=0.5, grid_ystep=0.5).next_to(self.w_matrix, RIGHT)

    def construct(self):
        # self.add(ComplexPlane())

        title = Title("Step2. Scaled Dot-Product Attention", color=YELLOW)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(Unwrite(title))

        commentary1 = Text("We've got the initial input vector.", color=YELLOW, font_size=35).to_edge(UP, buff=0.5)
        commentary2 = Text(
            "and the next job is to compute the attention score", color=YELLOW, font_size=35).next_to(commentary1, DOWN)
        self.play(Create(commentary1))
        self.wait()

        self.x1.scale(0.8).move_to(LEFT * 6.5 + UP * 2.8)
        self.x2.scale(0.8).move_to(LEFT * 6.5)
        self.x3.scale(0.8).move_to(LEFT * 6.5 + DOWN * 2.8)
        self.play(FadeIn(self.x1, self.x2, self.x3))
        self.wait()

        self.play(Create(commentary2))
        self.wait(0.5)
        self.play(FadeOut(commentary1, commentary2))
        self.wait(0.5)

        commentary1 = MathTex(
            r"""&\text{We use three different weight matrices }\mathbf{W}^q,\mathbf{W}^k,\mathbf{W}^v\\
            &\text{calculated separately to get vector }q^i,k^i,v^i""",
            color=YELLOW,
            font_size=35,
            tex_to_color_map={
                r'\mathbf{W}^q': BLUE,
                r'\mathbf{W}^k': GOLD,
                r'\mathbf{W}^v': GREEN,
                r'q^i': BLUE,
                r'k^i': GOLD,
                r'v^i': GREEN,
            }
        ).to_edge(UP, buff=0.5).shift(LEFT * 0.5)
        self.play(Create(commentary1))

        self.w_matrix.set_color(BLUE)
        w_tex_1 = MathTex(r"\mathbf{W}^q", color=BLUE).next_to(self.w_matrix, DOWN, buff=0.2)

        self.play(
            FadeIn(self.w_matrix),
            Write(w_tex_1)
        )
        self.wait()
        q1 = self.get_qkv(self.x1[0], BLUE, RIGHT * 4.5 + UP * 2.8, r"q^1")
        q2 = self.get_qkv(self.x2[0], BLUE, RIGHT * 5.5 + UP * 2.8, r"q^2")
        q3 = self.get_qkv(self.x3[0], BLUE, RIGHT * 6.5 + UP * 2.8, r"q^3")

        w_tex_2 = MathTex(r"\mathbf{W}^k", color=GOLD).next_to(self.w_matrix, DOWN, buff=0.2)
        self.play(
            self.w_matrix.animate.set_color(GOLD),
            AnimationGroup(
                FadeOut(w_tex_1),
                Write(w_tex_2)
            )
        )
        k1 = self.get_qkv(self.x1[0], GOLD, RIGHT * 4.5, r"k^1")
        k2 = self.get_qkv(self.x2[0], GOLD, RIGHT * 5.5, r"k^2")
        k3 = self.get_qkv(self.x3[0], GOLD, RIGHT * 6.5, r"k^3")

        w_tex_1 = MathTex(r"\mathbf{W}^v", color=GREEN).next_to(self.w_matrix, DOWN, buff=0.2)
        self.play(
            FadeToColor(self.w_matrix, GREEN),
            AnimationGroup(
                FadeOut(w_tex_2),
                Write(w_tex_1)
            )
        )
        v1 = self.get_qkv(self.x1[0], GREEN, RIGHT * 4.5 + DOWN * 2.5, r"v^1")
        v2 = self.get_qkv(self.x2[0], GREEN, RIGHT * 5.5 + DOWN * 2.5, r"v^2")
        v3 = self.get_qkv(self.x3[0], GREEN, RIGHT * 6.5 + DOWN * 2.5, r"v^3")
        self.wait()

        self.play(FadeOut(self.x1, self.x2, self.x3, self.w_matrix, w_tex_1, commentary1))

        commentary1 = MathTex(
            r"""&\text{...then, we do a dot product between }q^i\text{ and }k^i\\
            &\text{to compute a scoring vector}""",
            color=YELLOW,
            font_size=35,
            tex_to_color_map={
                r'q^i': BLUE,
                r'k^i': GOLD,
            }
        ).to_edge(UR, buff=0.5)

        self.play(
            q1.animate.move_to(LEFT * 6 + DOWN * 2.5),
            q2.animate.move_to(LEFT * 4.5 + DOWN * 2.5),
            q3.animate.move_to(LEFT * 3 + DOWN * 2.5),
            k1.animate.move_to(LEFT * 6),
            k2.animate.move_to(LEFT * 4.5),
            k3.animate.move_to(LEFT * 3),
        )
        self.play(Create(commentary1))
        self.wait()

        alpha_1_ = self.dot_products(q1[0], [k1[0], k2[0], k3[0]], LEFT * 6 + UP * 2.8, r"\alpha^{'1}")
        alpha_2_ = self.dot_products(q2[0], [k1[0], k2[0], k3[0]], LEFT * 4.5 + UP * 2.8, r"\alpha^{'2}")
        alpha_3_ = self.dot_products(q3[0], [k1[0], k2[0], k3[0]], LEFT * 3 + UP * 2.8, r"\alpha^{'3}")
        self.wait()

        self.play(
            FadeOut(commentary1),
            q1.animate.move_to(RIGHT * 4.5 + UP * 2.8),
            q2.animate.move_to(RIGHT * 5.5 + UP * 2.8),
            q3.animate.move_to(RIGHT * 6.5 + UP * 2.8),
            k1.animate.move_to(LEFT * 6 + DOWN * 2.5),
            k2.animate.move_to(LEFT * 4.5 + DOWN * 2.5),
            k3.animate.move_to(LEFT * 3 + DOWN * 2.5),
        )

        commentary1 = MathTex(
            r"""&\text{for these scoring vectors, we need to do a scaling}""",
            color=YELLOW,
            font_size=35,
        ).to_edge(LEFT, buff=0.5)
        self.play(Create(commentary1))

        brace = BraceBetweenPoints([-2.8, -1.7, 0], [-2.8, -2.7, 0], direction=np.array([1, 0, 0]))
        self.play(Create(brace))

        dim_tex = MathTex(r"dim_k=", "3", font_size=30).next_to(brace, RIGHT)
        self.play(Write(dim_tex))
        self.wait()

        box = SurroundingRectangle(
            VGroup(alpha_1_, alpha_2_, alpha_3_), color=GREEN, buff=MED_LARGE_BUFF, corner_radius=0.2)
        w_tex_1 = MathTex(r"\div").next_to(box, RIGHT)
        dim = dim_tex[1].copy()
        w_tex_2 = MathTex(r"=")
        self.play(Create(box))
        self.play(
            Write(w_tex_1),
            Transform(
                dim, MathTex(r"\sqrt{3}").next_to(w_tex_1, RIGHT))
        )
        self.play(Write(w_tex_2.next_to(dim)))
        self.play(FadeOut(commentary1))

        alpha_1__ = self.scale(alpha_1_[0], RIGHT * 1. + UP * 2.8, r"\alpha^{''1}")
        alpha_2__ = self.scale(alpha_2_[0], RIGHT * 2. + UP * 2.8, r"\alpha^{''2}")
        alpha_3__ = self.scale(alpha_3_[0], RIGHT * 3. + UP * 2.8, r"\alpha^{''3}")
        self.wait(0.5)

        self.play(
            FadeOut(
                alpha_1_, alpha_2_, alpha_3_, brace, dim_tex, dim, w_tex_1, w_tex_2),
            Uncreate(box)
        )

        self.play(
            alpha_1__.animate.move_to(LEFT + UP * 2.8),
            alpha_2__.animate.move_to(ORIGIN + UP * 2.8),
            alpha_3__.animate.move_to(RIGHT + UP * 2.8),
            k1.animate.move_to(RIGHT * 4.5),
            k2.animate.move_to(RIGHT * 5.5),
            k3.animate.move_to(RIGHT * 6.5),
        )
        self.wait(0.5)

        softmax_block = RoundedRectangle(width=3.5, height=1.2, corner_radius=0.2, color=GREEN)
        softmax_block_text = Text("Softmax", font_size=32).move_to(softmax_block)
        self.play(
            Create(softmax_block),
            Write(softmax_block_text)
        )

        arrows = self.draw_arrows([alpha_1__, alpha_2__, alpha_3__], softmax_block)
        alpha1_rect = alpha_1__[0].copy().set_color(TEAL_A).shift(DOWN * 5)
        alpha1_tex = MathTex(r"\alpha^1", color=TEAL_A).scale(0.64).next_to(alpha1_rect, DOWN)
        alpha1 = VGroup(alpha1_rect, alpha1_tex)
        alpha2_rect = alpha_2__[0].copy().set_color(TEAL_A).shift(DOWN * 5)
        alpha2_tex = MathTex(r"\alpha^2", color=TEAL_A).scale(0.64).next_to(alpha2_rect, DOWN)
        alpha2 = VGroup(alpha2_rect, alpha2_tex)
        alpha3_rect = alpha_3__[0].copy().set_color(TEAL_A).shift(DOWN * 5)
        alpha3_tex = MathTex(r"\alpha^1", color=TEAL_A).scale(0.64).next_to(alpha3_rect, DOWN)
        alpha3 = VGroup(alpha3_rect, alpha3_tex)
        self.play(
            FadeIn(alpha1_rect, alpha2_rect, alpha3_rect),
            Write(alpha1_tex),
            Write(alpha2_tex),
            Write(alpha3_tex),
        )
        self.wait()

        self.play(
            FadeOut(arrows, alpha_1__, alpha_2__, alpha_3__, softmax_block, softmax_block_text),
            alpha1.animate.move_to(LEFT),
            alpha2.animate.move_to(ORIGIN),
            alpha3.animate.move_to(RIGHT),
        )

        box = SurroundingRectangle(
            VGroup(alpha1, alpha2, alpha3), color=GREEN, buff=MED_LARGE_BUFF, corner_radius=0.2)

        commentary1 = Text("Score").next_to(box, DOWN)
        self.play(
            Create(box),
            Write(commentary1)
        )
        self.wait()
        self.play(
            Uncreate(box),
            FadeOut(commentary1)
        )

        commentary1 = MathTex(
            r"\text{...then, we calculate dot product between }\alpha^i\text{ and }v^i",
            tex_to_color_map={
                r'\alpha^i': TEAL_A,
                r'v^i': GREEN
            },
            color=YELLOW,
            font_size=35,
        ).to_edge(UL, buff=0.5)
        self.play(Create(commentary1))
        self.wait()
        self.play(FadeOut(commentary1))

        self.play(
            alpha1.animate.move_to(LEFT * 6 + DOWN * 2.5),
            alpha2.animate.move_to(LEFT * 4.5 + DOWN * 2.5),
            alpha3.animate.move_to(LEFT * 3 + DOWN * 2.5),
            v1.animate.move_to(LEFT * 6),
            v2.animate.move_to(LEFT * 4.5),
            v3.animate.move_to(LEFT * 3),
        )
        self.wait()

        y_1 = self.dot_products(alpha1[0], [v1[0], v2[0], v3[0]], LEFT * 6 + UP * 2.8, r"y^{1}")
        y_2 = self.dot_products(alpha2[0], [v1[0], v2[0], v3[0]], LEFT * 4.5 + UP * 2.8, r"y^{2}")
        y_3 = self.dot_products(alpha3[0], [v1[0], v2[0], v3[0]], LEFT * 3 + UP * 2.8, r"y^{3}")
        self.wait()

        self.play(
            FadeOut(alpha1, alpha2, alpha3),
            v1.animate.move_to(RIGHT * 4.5 + DOWN * 2.5),
            v2.animate.move_to(RIGHT * 5.5 + DOWN * 2.5),
            v3.animate.move_to(RIGHT * 6.5 + DOWN * 2.5),
            y_1.animate.move_to(LEFT),
            y_2.animate.move_to(ORIGIN),
            y_3.animate.move_to(RIGHT)
        )
        self.wait()

        commentary1 = MathTex(
            r"\text{now this is the output we get from the attention layer}",
            color=YELLOW,
            font_size=35,
        ).to_edge(UL, buff=0.5)
        self.play(Create(commentary1))
        self.wait()
        self.play(
            FadeOut(commentary1),
            FadeOut(y_1, y_2, y_3)
        )

        q_matrix = self.contact_to_matrix([q1, q2, q3], BLUE, LEFT * 6 + UP * 2.8, r"Q")
        k_matrix = self.contact_to_matrix([k1, k2, k3], GOLD, LEFT * 6, r"K")
        v_matrix = self.contact_to_matrix([v1, v2, v3], GREEN, LEFT * 6 + DOWN * 2.5, r"V")

        commentary1 = MathTex(
            r"""&\text{After combining the vectors into a matrix}\\
            &\text{the operation just described can be expressed as follow: }
            """,
            color=YELLOW,
            font_size=35,
        ).to_edge(UP, buff=0.5)
        self.play(Create(commentary1))
        self.wait(0.5)

        commentary2 = MathTex(
            r"\text{Attention}(Q,K,V)=\text{softmax}\left({ QK^T \over \sqrt{dim_k} }\right)V",
            tex_to_color_map={
                r'Q': BLUE,
                r'K': GOLD,
                r'V': GREEN,
            }
        )
        self.play(Write(commentary2))
        self.wait(2)

        self.play(FadeOut(commentary1, q_matrix, k_matrix, v_matrix))
        self.play(FadeOut(commentary2))
        self.wait(3)

    def get_qkv(self, origin: Mobject, result_color: ManimColor, target_position, tex_text: str) -> Mobject:
        _rect = origin.copy()

        self.play(_rect.animate.next_to(self.w_matrix, LEFT, buff=1).rotate(90 * DEGREES))
        self.wait(0.5)
        self.result_vector.set_color(result_color)
        self.play(Transform(_rect, self.result_vector))
        self.wait(0.5)
        self.play(_rect.animate.move_to(target_position).rotate(90 * DEGREES).scale(0.8))

        _tex = MathTex(tex_text, color=result_color).scale(0.64).next_to(_rect, DOWN)
        self.play(Write(_tex))

        return VGroup(_rect, _tex)

    def dot_products(self, mobj1: Mobject, mobj2: List[Mobject], target_position, tex_text: str) -> Mobject:
        def get_arrow(origin: Mobject, target: Mobject):
            start_pos = origin.get_top()
            end_pos = target.get_bottom()

            arrow = Line(
                start_pos, end_pos, stroke_width=3, buff=SMALL_BUFF
            ).add_tip(tip_shape=ArrowTriangleFilledTip, tip_width=0.1, tip_length=0.15)

            return arrow

        _rect = mobj1.copy().set_color(WHITE).move_to(target_position)
        _tex = MathTex(tex_text).scale(0.64).next_to(_rect, DOWN)

        arrow1 = get_arrow(mobj1, mobj2[0])
        arrow2 = get_arrow(mobj1, mobj2[1])
        arrow3 = get_arrow(mobj1, mobj2[2])
        arrow4 = get_arrow(mobj2[0], _rect)
        arrow5 = get_arrow(mobj2[1], _rect)
        arrow6 = get_arrow(mobj2[2], _rect)

        self.play(
            Create(arrow1),
            Create(arrow2),
            Create(arrow3),
            Create(arrow4),
            Create(arrow5),
            Create(arrow6),
        )
        self.play(FadeIn(_rect))
        self.play(FadeOut(arrow1, arrow2, arrow3, arrow4, arrow5, arrow6, run_time=0.5))
        self.play(Write(_tex))

        return VGroup(_rect, _tex)

    def scale(self, mobj: Mobject, target_position, tex_text: str) -> Mobject:
        _rect = mobj.copy()
        self.play(Transform(
            _rect,
            mobj.copy().move_to(target_position)
        ))

        _tex = MathTex(tex_text).scale(0.64).next_to(_rect, DOWN)
        self.play(Write(_tex))

        return VGroup(_rect, _tex)

    def draw_arrows(self, origin_list: List[Mobject], target: Mobject) -> Mobject:
        def get_arrow(origin: Mobject):
            start_pos = origin.get_bottom()

            end_pos = target.get_top()
            end_pos[0] = start_pos[0]
            arrow = Arrow(
                start_pos, end_pos,
                stroke_width=3
            )

            return arrow

        arrow1 = get_arrow(origin_list[0])
        arrow2 = get_arrow(origin_list[1])
        arrow3 = get_arrow(origin_list[2])

        self.play(
            GrowArrow(arrow1),
            GrowArrow(arrow2),
            GrowArrow(arrow3),
        )

        return VGroup(arrow1, arrow2, arrow3)

    def contact_to_matrix(
            self, mobj_list: List[Mobject], result_color: ManimColor, target_position, tex_text: str
    ) -> Mobject:
        group = Group()
        tex_group = Group()
        for mobj in mobj_list:
            group.add(mobj[0])
            tex_group.add(mobj[1])

        _rect = Rectangle(
            width=1.5, height=1.5, grid_xstep=0.5, grid_ystep=0.5, color=result_color
        ).scale(0.8).move_to(target_position)

        self.play(
            TransformMatchingShapes(group, _rect),
            FadeOut(tex_group)
        )

        _tex = MathTex(tex_text, color=result_color).scale(0.64).next_to(_rect, DOWN)
        self.play(Write(_tex))

        return Group(_rect, _tex)


def sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s.round(2)


class DecoderOnly(ThreeDScene):
    def __init__(self, *args, **kwargs):
        ThreeDScene.__init__(self, *args, **kwargs)

        self.all: Group = Group()
        self.sentence: Tex = None
        self.embedding_block: VGroup = None
        self.embedding_vector: VGroup = None
        self.position_vector: VGroup = None
        self.x_matrix: Matrix = None

        self.wq: VGroup = None
        self.wk: VGroup = None
        self.wv: VGroup = None
        self.q_matrix: Matrix = None
        self.k_matrix: Matrix = None
        self.v_matrix: Matrix = None

        self.liner1: VGroup = None
        self.q_group: VGroup = None
        self.k_group: VGroup = None
        self.v_group: VGroup = None

        self.scale_block: VGroup = None
        self.sigmoid_block: VGroup = None
        self.liner2: Prism = None
        self.y_matrix: Matrix = None

    def construct(self):
        title = Title("Step3. Multi head masked attention", color=YELLOW)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(Unwrite(title))

        self.set_camera_orientation(phi=90 * DEGREES)

        commentary1 = Text(
            "Let's take a complete look at the attention calculation process",
            color=YELLOW,
            font_size=29
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_corner(UL)
        self.play(Write(commentary1))

        self.sentence = Tex("Attention ", "is ", "all ", "you ", "need")
        self.play(Write(self.sentence.rotate(PI / 2, axis=RIGHT)))
        self.all.add(self.sentence)

        phi, theta, focal_distance, gamma, zoom = self.camera.get_value_trackers()
        # print(f'phi: {phi.get_value() / DEGREES}, theta: {theta.get_value() / DEGREES}, gamma: {gamma.get_value()}')
        self.wait()
        self.play(
            phi.animate.set_value(75 * DEGREES),
            theta.animate.set_value(-150 * DEGREES),
            zoom.animate.set_value(0.8)
        )

        self.play(FadeOut(commentary1))

        commentary1 = MathTex(
            r"""&\text{First we compute the word embedding and positional encoding}\\
         &\text{of the text to get its vector representation}""",
            color=YELLOW,
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_corner(UL)
        self.play(Write(commentary1))
        self.wait()
        self.play(FadeOut(commentary1))

        self.embedding()
        self.wait()

        commentary1 = MathTex(
            r"""\text{Then, we compute the matrix }Q,K,V\\ 
            \text{by three weights }\boldsymbol{w}^q,\boldsymbol{w}^k,\boldsymbol{w}^v""",
            tex_to_color_map={
                r'\boldsymbol{w}^q': BLUE,
                r'\boldsymbol{w}^k': GOLD,
                r'\boldsymbol{w}^v': GREEN,
                r'Q': BLUE,
                r'K': GOLD,
                r'V': GREEN,
            },
            color=YELLOW,
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_edge(RIGHT)
        self.play(Write(commentary1))
        self.wait()
        self.play(FadeOut(commentary1))

        self.get_qkv()
        self.wait()

        commentary1 = MathTex(
            r"""\text{Here, we use }n\text{ different MLP to }\\
            \text{extract various features as inputs}\\
            \text{for multi-head attention.}""",
            color=YELLOW,
            tex_to_color_map={
                "multi-head attention": WHITE
            },
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_edge(RIGHT)
        self.play(Write(commentary1))
        self.wait()
        self.play(FadeOut(commentary1))

        self.multi_head()
        self.play(zoom.animate.set_value(0.6))
        self.wait()

        commentary1 = MathTex(
            r"""\text{For each set of }Q,K,V\\ 
            \text{the calculations we perform are}\\
            \text{the same as before.}""",
            tex_to_color_map={
                r'Q': BLUE,
                r'K': GOLD,
                r'V': GREEN,
            },
            color=YELLOW,
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_edge(RIGHT)
        self.play(Write(commentary1))
        self.wait(0.8)
        self.play(FadeOut(commentary1))
        commentary1 = MathTex(
            r"""\text{First, we calculate dot product}\\ 
            \text{between }Q \text{ and the transpose of }K""",
            tex_to_color_map={
                r'Q': BLUE,
                r'K': GOLD,
            },
            color=YELLOW,
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_edge(RIGHT)
        self.play(Write(commentary1))
        self.wait(0.8)
        self.play(FadeOut(commentary1))

        self.self_attention()
        self.wait()

        self.play(
            self.all.animate.shift(UP * 5),
            theta.animate.set_value(-115 * DEGREES),
            zoom.animate.set_value(0.6),
            run_time=2
        )

        commentary1 = MathTex(
            r"""\text{This is the process of multi-head attention calculation.}""",
            color=YELLOW,
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_corner(DL)
        self.play(Write(commentary1))
        self.wait()
        self.all.remove(self.y_matrix)

        self.play(
            FadeOut(self.all),
            theta.animate.set_value(-90 * DEGREES),
        )
        self.play(FadeOut(commentary1))
        self.wait(0.5)
        self.play(FadeOut(self.y_matrix))
        self.wait(2)

    def embedding(self):
        self.play(self.all.animate.shift(UP * 3))

        embedding_prism = Prism(
            dimensions=(4, 0.5, 2),
            fill_color=GRAY,
            fill_opacity=0.3,
            stroke_color=GREEN,
            stroke_width=1,
            stroke_opacity=1
        )
        embedding_tex = Text(
            "Embedding layer", font_size=30, color=GREEN
        ).next_to(embedding_prism, LEFT).shift(IN + DOWN).rotate(PI / 2, RIGHT).rotate(PI / 2, IN)
        self.embedding_block = VGroup(embedding_prism, embedding_tex)

        self.play(FadeIn(self.embedding_block.move_to(ORIGIN)))
        self.all.add(self.embedding_block)

        self.play(self.all.animate.shift(IN * 1.5))

        self.embedding_vector = VGroup()
        self.position_vector = VGroup()
        sum_vector = np.zeros((6, 5))
        for i in range(5):
            if i == 0:
                self.play(self.sentence[i].animate.set_color(BLUE_D))
            else:
                self.play(self.sentence[i - 1].animate.set_color(WHITE), self.sentence[i].animate.set_color(BLUE_D))

            np.random.seed(i)
            values = np.random.random((6, 1)).round(2)
            sum_vector[:, i] += values[:, 0]

            vector = Matrix(values, bracket_v_buff=SMALL_BUFF).scale(0.7).move_to(
                embedding_prism.get_center()).rotate(PI / 2, axis=RIGHT)

            np.random.seed(i + 10)
            position_values = np.random.random((6, 1)).round(2)
            sum_vector[:, i] += position_values[:, 0]
            position_vector = self.sentence.copy()

            self.play(self.sentence[i].copy().animate.move_to(embedding_prism.get_center()).fade(1))
            self.play(vector.animate.shift(3 * DOWN + LEFT * 3 + RIGHT * i * 1.5).fade(0))
            self.play(
                Transform(
                    position_vector,
                    Matrix(position_values, bracket_v_buff=SMALL_BUFF).scale(0.7).move_to(
                        embedding_prism.get_center() + LEFT * 3 + OUT * 4 + RIGHT * i * 1.5 + DOWN * 3
                    ).rotate(PI / 2, axis=RIGHT).fade(0),
                    run_time=1.5
                )
            )

            self.embedding_vector.add(vector)
            self.position_vector.add(position_vector)

            if i == 4:
                self.play(self.sentence[i].animate.set_color(WHITE))

        self.all.add(self.embedding_vector, self.position_vector)

        self.play(self.all.animate.shift(UP * 4))
        sum_vector = sum_vector.round(2)
        self.x_matrix = Matrix(sum_vector).set_color(PURPLE_A).move_to(ORIGIN).scale(0.7).rotate(PI / 2, axis=RIGHT)

        self.play(Succession(
            Transform(
                VGroup(self.embedding_vector.copy(), self.position_vector.copy()),
                self.x_matrix,
                replace_mobject_with_target_in_scene=True
            ),
            AnimationGroup(
                self.position_vector.animate.fade(),
                self.embedding_vector.animate.fade()
            )
        ))
        self.all.add(self.x_matrix)

        self.play(self.all.animate.shift(UP * 3))

    def get_qkv(self):
        wk_prism = Prism(
            dimensions=(3, 0.5, 3),
            fill_color=GRAY,
            fill_opacity=0.3,
            stroke_color=GOLD,
            stroke_width=1,
            stroke_opacity=1
        )
        wk_tex = MathTex(
            r"\boldsymbol{w}^q", font_size=40, color=GOLD
        ).next_to(wk_prism, LEFT, buff=2).shift(DOWN).rotate(PI / 2, RIGHT).rotate(PI / 2, IN)
        self.wk = VGroup(wk_prism, wk_tex)

        wq_prism = wk_prism.copy().set_stroke(color=BLUE).next_to(wk_prism, OUT)
        wq_tex = MathTex(
            r"\boldsymbol{w}^k", font_size=40, color=BLUE
        ).next_to(wq_prism, LEFT, buff=2).shift(DOWN).rotate(PI / 2, RIGHT).rotate(PI / 2, IN)
        self.wq = VGroup(wq_prism, wq_tex)

        wv_prism = wk_prism.copy().set_stroke(color=GREEN).next_to(wk_prism, IN)
        wv_tex = MathTex(
            r"\boldsymbol{w}^v", font_size=40, color=GREEN
        ).next_to(wv_prism, LEFT, buff=2).shift(DOWN).rotate(PI / 2, RIGHT).rotate(PI / 2, IN)
        self.wv = VGroup(wv_prism, wv_tex)

        self.play(
            FadeIn(wq_prism, wk_prism, wv_prism),
            Write(wq_tex),
            Write(wk_tex),
            Write(wv_tex)
        )
        self.all.add(self.wq, self.wk, self.wv)

        self.q_matrix = self.x_matrix.copy()
        self.k_matrix = self.x_matrix.copy()
        self.v_matrix = self.x_matrix.copy()

        self.play(
            self.q_matrix.animate.move_to(wq_prism.get_center()).fade(0.5),
            self.k_matrix.animate.move_to(wk_prism.get_center()).fade(0.5),
            self.v_matrix.animate.move_to(wv_prism.get_center()).fade(0.5)
        )

        np.random.seed(114)
        value = np.random.random((6, 5)).round(2)
        new_q = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(BLUE).move_to(self.q_matrix).shift(3 * DOWN).scale(0.7).rotate(PI / 2, axis=RIGHT)

        np.random.seed(514)
        value = np.random.random((6, 5)).round(2)
        new_k = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(GOLD).move_to(self.k_matrix).shift(3 * DOWN).scale(0.7).rotate(PI / 2, axis=RIGHT)

        np.random.seed(1919)
        value = np.random.random((6, 5)).round(2)
        new_v = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(GREEN).move_to(self.v_matrix).shift(3 * DOWN).scale(0.7).rotate(PI / 2, axis=RIGHT)

        self.play(
            Transform(self.q_matrix, new_q),
            Transform(self.k_matrix, new_k),
            Transform(self.v_matrix, new_v),
        )

        q_tex = MathTex(
            r"\boldsymbol{Q}", font_size=40, color=BLUE
        ).next_to(self.q_matrix, LEFT, buff=2).shift(DOWN).rotate(PI / 2, RIGHT).rotate(PI / 2, IN)
        k_tex = MathTex(
            r"\boldsymbol{K}", font_size=40, color=GOLD
        ).next_to(self.k_matrix, LEFT, buff=2).shift(DOWN).rotate(PI / 2, RIGHT).rotate(PI / 2, IN)
        v_tex = MathTex(
            r"\boldsymbol{V}", font_size=40, color=GREEN
        ).next_to(self.v_matrix, LEFT, buff=2).shift(DOWN).rotate(PI / 2, RIGHT).rotate(PI / 2, IN)
        self.play(
            Write(q_tex, run_time=0.5),
            Write(k_tex, run_time=0.5),
            Write(v_tex, run_time=0.5),
        )

        self.all.add(self.q_matrix, self.k_matrix, self.v_matrix, q_tex, k_tex, v_tex)

        self.play(self.all.animate.shift(UP * 6))

    def multi_head(self):
        self.liner1 = VGroup()

        mlp1_2 = Prism(
            dimensions=(0.5, 2, 5),
            fill_color=GRAY,
            fill_opacity=0.3,
            stroke_color=RED,
            stroke_width=1,
            stroke_opacity=1
        )

        mlp1_1 = mlp1_2.copy().next_to(mlp1_2, LEFT, buff=1.5)
        mlp1_3 = mlp1_2.copy().next_to(mlp1_2, RIGHT, buff=1.5)
        self.play(FadeIn(mlp1_1, mlp1_2, mlp1_3))
        self.liner1.add(mlp1_1, mlp1_2, mlp1_3)
        self.all.add(self.liner1)

        self.q_group = VGroup()
        q_1 = self.q_matrix.copy()
        q_2 = self.q_matrix.copy()
        q_3 = self.q_matrix.copy()

        self.play(
            q_1.animate.move_to(mlp1_1).rotate(PI / 2, axis=IN).fade(0.8),
            q_2.animate.move_to(mlp1_2).rotate(PI / 2, axis=IN).fade(0.8),
            q_3.animate.move_to(mlp1_3).rotate(PI / 2, axis=IN).fade(0.8),
        )

        np.random.seed(111)
        value = np.random.random((6, 5)).round(2)
        q_1_new = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(BLUE).move_to(
            mlp1_1
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 4 + OUT * 3.25).scale(0.7)

        np.random.seed(112)
        value = np.random.random((6, 5)).round(2)
        q_2_new = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(BLUE).move_to(
            mlp1_2
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 4 + OUT * 3.25).scale(0.7)

        np.random.seed(113)
        value = np.random.random((6, 5)).round(2)
        q_3_new = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(BLUE).move_to(
            mlp1_3
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 4 + OUT * 3.25).scale(0.7)

        self.play(
            Transform(q_1, q_1_new),
            Transform(q_2, q_2_new.fade(0.5)),
            Transform(q_3, q_3_new.fade(0.6)),
        )
        self.q_group.add(q_1, q_2, q_3)

        self.k_group = VGroup()
        k_1 = self.k_matrix.copy()
        k_2 = self.k_matrix.copy()
        k_3 = self.k_matrix.copy()

        self.play(
            k_1.animate.move_to(mlp1_1).rotate(PI / 2, axis=IN).fade(0.8),
            k_2.animate.move_to(mlp1_2).rotate(PI / 2, axis=IN).fade(0.8),
            k_3.animate.move_to(mlp1_3).rotate(PI / 2, axis=IN).fade(0.8),
        )

        np.random.seed(121)
        value = np.random.random((6, 5)).round(2)
        k_1_new = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(GOLD).move_to(
            mlp1_1
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 4).scale(0.7)

        np.random.seed(122)
        value = np.random.random((6, 5)).round(2)
        k_2_new = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(GOLD).move_to(
            mlp1_2
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 4).scale(0.7)

        np.random.seed(123)
        value = np.random.random((6, 5)).round(2)
        k_3_new = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(GOLD).move_to(
            mlp1_3
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 4).scale(0.7)

        self.play(
            Transform(k_1, k_1_new),
            Transform(k_2, k_2_new.fade(0.5)),
            Transform(k_3, k_3_new.fade(0.6)),
        )
        self.k_group.add(k_1, k_2, k_3)

        self.v_group = VGroup()
        v_1 = self.v_matrix.copy()
        v_2 = self.v_matrix.copy()
        v_3 = self.v_matrix.copy()

        self.play(
            v_1.animate.move_to(mlp1_1).rotate(PI / 2, axis=IN).fade(0.8),
            v_2.animate.move_to(mlp1_2).rotate(PI / 2, axis=IN).fade(0.8),
            v_3.animate.move_to(mlp1_3).rotate(PI / 2, axis=IN).fade(0.8),
        )

        np.random.seed(131)
        value = np.random.random((6, 5)).round(2)
        v_1_new = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(GREEN).move_to(
            mlp1_1
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 4 + IN * 3.25).scale(0.7)

        np.random.seed(132)
        value = np.random.random((6, 5)).round(2)
        v_2_new = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(GREEN).move_to(
            mlp1_2
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 4 + IN * 3.25).scale(0.7)

        np.random.seed(133)
        value = np.random.random((6, 5)).round(2)
        v_3_new = Matrix(
            value,
            v_buff=0.6,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(GREEN).move_to(
            mlp1_3
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 4 + IN * 3.25).scale(0.7)

        self.play(
            Transform(v_1, v_1_new),
            Transform(v_2, v_2_new.fade(0.5)),
            Transform(v_3, v_3_new.fade(0.6)),
        )
        self.v_group.add(v_1, v_2, v_3)

        # self.all.remove(self.sentence)
        self.all.add(self.q_group, self.k_group, self.v_group)
        self.play(self.all.animate.shift(UP * 4))

    def self_attention(self):
        def update_matrix(values: List[np.ndarray], shift: List[Vector3]) -> Tuple[Matrix, Matrix, Matrix]:
            _a_1_new = Matrix(
                values[0],
            ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).set_color(WHITE).move_to(a_1).shift(shift[0])

            _a_2_new = Matrix(
                values[1],
            ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).set_color(WHITE).move_to(a_2).shift(shift[1])

            _a_3_new = Matrix(
                values[2],
            ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).set_color(WHITE).move_to(a_3).shift(shift[2])

            return _a_1_new, _a_2_new, _a_3_new

        np.random.seed(111)
        q_1 = np.random.random((6, 5))
        np.random.seed(121)
        k_1 = np.random.random((6, 5))
        a_1_value: np.ndarray = np.matmul(q_1, k_1.T).round(2)

        a_1 = Matrix(
            a_1_value,
            v_buff=0.8,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(WHITE).move_to(
            self.q_group[0]
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 5 + IN * 1.5).scale(0.7)

        np.random.seed(112)
        q_2 = np.random.random((6, 5))
        np.random.seed(122)
        k_2 = np.random.random((6, 5))
        a_2_value: np.ndarray = np.matmul(q_2, k_2.T).round(2)

        a_2 = Matrix(
            a_2_value,
            v_buff=0.8,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(WHITE).move_to(
            self.q_group[1]
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 5 + IN * 1.5).scale(0.7)

        np.random.seed(131)
        q_3 = np.random.random((6, 5))
        np.random.seed(131)
        k_3 = np.random.random((6, 5))
        a_3_value: np.ndarray = np.matmul(q_3, k_3.T).round(2)

        a_3 = Matrix(
            a_3_value,
            v_buff=0.8,
            h_buff=1.2,
            bracket_v_buff=SMALL_BUFF,
            bracket_h_buff=SMALL_BUFF
        ).set_color(WHITE).move_to(
            self.q_group[2]
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).shift(DOWN * 5 + IN * 1.5).scale(0.7)

        self.play(
            Transform(
                VGroup(self.q_group.copy(), self.k_group.copy()),
                VGroup(a_1, a_2.fade(0.5), a_3.fade(0.6)),
                replace_mobject_with_target_in_scene=True
            )
        )

        self.all.add(a_1, a_2, a_3)
        self.play(self.all.animate.shift(UP * 4))

        commentary1 = MathTex(
            r"""\text{First, we use }\sqrt{dim_k}\\ 
            \text{to scale the result of dot product}""",
            color=YELLOW,
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_corner(DR)
        self.play(Write(commentary1))
        self.wait(0.8)
        self.play(FadeOut(commentary1))

        scale_prism = Prism(
            dimensions=(6, 0.5, 3),
            fill_color=YELLOW_A,
            fill_opacity=0.3,
            stroke_color=YELLOW,
            stroke_width=1,
            stroke_opacity=1
        ).next_to(a_2, DOWN, buff=0.8)
        scale_tex = Text(
            "Scale", font_size=30, color=YELLOW
        ).next_to(scale_prism, LEFT, buff=2.5).shift(DOWN + IN).rotate(PI / 2, RIGHT).rotate(PI / 2, IN)
        self.scale_block = VGroup(scale_prism, scale_tex)

        self.play(FadeIn(self.scale_block))
        self.all.add(self.scale_block)

        a_1_value = (a_1_value / math.sqrt(6)).round(2)
        a_2_value = (a_2_value / math.sqrt(6)).round(2)
        a_3_value = (a_3_value / math.sqrt(6)).round(2)
        a_1_new, a_2_new, a_3_new = update_matrix([a_1_value, a_2_value, a_3_value], [DOWN * 4, DOWN * 4, DOWN * 4])

        self.play(
            Transform(a_1, a_1_new.scale(0.7)),
            Transform(a_2, a_2_new.fade(0.5).scale(0.7)),
            Transform(a_3, a_3_new.fade(0.6).scale(0.7)),
            self.scale_block.animate.shift(UP * 4)
        )
        a_group = VGroup(a_1, a_2, a_3)
        self.all.add(a_group)

        mask = np.zeros((6, 6))
        mask[np.triu_indices(6, 1)] = np.NINF
        mask_matrix = Matrix(
            mask
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).set_color(WHITE)

        self.play(self.all.animate.shift(UP * 3.5))

        a1_pos, a2_pos, a3_pos = a_1.get_center(), a_2.get_center(), a_3.get_center()
        self.play(a_2.animate.shift(1.75 * IN).fade(-1))
        self.play(
            a_1.animate.next_to(a_2, OUT),
            a_3.animate.next_to(a_2, IN).fade(-1.5)
        )
        self.play(self.all.animate.shift(UP))

        text = Text(
            "Mask", font_size=30, color=YELLOW
        ).rotate(PI / 2, RIGHT).rotate(PI / 2, IN)
        self.play(
            FadeIn(mask_matrix.next_to(a_2, DOWN).scale(0.7)),
            Write(text.next_to(mask_matrix, IN))
        )

        commentary1 = MathTex(
            r"""\text{Here, we use a mask matrix}\\ 
            \text{to implement masking}\\
            \text{of the subsequent words.}""",
            color=YELLOW,
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_corner(UR)
        self.play(Write(commentary1))
        self.wait(0.8)
        self.play(FadeOut(commentary1))
        self.play(Unwrite(text))

        a_1_value = a_1_value + mask
        a_2_value = a_2_value + mask
        a_3_value = a_3_value + mask

        a_1_new, a_2_new, a_3_new = update_matrix([a_1_value, a_2_value, a_3_value], [ORIGIN, ORIGIN, ORIGIN])

        self.play(
            Succession(
                mask_matrix.copy().animate.move_to(a_1).fade(1),
                Transform(a_1, a_1_new.scale(0.7)),
            ),
            Succession(
                mask_matrix.copy().animate.move_to(a_2).fade(1),
                Transform(a_2, a_2_new.scale(0.7)),
            ),
            Succession(
                mask_matrix.animate.move_to(a_3).fade(1),
                Transform(a_3, a_3_new.scale(0.7)),
            ),
        )

        self.play(
            a_1.animate.move_to(a1_pos),
            a_2.animate.move_to(a2_pos).fade(0.5),
            a_3.animate.move_to(a3_pos).fade(0.6),
        )

        sigmoid_prism = Prism(
            dimensions=(6, 0.5, 3),
            fill_color=PINK,
            fill_opacity=0.3,
            stroke_color=LIGHT_PINK,
            stroke_width=1,
            stroke_opacity=1
        ).next_to(a_2, DOWN, buff=0.8)
        sigmoid_tex = Text(
            "Sigmoid", font_size=30, color=PINK
        ).next_to(sigmoid_prism, LEFT, buff=2.5).shift(DOWN + IN).rotate(PI / 2, RIGHT).rotate(PI / 2, IN)
        self.sigmoid_block = VGroup(sigmoid_prism, sigmoid_tex)

        self.play(FadeIn(self.sigmoid_block))
        self.all.add(self.sigmoid_block)

        commentary1 = MathTex(
            r"""\text{The masked matrix passed through a sigmoid function}\\ 
            \text{and the values of the masked parts turned into }0""",
            color=YELLOW,
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_corner(DR)
        self.play(Write(commentary1))
        self.wait(0.8)
        self.play(FadeOut(commentary1))

        a_1_value = sigmoid(a_1_value)
        a_2_value = sigmoid(a_2_value)
        a_3_value = sigmoid(a_3_value)
        a_1_new, a_2_new, a_3_new = update_matrix([a_1_value, a_2_value, a_3_value], [DOWN * 3, DOWN * 3, DOWN * 3])

        self.play(
            Transform(a_1, a_1_new.scale(0.7)),
            Transform(a_2, a_2_new.fade(0.5).scale(0.7)),
            Transform(a_3, a_3_new.fade(0.6).scale(0.7)),
            self.sigmoid_block.animate.shift(UP * 5.5)
        )

        self.play(Indicate(self.v_group, color=PURE_GREEN))

        np.random.seed(131)
        v_1 = np.random.random((6, 5))
        a_1_value = np.matmul(a_1_value, v_1).round(2)

        np.random.seed(132)
        v_2 = np.random.random((6, 5))
        a_2_value = np.matmul(a_2_value, v_2).round(2)

        np.random.seed(133)
        v_3 = np.random.random((6, 5))
        a_3_value = np.matmul(a_3_value, v_3).round(2)

        a_1_new, a_2_new, a_3_new = update_matrix([a_1_value, a_2_value, a_3_value], [ORIGIN, ORIGIN, ORIGIN])
        self.play(
            Succession(
                self.v_group[0].copy().animate.move_to(a_1).fade(1),
                Transform(a_1, a_1_new.scale(0.7)),
                lag_ratio=0.98
            ),
            Succession(
                self.v_group[1].copy().animate.move_to(a_2).fade(1),
                Transform(a_2, a_2_new.scale(0.7).fade(0.5)),
                lag_ratio=0.98
            ),
            Succession(
                self.v_group[2].copy().animate.move_to(a_3).fade(1),
                Transform(a_3, a_3_new.scale(0.7).fade(0.6)),
                lag_ratio=0.98
            ),
        )

        commentary1 = MathTex(
            r"""\text{The above process is the calculation of masked-attention:}""",
            color=YELLOW,
            font_size=30
        )
        commentary2 = MathTex(
            r"""\text{Attention}(Q,K,V)=\text{softmax}\left({ QK^T \over \sqrt{dim_k} }+\mathbf{A}_{mask}\right)V""",
            tex_to_color_map={
                r'Q': BLUE,
                r'K': GOLD,
                r'V': GREEN,
            },
            color=WHITE,
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary2.to_corner(DR)
        commentary1.next_to(commentary2, UP)
        self.play(Write(commentary1))
        self.add_fixed_in_frame_mobjects(commentary2)
        self.play(Write(commentary2))
        self.wait(2)
        self.play(FadeOut(commentary1, commentary2))
        commentary1 = MathTex(
            r"""\text{Finally, we concatenate the outputs from different heads}\\ 
            \text{and transform them to the same dimension as the beginning through a MLP}""",
            color=YELLOW,
            font_size=30
        )
        self.add_fixed_in_frame_mobjects(commentary1)
        commentary1.to_corner(DR)
        self.play(Write(commentary1))
        self.wait(0.8)
        self.play(FadeOut(commentary1))

        a_out = np.concatenate((a_1_value, a_2_value, a_3_value), axis=0)
        a_out_matrix = Matrix(
            a_out,
        ).rotate(PI / 2, axis=IN).rotate(PI / 2, axis=DOWN).set_color(WHITE)

        self.all.remove(a_group)
        self.play(Transform(
            a_group,
            a_out_matrix.scale(0.7).move_to(DOWN * 3),
            replace_mobject_with_target_in_scene=True
        ))

        self.all.add(a_out_matrix)
        self.play(self.all.animate.shift(UP * 3))

        phi, theta, focal_distance, gamma, zoom = self.camera.get_value_trackers()
        self.play(zoom.animate.set_value(0.7))

        self.play(Indicate(a_out_matrix.get_rows()[:6]))
        self.play(Indicate(a_out_matrix.get_rows()[6:12]))
        self.play(Indicate(a_out_matrix.get_rows()[12:]))

        self.liner2 = Prism(
            dimensions=(5, 0.5, 4),
            fill_color=GRAY,
            fill_opacity=0.3,
            stroke_color=PURPLE,
            stroke_width=1,
            stroke_opacity=1
        ).next_to(a_out_matrix, DOWN, buff=1)

        self.play(FadeIn(self.liner2))

        self.all.add(self.liner2)
        self.play(self.all.animate.shift(UP * 2))

        y_value = np.random.random((6, 5)).round(2)
        self.y_matrix = Matrix(
            y_value,
        ).set_color(PURPLE_A).move_to(self.liner2).rotate(PI / 2, axis=RIGHT)

        self.all.remove(a_out_matrix)
        self.play(
            Transform(
                a_out_matrix,
                self.y_matrix.scale(0.5).fade(0.5),
                replace_mobject_with_target_in_scene=True
            )
        )
        self.play(self.y_matrix.animate.shift(DOWN).scale(2).fade(-1))
        self.all.add(self.y_matrix)
