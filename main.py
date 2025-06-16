"""
Programming 1 project by: Örkényi Vilmos

Summary: UNO card game.
"""
import os
from sys import argv
from uno import *

def clear_log(filename: str = LOG_FILE):
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

def start_game():
    only_bots = False
    msg = ""
    if len(argv) > 1:
        if argv[1] == "bot":
            msg = "Starting the game with only bot players."
            only_bots = True
    clear_log()
    print("-- UNO Game --", msg)
    count = get_player_number()
    if only_bots and count < 2:
        raise ValueError("Need at least 2 players to start a game.")
    game = Game()
    game.run(count, only_bots)

    
if __name__ == "__main__":
    start_game()
    