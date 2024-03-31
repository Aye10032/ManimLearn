from manim import *
import numpy as np


class FollowingGraphCamera(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()

        ax = Axes(
            x_range=[-1, 10],
            y_range=[-1, 10]
        )
        graph = ax.plot(lambda x: np.sin(x), color=BLUE, x_range=[0, 3 * PI])
        moving_dot = Dot(ax.i2gp(graph.t_min, graph), color=ORANGE)

        self.add(ax, graph, moving_dot)
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))

        def update_curve(mob: Mobject):
            mob.move_to(moving_dot.get_center())

        self.camera.frame.add_updater(update_curve)

        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear), run_time=2)
        self.camera.frame.remove_updater(update_curve)

        self.play(Restore(self.camera.frame))


class MovingZoomedSceneAround(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=1,
            zoomed_display_width=6,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )

    def construct(self):
        dot = Dot().shift(UL * 2)
        image = ImageMobject(np.uint8([[0, 100, 30, 200],
                                       [255, 0, 5, 22]]))

        image.height = 8
        self.add(image, dot)

        zoom_camera = self.zoomed_camera
        zoom_display = self.zoomed_display
        camera_frame = zoom_camera.frame
        zoom_frame = zoom_display.display_frame

        camera_frame.move_to(dot)
        camera_frame.set_color(PURPLE)
        zoom_frame.set_color(RED)
        zoom_display.shift(DOWN)

        zd_rect = BackgroundRectangle(zoom_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self.add_foreground_mobject(zd_rect)

        def update_rect(rect: Mobject):
            rect.replace(zoom_display)

        unfold_camera = UpdateFromFunc(zd_rect, update_rect)

        frame_text = Text("Frame", color=PURPLE, font_size=67)
        frame_text.next_to(camera_frame, DOWN)

        self.play(Create(camera_frame), FadeIn(frame_text, shift=UP))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)

        camera_text = Text("Zoom", color=RED, font_size=67)
        camera_text.next_to(zoom_frame, DOWN)
        self.play(FadeIn(camera_text))

        scale_factor = [0.5, 1.5, 0]
        self.play(
            camera_frame.animate.scale(scale_factor),
            zoom_display.animate.scale(scale_factor),
            FadeOut(camera_text, frame_text)
        )
        self.wait()
        self.play(ScaleInPlace(zoom_display, 2))
        self.wait()
        self.play(camera_frame.animate.shift(2.5 * DOWN))
        self.wait()
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera, rate_func=lambda t: smooth(1 - t))
        self.play(Uncreate(zoom_frame), FadeOut(camera_frame))
        self.wait()


class FixedInFrameMObjectTest(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        text3d = Text("This is 3D Object")
        self.add_fixed_in_frame_mobjects(text3d)
        text3d.to_corner(UL)
        self.add(ax)
        self.wait()


class ThreeDLightSourcePosition(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()

        def surface_func(u, v):
            return np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ])

        sphere = Surface(
            surface_func,
            v_range=[0, TAU],
            u_range=[-PI / 2, PI / 2],
            checkerboard_colors=[RED_D, RED_E],
            resolution=(15, 32)
        )

        self.renderer.camera.light_source.move_to(3 * IN)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(ax, sphere)


class ThreeDCameraRotation(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        circle = Circle()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(circle, ax)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait()
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        self.wait()


class ThreeDCameraIllusionRotation(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        circle = Circle()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(circle, ax)

        self.begin_3dillusion_camera_rotation(rate=2)
        self.wait()
        self.stop_3dillusion_camera_rotation()
