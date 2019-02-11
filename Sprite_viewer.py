import arcade
import random
import time
import timeit
import collections
import pyglet.gl as gl

SPRITE_SCALING = 1
SPRITE_INCREMENT = 1000

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        super().__init__(width, height, "Sprite Viewer", fullscreen=True)

        self.fullscreen_width, self.fullscreen_height = self.get_size()

        # Set up the sprite info
        self.sprite_list = arcade.SpriteList()

        # Set up timer
        self.processing_time = 0
        self.draw_time = 0
        self.program_start_time = timeit.default_timer()
        self.sprite_count_list = []
        self.fps_list = []
        self.processing_time_list = []
        self.drawing_time_list = []
        self.last_fps_reading = 0
        self.fps = FPSCounter()

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        """ Set up the game and initialize the variables. """
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        draw_start_time = timeit.default_timer()

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.sprite_list.draw()

        # Display info on sprites
        output = f"Sprite count: {len(self.sprite_list):,}"
        arcade.draw_text(output, 20, self.fullscreen_height - 20, arcade.color.BLACK, 16)

        # Display timings
        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(output, 20, self.fullscreen_height - 40, arcade.color.BLACK, 16)

        fps = self.fps.get_fps()
        output = f"FPS: {fps:3.0f}"
        arcade.draw_text(output, 20, self.fullscreen_height - 60, arcade.color.BLACK, 16)

        self.draw_time = timeit.default_timer() - draw_start_time
        self.fps.tick()

        gl.glFlush()

    def update(self, delta_time):
        # Total time program has been running
        total_program_time = int(timeit.default_timer() - self.program_start_time)

        # Print out stats, or add more sprites
        if total_program_time > self.last_fps_reading:
            self.last_fps_reading = total_program_time

            # It takes the program a while to "warm up", so the first
            # few seconds our readings will be off. So wait some time
            # before taking readings
            if total_program_time > 5:

                # We want the program to run for a while before taking
                # timing measurements. We don't want the time it takes
                # to add new sprites to be part of that measurement. So
                # make sure we have a clear second of nothing but
                # running the sprites, and not adding the sprites.
                if total_program_time % 5 == 1:
                    # Take timings
                    print(
                        f"{total_program_time}, {len(self.sprite_list)}, {self.fps.get_fps():.1f}, {self.processing_time:.4f}, {self.draw_time:.4f}")
                    self.sprite_count_list.append(len(self.sprite_list))
                    self.fps_list.append(round(self.fps.get_fps(), 1))
                    self.processing_time_list.append(self.processing_time)
                    self.drawing_time_list.append(self.draw_time)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.SPACE:
            # Create the sprites
            for i in range(SPRITE_INCREMENT):

                # Create the sprite instance
                sprite = arcade.Sprite("sprites/rain.png", scale=SPRITE_SCALING)

                # Position the sprite
                sprite.center_x = random.randrange(self.fullscreen_width)
                sprite.center_y = random.randrange(self.fullscreen_height)

                # Add the sprites to the lists
                self.sprite_list.append(sprite)

        if key == arcade.key.ESCAPE:
            arcade.window_commands.close_window()


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()