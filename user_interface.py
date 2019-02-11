import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class UserInterface:
    button_list = []

    @classmethod
    def setup(cls, window):
        """Start, pause, previous, next"""

        play_button = Button(window.fullscreen_width - 50, window.fullscreen_height - 25, 100, 50, "Play")
        next_button = Button(window.fullscreen_width - 50, 25, 100, 50, "Next")
        previous_button = Button(next_button.center_x - 100, next_button.center_y, 100, 50, "Previous")

        cls.button_list.extend((play_button, next_button, previous_button))

    @classmethod
    def press_mouse(cls, x, y, window):
        for button in cls.button_list:
            button.check_button_press(x, y, window)

    @classmethod
    def release_mouse(cls):
        for button in cls.button_list:
            button.pressed = False


class Button:

    @staticmethod
    def pause_program(self, window):
        window.pause = True
        self.change_action("Play")

    @staticmethod
    def resume_program(self, window):
        window.pause = False
        self.change_action("Pause")

    @staticmethod
    def next_demo(self, window):
        window.DemoKey += 1
        window.setup()

    @staticmethod
    def previous_demo(self, window):
        window.DemoKey -= 1
        window.setup()

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):

        button_action = {"Play": Button.resume_program,
                         "Pause": Button.pause_program,
                         "Next": Button.next_demo,
                         "Previous": Button.previous_demo}

        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.action_function = button_action[text]
        self.font_size = font_size
        self.font_face = font_face
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height
        self.pressed = False

    def change_action(self, text):

        button_action = {"Play": Button.resume_program,
                         "Pause": Button.pause_program,
                         "Next": Button.next_demo,
                         "Previous": Button.previous_demo}
        self.text = text
        self.action_function = button_action[text]

    def draw(self):
        """ Draw the button """

        x = self.center_x
        y = self.center_y

        if self.pressed:
            color_br = self.highlight_color
            color_tr = self.shadow_color
            x += self.button_height
            y -= self.button_height
        else:
            color_br = self.shadow_color
            color_tr = self.highlight_color

        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color_br, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color_br, self.button_height)

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color_tr, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color_tr, self.button_height)

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def check_button_press(self, x, y, window):
        """ Given an x, y, see if we need to register any button clicks. """

        max_x = self.center_x + self.width / 2
        min_x = self.center_x - self.width / 2
        max_y = self.center_y + self.height / 2
        min_y = self.center_y - self.height / 2

        if min_x <= x <= max_x and min_y <= y <= max_y:
            self.pressed = True
            self.action_function(self, window)


def main():
    """ Main method """
    window = Test(SCREEN_WIDTH, SCREEN_HEIGHT, UserInterface, (100, 100, 100))
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
