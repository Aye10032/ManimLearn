from typing import Tuple

import numpy as np
from manim import *
from manim import VGroup, Arrow


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
            width=0.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=BLUE
        )
        q1_tex = MathTex(r"x^1", color=BLUE).next_to(q1_rect, DOWN)
        q1 = VGroup(q1_rect, q1_tex).scale(0.8).move_to(LEFT + UP * 2.8)

        q2_rect = Rectangle(
            width=0.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=BLUE
        )
        q2_tex = MathTex(r"x^2", color=BLUE).next_to(q2_rect, DOWN)
        q2 = VGroup(q2_rect, q2_tex).scale(0.8).move_to(LEFT)

        q3_rect = Rectangle(
            width=0.5, height=2.0, grid_xstep=0.5, grid_ystep=0.5, stroke_width=6, color=BLUE
        )
        q3_tex = MathTex(r"x^3", color=BLUE).next_to(q3_rect, DOWN)
        q3 = VGroup(q3_rect, q3_tex).scale(0.8).move_to(LEFT + DOWN * 2.8)

        self.play(
            Write(q1),
            Write(q2),
            Write(q3),
        )
        self.wait()

        commentary1 = MathTex(
            r"&\text{...and here,}\\ &\text{we get the input vector }x^i",
            tex_to_color_map={r"x^i": BLUE}
        ).move_to(RIGHT * 3)
        self.play(Write(commentary1))

        self.wait(2)

        self.play(
            FadeOut(a1, a2, a3),
            FadeOut(tex1_plus, tex2_plus, tex3_plus),
            FadeOut(d1, d2, d3),
            FadeOut(tex1_eq, tex2_eq, tex3_eq),
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
            width=2, height=0.5, grid_xstep=0.5, grid_ystep=1, stroke_width=6, color=PURPLE
        ).move_to(RIGHT * 2 + DOWN * 1.5)

        d_tex = MathTex(tex_text, color=PURPLE).next_to(d_rec, DOWN)

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


class EncoderAndDecoder(Scene):
    def construct(self):
        pass
