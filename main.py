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

def get_player_count():
    is_number = False
    while not is_number:
        player_count = input("How many players are gonna play? ")
        try:
            player_count = int(player_count)
            if player_count > 0 and player_count < 5:
                is_number = True
            else: print("Number has to be greater than 0 and maximum 4")
        except:
            print("You need to enter a valid number to continue.")
    return player_count

def start_game():
    clear_log()
    print("-- UNO Game --")
    count = get_player_count()
    game = Game()
    game.run(count, only_bots)

    
if __name__ == "__main__":
    only_bots = False
    if len(argv) > 1:
        if argv[1] == "bot":
            print("Starting the game with only bot players.")
            only_bots = True
    start_game()
    