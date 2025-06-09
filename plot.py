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
    player1 = player_cards[::player_count]
    player2 = player_cards[1::player_count]
    player3 = player_cards[2::player_count]
    player4 = player_cards[3::player_count]

    fig, ax = plt.subplots(layout='tight')
    ax.plot(player1)
    ax.plot(player2)
    if player_count == 3:
        ax.plot(player3)
    if player_count == 4:
        ax.plot(player3)
        ax.plot(player4)

    ax.set_xlabel("Rounds")
    ax.set_ylabel("Cards")
    ax.set_title("Cards by round")
    ax.grid()
    fig.legend(players)
    fig.savefig("stat.jpg")

if __name__ == "__main__":
    LOG_FILE = "game_log.json"
    load_log(LOG_FILE)
    plot_game(LOG_FILE)
