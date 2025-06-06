import matplotlib.pyplot as plt
import numpy as np
import os, json

def load_log(filename: str):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    return data

def plot_game(filename: str):
    data = load_log(filename)
    rounds = [round for round in data]
    players = []
    player_cards = []
    for el in data.values():
        for name, cards in el.items():
            players.append(name)
            player_cards.append(cards)

    player_count = len(players)//len(rounds)
    player1 = player_cards[::2]
    player2 = player_cards[1::2]
    player3 = player_cards[1::3]
    #player4 = player_cards[::4]

    names = [name for name in players]
    x = np.arange(len(rounds))
    width = 0.2
    fig, ax = plt.subplots(layout='constrained')
    ax.bar(x-0.1, player1, width)
    ax.bar(x+0.1, player2, width)
    if player_count == 3:
        ax.bar(x+0.3, player3, width)
    ax.set_xlabel("Rounds")
    ax.set_ylabel("Cards")
    ax.set_title("Cards by round")
    #ax.grid()
    fig.legend(names)
    fig.savefig("stat.jpg")

if __name__ == "__main__":
    LOG_FILE = "game_log.json"
    load_log(LOG_FILE)
    plot_game(LOG_FILE)
