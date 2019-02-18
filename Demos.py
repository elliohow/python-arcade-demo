import arcade
from rain import Rain
from double_pendulum import DoublePendulum
from user_interface import UserInterface

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800


class DemoWindow(arcade.Window):
    """
    Main application class.
    """
    DemoKey = 0
    Demos = [Rain,
             DoublePendulum]
    pause = True

    def __init__(self, width, height):
        super().__init__(width, height, "Demo", fullscreen=True)

        self.sprite_list = None

        self.fullscreen_width, self.fullscreen_height = self.get_size()

        # UserInterface.setup(self)

    def setup(self):
        """
        Set update rate and initialise sprite classes.
        """
        current_demo = self.Demos[self.DemoKey]

        arcade.set_background_color(current_demo.BACKGROUND_COLOUR)

        self.sprite_list = arcade.SpriteList(use_spatial_hash=False)  # Disable collision detecting to improve speed

        for i in range(current_demo.SPRITE_AMOUNT):
            sprite_init = current_demo(self)
            self.sprite_list.append(sprite_init.sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # Clear the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        self.sprite_list.draw()

        #for button in UserInterface.button_list:
        #    button.draw()

    def update(self, delta_time):
        """
        Update the sprites.
        """

        #if self.pause:
        #    return

        # TODO: Make this more efficient using built in sprite_list update method
        for sprite in self.sprite_list:
            sprite.update(self)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """

        if key == arcade.key.ESCAPE:
            arcade.window_commands.close_window()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """

        # UserInterface.press_mouse(x, y, self)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """

        # UserInterface.release_mouse()


def main():
    window = DemoWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
