# from game import constants
import os
from pickle import FALSE
import random
import shelve
from enum import Enum
import math
import constants
import time
import arcade

import src.word




class GameStates(Enum):
    GAME_OVER = 0
    RUNNING = 1

class Game(arcade.Window):
    def __init__(self, width, height, words, word_rows_count=20):
        super().__init__(width, height, constants.SCREEN_TITLE)
        arcade.set_background_color((5, 2, 27))

        self.screen_width = width
        self.screen_height = height
        self.words = words
        self.word_rows_count = word_rows_count

        self.high_score = int()
        self.start = float() # Keeps track of the time when you start typing out a word
        self.end= float() # Keeps track of the time that you finish typing the word
        self.avgwpm = list()
        self.score = int()
        self.lives = int()
        self.errors = int()
        self.wpm = float()
        self.state = None
        self.focus_word = None # The word that is currently being focused on / typed

        self.word_list = set()

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.score = 0
        self.lives = 3
        self.errors = 0
        self.wpm = 0
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
        arcade.draw_text(f"Words Per Minute : {round(self.wpm)}", 15, 35,arcade.color.WHITE, 14,)
        arcade.draw_text(f"High score : {self.high_score}", self.screen_width - 15, 15, arcade.color.WHITE, 14,
             anchor_x="right", anchor_y="baseline")
        arcade.draw_text(f"Errors: {self.errors}", 15, self.screen_height - 30, arcade.color.WHITE, 14)
    
    def draw_game(self):
        
        for word in self.word_list:
            word.draw()
        arcade.draw_text(f"Score : {self.score}", 15, 15, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives : {self.lives}", self.screen_width - 15, 15,  arcade.color.WHITE, 14, anchor_x="right", anchor_y="baseline")
        arcade.draw_text(f"Errors: {self.errors}", 15, self.screen_height - 30, arcade.color.WHITE, 14)
        arcade.draw_text(f"Words per Minute: {round(self.wpm)}", 15, self.screen_height -50, arcade.color.WHITE, 14)
    def on_draw(self):
        arcade.start_render()

        if self.state == GameStates.RUNNING:
            self.draw_game()
        else:
            self.draw_game_over()

    def calculateWPM(self):
        #Calculate the words per minute by taking the score or total number of words and then dividing it by the total time it took to type the word and then subtracting any errors
        wordsperminute = (self.score / (self.end - self.start)) - self.errors
        self.avgwpm.append(wordsperminute)
        # To try and average all the words per minute I store each value in a list and divide it by how many times you have completed a word
        for i in self.avgwpm:
            self.wpm += i
        self.wpm = self.wpm / len(self.avgwpm)

        
    
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
                
                if word.x < 0:
                    if self.focus_word == word:
                        self.focus_word = None

                    self.lives -= 1

                    self.word_list.discard(word)
                    self.create_word()

                """These if statements increase word speed based on score"""
                if self.score >= 180:
                    word.x -= 4
                elif self.score >= 150:
                    word.x -= 3.5
                elif self.score >= 120:
                    word.x -= 3
                elif self.score >= 90:
                    word.x -= 2.5
                elif self.score >= 60:
                    word.x -= 2
                elif self.score >= 30:
                    word.x -= 1.5
                elif self.score >= 0:
                    word.x -= 1
                

                    
                
            
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
                arcade.exit()

        if self.focus_word is None:
            self.focus_word = self._get_leftmost_word_starting_with(chr(key))
            if self.focus_word is not None:
                self.focus_word.in_focus = True
                self.focus_word.attack()
                self.start = time.time()
            elif not self.focus_word and not key == 32:
                self.errors += 1
            
        else:
            if self.focus_word.word[0].lower() == chr(key):
                self.focus_word.attack()
            else: self.errors += 1

        if self.focus_word.word == "":
            self.word_list.discard(self.focus_word)
            self.focus_word = None
            self.score += 1
            self.end = time.time()
            self.create_word()
            self.calculateWPM()