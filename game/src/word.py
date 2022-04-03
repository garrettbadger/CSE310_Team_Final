import arcade

class Word:
    def __init__(self, word, row, screen_width, screen_height, word_row_count):
        self.word = word
        self.row = row
        self.x = screen_width
        self.y = (int((screen_height - 100) / word_row_count) * row) +100
        self.in_focus = False

    def draw(self):
        arcade.draw_text(self.word, self.x, self.y,
            arcade.color.DODGER_BLUE if self.in_focus else arcade.color.BLACK,
        14)
    
    def attack(self):
        self.word = self.word[1:]