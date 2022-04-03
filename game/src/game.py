# from game import constants
import os
import random
import shelve
from enum import Enum
import math
import constants
import time
import arcade
from src.car import Car

import src.word


class GameStates(Enum):
    GAME_OVER = 0
    RUNNING = 1

class Game(arcade.Window):
    def __init__(self, width, height, words, word_rows_count=20):
        super().__init__(width, height, constants.SCREEN_TITLE)

        self.screen_width = width
        self.screen_height = height
        self.background_img = constants.BACKGROUND_IMG
        self.foreground_img = constants.FOREGROUND_IMG
        self.background_texture = arcade.load_texture(self.background_img)
        self.foreground = arcade.Sprite(self.foreground_img, 0.5, center_x=800, center_y=40)
        self.foreground2 = arcade.Sprite(self.foreground_img, 0.5, center_x=2400, center_y=40)
        self.foreground_list = arcade.SpriteList()

        self.words = words
        self.word_rows_count = word_rows_count
        
        self.high_score = int()
        self.start = float() # Keeps track of the time when you start typing out a word
        self.end= float() # Keeps track of the time that you finish typing the word
        self.avgwpm = list()
        self.score = int()
        self.number_words = int()
        self.lives = int()
        self.errors = int()
        self.wpm = float()
        self.state = None
        self.focus_word = None # The word that is currently being focused on / typed

        self.word_list = set()
        self.car = Car()


    def setup(self):
        """ Set up the game and initialize the variables. """
        self.score = 0
        self.lives = 300
        self.number_words=3
        self.errors = 0
        self.wpm = 0
        self.state = GameStates.RUNNING
        self.focus_word = None
        self.start = time.time()
        self.word_list = set()

        for _ in range(self.number_words):
            self.create_word()

        self.foreground_list.append(self.foreground)
        self.foreground_list.append(self.foreground2)
    
    def draw_game_over(self):
        self.calculateWPM()
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

        arcade.draw_text("Press Q to quit",
                         self.screen_width / 2, (self.screen_height / 2) - 35,
                         arcade.color.WHITE, 24, anchor_x="center", anchor_y="center"
                         )

        arcade.draw_text(f"Current score : {self.score}", 15, 15,arcade.color.WHITE, 14,)
        arcade.draw_text(f"Words Per Minute : {round(self.wpm)}", 15, 35,arcade.color.WHITE, 14,)
        arcade.draw_text(f"High score : {self.high_score}", self.screen_width - 15, 15, arcade.color.WHITE, 14,
             anchor_x="right", anchor_y="baseline")
        arcade.draw_text(f"Errors: {self.errors}", 15, self.screen_height - 30, arcade.color.WHITE, 14)
    
        self.car.draw()

    def draw_game(self):

        arcade.draw_texture_rectangle(300, 300, 800, 600, self.background_texture)
        for fg in self.foreground_list:
            fg.draw()

        for word in self.word_list:
            word.draw()
        arcade.draw_text(f"Score : {self.score}", 15, 90, arcade.color.BLACK, 14)
        arcade.draw_text(f"Lives : {self.lives}", self.screen_width - 15, 90,  arcade.color.BLACK, 14, anchor_x="right", anchor_y="baseline")
        arcade.draw_text(f"Errors: {self.errors}", 15, self.screen_height - 30, arcade.color.BLACK, 14)

        self.car.draw()
        

    def on_draw(self):
        arcade.start_render()
        
        if self.state == GameStates.RUNNING:
            self.draw_game()
            
            self.end = time.time() 
        else:
            self.draw_game_over()

    def calculateWPM(self):
        #Calculate the words per minute by taking the score or total number of words and then dividing it by the total time it took to type the word and then subtracting any errors
        wordsperminute = (self.score / (self.end - self.start))
        self.avgwpm.append(wordsperminute)
        # To try and average all the words per minute I store each value in a list and divide it by how many times you have completed a word
        
        self.wpm = wordsperminute
    
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
            for fg in self.foreground_list:
                fg.center_x -= 2
                if fg.center_x < -800:
                    fg.center_x = 2400
            
            for word in self.word_list:
                
                if word.x < 0:
                    if self.focus_word == word:
                        self.focus_word = None

                    self.lives -= 1
                    self.car.update_image()
                    
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
                    word.x -= 5
                
            
            if self.lives <= 0:
                
                path = os.path.join(os.path.expanduser("~"), ".racer-type")
                score_file = shelve.open(path)  
                new_high_score = int()
                if score_file.get("high_score") == None:
                    new_high_score = self.score
                else:
                    new_high_score = max([self.score, score_file["high_score"]])
                score_file["high_score"] = new_high_score
                self.high_score = new_high_score
                self.end = time.time()
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

    def on_key_press(self, key):
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
            
            self.create_word()