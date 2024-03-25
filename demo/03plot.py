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
