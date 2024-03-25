from manim import *
import numpy as np


class SinAndCosFunctionPlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10.3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            axis_config={'color': GREEN},
            x_axis_config={
                'numbers_to_include': np.arange(-10, 10.1, 2),
                'numbers_with_elongated_ticks': np.arange(-10, 10.1, 2)
            }
        )

        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED)

        plot = VGroup(axes, sin_graph, cos_graph)

        axe_label = axes.get_axis_labels()
        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)", x_val=-10, direction=np.array([0.0, 0.8, 0.0]))
        cos_label = axes.get_graph_label(cos_graph, "\\cos(x)", x_val=-10, direction=np.array([0.0, -1.2, 0.0]))
        vert_line = axes.get_vertical_line(
            axes.i2gp(TAU, cos_graph), color=YELLOW, line_func=Line
        )
        line_label = axes.get_graph_label(
            cos_graph, "x=2\\pi", x_val=TAU, direction=np.array([0.0, 1.2, 0.0]), color=WHITE
        )

        labels = VGroup(axe_label, sin_label, cos_label, vert_line, line_label)
        self.add(plot, labels)


class ArgMinExample(Scene):
    def construct(self):
        axe = Axes(
            x_range=[0, 10],
            y_range=[0, 100, 10],
            axis_config={"include_tip": False}
        )
        labels = axe.get_axis_labels(x_label='x', y_label='f(x)')

        t = ValueTracker(0)

        def func(x):
            return 2 * (x - 5) ** 2

        graph = axe.plot(func, color=MAROON)

        p0 = np.array([axe.coords_to_point(t.get_value(), func(t.get_value()))])
        dot = Dot(point=p0)

        self.add(axe, labels, graph, dot)

        def update_func(mobj: Mobject):
            mobj.move_to(axe.c2p(t.get_value(), func(t.get_value())))

        dot.add_updater(update_func)
        x_space = np.linspace(*axe.x_range[:2], 200)
        min_index = func(x_space).argmin()

        self.play(t.animate.set_value(x_space[min_index]))
        self.wait()


class GraphArePlot(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 6],
            x_axis_config={'numbers_to_include': [2, 3]},
            tips=True
        )
        labels = ax.get_axis_labels()

        self.add(ax, labels)

        def func1(_x):
            return 4 * _x - _x ** 2

        def func2(_x):
            return 0.8 * _x ** 2 - 3 * _x + 4

        curve1 = ax.plot(func1, x_range=np.array([0, 4]), color=BLUE_C)
        curve2 = ax.plot(func2, x_range=np.array([0, 4]), color=GREEN_B)

        line1 = ax.get_vertical_line(ax.input_to_graph_point(2, curve1), color=YELLOW)
        line2 = ax.get_vertical_line(ax.i2gp(3, curve2), color=YELLOW)

        self.add(curve1, curve2, line1, line2)

        area1 = ax.get_riemann_rectangles(curve1, x_range=np.array([0.3, 0.6]), dx=0.03, color=BLUE, fill_opacity=0.5)
        area2 = ax.get_area(curve2, (2, 3), bounded_graph=curve1, color=GRAY, opacity=0.5)

        self.add(area1, area2)
