import arcade
from math import pi, sin, cos
from random import randint

# Initial constant set
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800


class DoublePendulum:
    BACKGROUND_COLOUR = (256, 256, 256)
    SPRITE_AMOUNT = 1

    def __init__(self, window):
        self.length1 = 200
        self.length2 = 200
        self.mass1 = 20
        self.mass2 = 20
        self.angle1 = pi / 2
        self.angle2 = pi / 2
        self.angle1dampening = 0
        self.angle2dampening = 0
        self.angle1velocity = 0
        self.angle2velocity = 0
        self.gravity = 1

        self.offsetX = window.fullscreen_width * 0.5
        self.offsetY = window.fullscreen_height * 0.7
        self.color = (1, 1, 1)

        self.linewidth = 20
        self.trailwidth = 5
        # TODO remove initial traillist values
        self.traillist = [20, 20]
        self.angle1acceleration = None
        self.angle2acceleration = None
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None

        self.coordinate_calculate()
        self.primitive_create()

    def primitive_create(self):
        circle1 = arcade.create_ellipse_filled(self.x1, self.y1, self.mass1, self.mass1, self.color)
        circle2 = arcade.create_ellipse_filled(self.x2, self.y2, self.mass2, self.mass2, self.color)
        line1 = arcade.create_line(self.offsetX, self.offsetY, self.x1, self.y1, self.color, self.linewidth)
        line2 = arcade.create_line(self.x1, self.y1, self.x2, self.y2, self.color, self.linewidth)
        trail = arcade.create_line_strip(self.traillist, self.color, self.trailwidth)

        self.circle1 = arcade.ShapeElementList()
        self.circle1.append(circle1)

        self.circle2 = arcade.ShapeElementList()
        self.circle2.append(circle2)

        self.line1 = arcade.ShapeElementList()
        self.line1.append(line1)

        self.line2 = arcade.ShapeElementList()
        self.line2.append(line2)

        self.trail = arcade.ShapeElementList()

    def angle_calculate(self):
        """
        Calculate acceleration for angle 1 and 2,
        change velocity and angle based on this calculation,
        then dampen angle velocity.
        """
        # Calculate angular acceleration for angle 1
        num1 = self.gravity * (2 * self.mass1 + self.mass2) * sin(self.angle1)
        num2 = -self.mass2 * -self.gravity * sin(self.angle1 - 2 * self.angle2)
        num3 = -2 * sin(self.angle1 - self.angle2) * self.mass2
        num4 = self.angle2velocity * self.angle2velocity * self.length2
        num5 = self.angle1velocity * self.angle1velocity * self.length1 * cos(self.angle1 - self.angle2)
        den = self.length1 * (2 * self.mass1 + self.mass2 - self.mass2 * cos(2 * self.angle1 - 2 * self.angle2))
        self.angle1acceleration = (num1 + num2 + num3 * (num4 + num5)) / den

        # Calculate angular acceleration for angle 2
        num1 = 2 * sin(self.angle1 - self.angle2)
        num2 = (self.angle1velocity * self.angle1velocity * self.length1 * (self.mass1 + self.mass2))
        num3 = -self.gravity * (self.mass1 + self.mass2) * cos(self.angle1)
        num4 = self.angle2velocity * self.angle2velocity * self.length2 * self.mass2 * cos(self.angle1 - self.angle2)
        den = self.length2 * (2 * self.mass1 + self.mass2 - self.mass2 * cos(2 * self.angle1 - 2 * self.angle2))
        self.angle2acceleration = num1 * (num2 + num3 + num4) / den

        # Change angular velocity and angle based on angular acceleration
        self.angle1velocity += self.angle1acceleration
        self.angle2velocity += self.angle2acceleration
        self.angle1 += self.angle1velocity
        self.angle2 += self.angle2velocity

        # Dampen angular velocity
        self.angle1velocity = (1 - self.angle1dampening) * self.angle1velocity
        self.angle2velocity = (1 - self.angle2dampening) * self.angle2velocity

    def coordinate_calculate(self):
        """
        Calculate coordinates based on angle.
        """
        self.x1 = (self.length1 * sin(self.angle1)) + self.offsetX
        self.y1 = (self.length1 * cos(self.angle1)) + self.offsetY
        self.x2 = self.x1 + self.length2 * sin(self.angle2)
        self.y2 = self.y1 + self.length2 * cos(self.angle2)

        self.circle1.center_x = self.x1
        self.circle1.center_y = self.y1

        self.circle2.center_x = self.x2
        self.circle2.center_y = self.y2

    def draw(self):
        """
        Render the Double Pendulum's trail, 2 circles and 2 lines.
        """

        VertexBufferObjects = []

        VertexBufferObjects.extend((circle1, circle2, line1, line2, trail))

        for VBO in VertexBufferObjects:
            arcade.render(VBO)

    def update(self, window):
        """
        Update the trail points then calculate the new angle and coordinates of the pendulum.
        """
        self.traillist.append((self.x2, self.y2))
        self.angle_calculate()
        self.coordinate_calculate()


def main():
    window = Test(SCREEN_WIDTH, SCREEN_HEIGHT, DoublePendulum, DoublePendulum.BACKGROUND_COLOUR)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
