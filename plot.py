import matplotlib.pyplot as plt
import os, json
import numpy as np

LOG_FILE = "data/game_log.json"

def load_log(filename: str = LOG_FILE):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    return data

def get_players_stat(filename: str = LOG_FILE):
    data = load_log(filename)
    players = [el for el in data]
    player_cards = [data[el] for el in data]
    rounds = len(player_cards[0])
    
    return rounds, players, player_cards

def plot_game():
    rounds, players, player_cards = get_players_stat() 
    player_count = len(players)
    player1 = player_cards[::player_count]
    player2 = player_cards[1::player_count]
    player3 = player_cards[2::player_count]
    player4 = player_cards[3::player_count]

    fig, ax = plt.subplots(layout='constrained')
    step = 1
    if rounds > 26:
        step += 1
    if rounds > 50:
        step += 1
    x = np.arange(0, rounds, step)
    y = np.arange(0, max(player_cards)+1, 1)
    plt.xticks(x)
    plt.yticks(y)
    ax.plot(player1)
    ax.plot(player2)
    if player_count > 2:
        ax.plot(player3)
    if player_count > 3:
        ax.plot(player4)
    ax.set_xlabel("Rounds")
    ax.set_ylabel("Cards")
    ax.set_title("Cards by round")
    ax.grid()
    fig.legend(players)
    fig.savefig("img/game_stats.jpg")
    plt.close()

if __name__ == "__main__":
    print(get_players_stat())
    plot_game()
