import arcade
import constants

class Car():
    def __init__(self):
        self.image = constants.CAR_IMG0
        self.height = constants.CAR_HEIGHT
        self.x = constants.CAR_X
        self.y = constants.CAR_Y
        self.car = arcade.Sprite(filename=self.image, center_x=self.x, center_y=self.y)
        self.sprites = arcade.SpriteList()

    def draw(self):
        self.sprites.draw()
    
    def update_image(self):
        if self.image == constants.CAR_IMG0:
            self.image= constants.CAR_IMG1
        elif self.image == constants.CAR_IMG1:
            self.image = constants.CAR_IMG2
        elif self.image == constants.CAR_IMG2:
            self.image = constants.CAR_IMG3

        # I set a new position in case it was drawing another behind the first
        self.center_x = 200
        
        # I even tried creating a new one altogether...
        self.create_car()
        # and drawing the list again
        self.draw()

    def create_car(self):
        self.car = arcade.Sprite(filename=self.image, center_x=self.x, center_y=self.y)
        self.sprites.append(self.car)