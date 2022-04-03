import arcade
import constants
import math
import time
class Car():
    def __init__(self):
        self.image = constants.CAR_IMG0
        self.x = constants.CAR_X
        self.y = constants.CAR_Y
        self.car = arcade.Sprite(filename=self.image, center_x=self.x, center_y=self.y)
        self.sprites = arcade.SpriteList()
        self.direction = 0

    def draw(self):
        # make sure we only have one
        if len(self.sprites) > 0:
            self.sprites.pop()
        self.sprites.append(self.car)
        self.sprites.draw()
        
    def update_image(self):
        if self.image == constants.CAR_IMG0:
            self.image= constants.CAR_IMG1
        elif self.image == constants.CAR_IMG1:
            self.image = constants.CAR_IMG2
        elif self.image == constants.CAR_IMG2:
            self.image = constants.CAR_IMG3
        elif self.image == constants.CAR_IMG3:
            self.image = constants.CAR_IMG0

        # create a new car to replace the old one
        self.create_car()
        self.draw()

    def create_car(self):
        self.car = arcade.Sprite(filename=self.image, center_x=self.x, center_y=self.y)

    def bounce_car(self):

        if self.car.center_y >= 30:
            self.direction = 1
        elif self.car.center_y <= 20:
            self.direction = 0
        
        if self.direction:
            self.car.center_y -= 0.5
        else:
            self.car.center_y += 0.5
