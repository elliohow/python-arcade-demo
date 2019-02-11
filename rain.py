import arcade
from random import randrange
from numpy import interp, arange, random

# Initial constant set
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800


class Rain:
    BACKGROUND_COLOUR = (30, 50, 50)
    RAIN_COLOUR = (0, 100, 150)
    SPRITE_AMOUNT = 400
    z1 = 1
    z2 = 4

    def __init__(self, window):
        self.reset(window)

        self.sprite = arcade.Sprite("sprites/rain.png")
        self.sprite.color = (0, 100, 150) # Why doesn't this work?
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        self.sprite.width = self.width
        self.sprite.height = self.length

        self.sprite.update = self.update

    def reset(self, window):
        self.x = randrange(0, window.fullscreen_width)
        self.y = randrange(window.fullscreen_height, window.fullscreen_height * 4)
        self.z = random.choice(arange(self.z1, self.z2), p=[0.05, 0.25, 0.7])
        self.length = interp(self.z, [self.z1, self.z2 - 1], [30, 10])
        self.yspeed = interp(self.z, [self.z1, self.z2 - 1], [60, 20])
        self.gravity = interp(self.z, [self.z1, self.z2 - 1], [0.3, 0.1])
        self.width = interp(self.z, [self.z1, self.z2 - 1], [5, 1])

    def update(self, window):
        self.y = self.y - self.yspeed
        self.yspeed += self.gravity

        # Change Sprite location
        self.sprite.center_y = self.y

        if self.y < 0:
            self.reset(window)
