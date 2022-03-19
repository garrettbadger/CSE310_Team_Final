import os
from pickle import FALSE
import random
import shelve
from enum import Enum
import math

import arcade

import src.word


class GameStates(Enum):
    GAME_OVER = 0
    RUNNING = 1

class Game(arcade.Window):
    def __init__(self, width, height, words, word_rows_count=20):
        super().__init__(width, height, title="Space Typer")
        arcade.set_background_color((5, 2, 27))

        self.screen_width = width
        self.screen_height = height
        self.words = words
        self.word_rows_count = word_rows_count

        self.high_score = int()

        self.score = int()
        self.lives = int()
        self.state = None
        self.focus_word = None # The word that is currently being focused on / typed

        self.word_list = set()
        self.star_list = set()

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.score = 0
        self.lives = 3
        self.state = GameStates.RUNNING
        self.focus_word = None
        
        self.word_list = set()

        for _ in range(3):
            self.create_word()

            
    
    def draw_game_over(self):
        arcade.draw_text("Game Over",
            self.screen_width / 2, (self.screen_height / 2) + 68,
            arcade.color.WHITE, 54,
            anchor_x="center", anchor_y="center"
        )

        arcade.draw_text("Press SPACE to restart",
            self.screen_width / 2, (self.screen_height / 2),
            arcade.color.WHITE, 24,
            anchor_x="center", anchor_y="center"
        )

        arcade.draw_text("q to quit",
                         self.screen_width / 2, (self.screen_height / 2) - 35,
                         arcade.color.WHITE, 24, anchor_x="center", anchor_y="center"
                         )

        arcade.draw_text(f"Current score : {self.score}", 15, 15,arcade.color.WHITE, 14,)
        arcade.draw_text(f"High score : {self.high_score}", self.screen_width - 15, 15, arcade.color.WHITE, 14,
             anchor_x="right", anchor_y="baseline"
        )
    
    def draw_game(self):
        for word in self.word_list:
            word.draw()
        
        arcade.draw_text(f"Score : {self.score}", 15, 15, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives : {self.lives}", self.screen_width - 15, 15,  arcade.color.WHITE, 14, anchor_x="right", anchor_y="baseline")

    def on_draw(self):
        arcade.start_render()

        if self.state == GameStates.RUNNING:
            self.draw_game()
        else:
            self.draw_game_over()
    
    def create_word(self):
        # Find a row that's currently not occupied by another word.
        row = int()
        occupied_rows = set()
        while True:
            row = random.randrange(self.word_rows_count)
            for word in self.word_list:
                occupied_rows.add(word.row)
            if row not in occupied_rows:
                break
        
        # Find a word that starts with a character that is not the first
        # character of another word.
        occupied_chars = set()
        for word in self.word_list:
            occupied_chars.add(word.word[0])
        rand_word = str()
        while True:
            rand_word = random.choice(self.words)
            if rand_word[0] not in occupied_chars:
                break
        
        self.word_list.add(src.word.Word(rand_word, row, self.screen_width, self.screen_height, self.word_rows_count))


    
    def update(self, delta_time):
        """ Movement and game logic """

        if self.state == GameStates.RUNNING:
            for word in self.word_list:
                word.x -= 50*delta_time
                if word.x < 0:
                    if self.focus_word == word:
                        self.focus_word = None

                    self.lives -= 1

                    self.word_list.discard(word)
                    self.create_word()
            
            if self.lives <= 0:
                path = os.path.join(os.path.expanduser("~"), ".space-typer")
                score_file = shelve.open(path)
                new_high_score = int()
                if score_file.get("high_score") == None:
                    new_high_score = self.score
                else:
                    new_high_score = max([self.score, score_file["high_score"]])
                score_file["high_score"] = new_high_score
                self.high_score = new_high_score

                self.state = GameStates.GAME_OVER

    def _get_leftmost_word_starting_with(self, character):
        words_starting_with_given_character = []
        for word in self.word_list:
            if word.word[0].lower() == character:
                words_starting_with_given_character.append(word)
        if len(words_starting_with_given_character) == 0:
            return None
        else:
            leftmost_word = min(words_starting_with_given_character, key=lambda word: word.x)
            return leftmost_word

    def on_key_press(self, key, modifiers):
        if key > 127:
            return

        if self.state == GameStates.GAME_OVER:
            if key == 32:
                self.setup()
                self.state = GameStates.RUNNING
            elif key == ord("q"):
                raise SystemExit

        if self.focus_word is None:
            self.focus_word = self._get_leftmost_word_starting_with(chr(key))
            if self.focus_word is not None:
                self.focus_word.in_focus = True
                self.focus_word.attack()
        else:
            if self.focus_word.word[0].lower() == chr(key):
                self.focus_word.attack()

        if self.focus_word.word == "":
            self.word_list.discard(self.focus_word)
            self.focus_word = None
            self.score += 1
            self.create_word()