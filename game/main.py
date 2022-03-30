import arcade
import argparse
import yaml
import constants
from src.game import Game

width=constants.SCREEN_WIDTH
height=constants.SCREEN_HEIGHT

DEFAULT_WORD_LIST = ("try","again", "sometime","please","we","will", "rock","you","hello", "giant", "panda", "bear", "dog", "thing", "small")


def main(width, height, words):
    game = Game(width, 
    height, words)
    game.setup()
    arcade.run()

def parse_word_list(word_list_filename):
    with open(word_list_filename, "r") as word_list_file:
        data = yaml.safe_load(word_list_file)
        return data["words"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start Type Racer game.")
    parser.add_argument("--screen-width", type=int, default=height, help="Width of screen in pixels")
    parser.add_argument("--screen-height", type=int, default=height, help="Height of screen in pixels")
    parser.add_argument("--word-list", type=str, default=None,
                        help="yaml file containing the words to use in the game" +
                        " (use a list of words with key 'words'); by default use built-in word list.")

    args = parser.parse_args()

    if args.word_list:
        words = parse_word_list(args.word_list)
    else:
        words = DEFAULT_WORD_LIST

    main(args.screen_width, args.screen_height, words)