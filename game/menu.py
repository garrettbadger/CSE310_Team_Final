import arcade
import arcade.gui


import constants

# This class is used to create a button that is supposed to call a new view with a rectangle in it
class GameButton1(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
        start_view = MainMenu()
        window.show_view(start_view)
        arcade.run()
# This is essentially the same as GameButton1
class GameButton2(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
        start_view = MainMenu()
        window.show_view(start_view)
        arcade.run()
# This class creates a button that quits the program
class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()
# This creates a UI manager to hold the buttons and then calls them and adds them to the v_box 
class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        game1_button = GameButton1(text="Game 1", width=200)
        self.v_box.add(game1_button.with_space_around(bottom=20))
        game2_button = GameButton2(text="Game 2", width=200)
        self.v_box.add(game2_button.with_space_around(bottom=20))
        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
    # Creates the background color and the viewport
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BEIGE)

        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        # this draws the text that welcomes the user and the manager which holds the buttons
    def on_draw(self):
        self.clear()
        arcade.draw_text("Welcome to our Educational Typing Game", self.window.width / 2, self.window.height / 2 + 100, arcade.color.BLACK, font_size=30, anchor_x="center")
        self.manager.draw()
   
       
        
# This class is supposed to create a new view or a new window which will allow our menu to launch a new operation or in our case game
class GameOne(arcade.View):
    def __init__(self):
        super().__init__()
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLUE)

        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(center_x= self.window.width / 2, center_y= self.window.height / 2 - 110, width=300, height=100, color=(0, 0, 25))

# this class is the same as GameOne
class GameTwo(arcade.View):
    def __init__(self):
        super().__init__()
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.GREEN)

        arcade.set_viewport(0, self.window.width, 0, self.window.height)
    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(center_x= self.window.width / 2, center_y= self.window.height / 2 - 110, width=300, height=100, color=(0, 55, 0))
# This instantiates the window and calls the first view which is the menu view
def main():
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    start_view = MainMenu()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
