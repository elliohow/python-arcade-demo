import arcade
from random import randrange
from numpy import interp, arange, random

# Initial constant set
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800


class Rain:
    # BACKGROUND_COLOUR = (30, 50, 50) # Original BG colour
    BACKGROUND_COLOUR = (255, 255, 255) # New bg colour until color is fixed
    RAIN_COLOUR = (0, 100, 150)
    SPRITE_AMOUNT = 1000
    z1 = 1
    z2 = 4
    light_rainfall = True

    def __init__(self, window):
        self.sprite = arcade.Sprite("sprites/rain.png")

        self.reset(window)

        self.sprite.color = (0, 100, 150) # Why doesn't this work?
        self.sprite.update = self.update

    def reset(self, window):
        _ = self.sprite
        _.center_x = randrange(0, window.fullscreen_width)
        _.center_y = randrange(window.fullscreen_height, window.fullscreen_height * 1.2)

        self.z = random.choice(arange(self.z1, self.z2), p=[0.05, 0.25, 0.7])

        if Rain.light_rainfall == True:
            _.center_y = randrange(window.fullscreen_height, window.fullscreen_height * 10)
            self.initial_speed = interp(self.z, [self.z1, self.z2 - 1], [50, 20])
        else:
            _.center_y = randrange(window.fullscreen_height, window.fullscreen_height * 1.2)
            self.initial_speed = interp(self.z, [self.z1, self.z2 - 1], [80, 40])

        self.jitter = randrange(5, 12, 1)  # randrange only works with integers
        self.yspeed = self.initial_speed * (self.jitter/10)  # Convert jitter to float between 0.5 and 1.2 in step 0.1

        self.length = interp(self.z, [self.z1, self.z2 - 1], [40, 10])
        self.width = interp(self.z, [self.z1, self.z2 - 1], [3, 1])
        _.width = self.width
        _.height = self.length

    def update(self, window):
        self.sprite.center_y = self.sprite.center_y - self.yspeed

        if self.sprite.center_y < 0 and Rain.light_rainfall == True:
            Rain.light_rainfall = False
            self.reset(window)

        if self.sprite.center_y < 0:
            self.reset(window)
