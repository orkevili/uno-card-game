import matplotlib.pyplot as plt
import os, json
import numpy as np

LOG_FILE = "data/game_log.json"

def load_log(filename: str = LOG_FILE):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    return data

def plot_game(filename: str = LOG_FILE):
    data = load_log(filename)
    players = data.keys()
    max_card_numer = max(max(hand) for hand in data.values())
    rounds = len(next(iter(data.values())))

    fig, ax = plt.subplots(layout='constrained')
    step = 1
    if rounds > 26:
        step += 1
    if rounds > 50:
        step += 1
    x = np.arange(0, rounds, step)
    y = np.arange(0, max_card_numer+1, 1)
    ax.set_xticks(x)
    ax.set_yticks(y)
    for player, hand in data.items():
        ax.plot(hand)
    ax.set_xlabel("Rounds")
    ax.set_ylabel("Cards")
    ax.set_title("Cards by round")
    ax.grid()
    fig.legend(players)
    fig.savefig("img/game_stats.jpg")

if __name__ == "__main__":
    plot_game()
