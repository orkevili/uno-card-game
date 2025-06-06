import json, os
from random import shuffle
from plot import plot_game

LOG_FILE = "game_log.json"
CARD_DATA = "deck.json"
START_CARDS = 7
BOT_NAME = "bot_Bob"

def load_card_data(file: str = CARD_DATA):
    """Load cards from json file(CARD_DATA)"""
    with open(file, "r") as f:
        data = json.load(f)
    return data

def get_colors() -> list:
    """Loads the color variants from json file(CARD_DATA)"""
    data = load_card_data()
    return data['colors']


class Card:
    def __init__(self, color: str, type: str|int):
        self.color = color
        self.type = type

    def __str__(self):
        return f"{self.color}({self.type})"
    
    def __repr__(self):
        return f"Card({self.color}, {self.type})"
    
    def __eq__(self, other: "Card"):
        if self.color == other.color and self.type == other.type:
            return True
        return False
    
    def __mul__(self, n):
        """Returns multiple pieces of a card"""
        return [Card(self.color, self.type) for _ in range(n)]


    def ask_color(self) -> None:
        """Asks a color for wild or wild_draw_4 card"""
        valid_color = False
        if self.type in ["wild", "wild_draw_4"]:
            colors = get_colors()
            print("Which color you want?")
            for idx, color in enumerate(colors):
                print(f"{idx+1}; {color}")
            while not valid_color:
                try:
                    selected_idx = int(input("Number: "))
                except ValueError:
                    print("Enter a valid number.")
                    continue
                if selected_idx > 0 and selected_idx <= len(colors):
                    valid_color = True
                else:
                    print(selected_idx)
                    print("Invalid number, try again.")
        self.color = colors[selected_idx-1]

    def can_place_on(self, other: "Card") -> bool:
        """Tells if the card can be placed on another card"""
        if self.color == other.color or self.type == other.type:
            return True
        if self.type in ["wild", "wild_draw_4"]:
            return True
        return False


class Pack:
    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)
    
    def __str__(self):
        return f"{self.cards}"

    def make_pack(self) -> None:
        """Makes a pack from cards
        Args:
            cards
        Returns:
            List of cards that makes a pack.
        """
        data = load_card_data()
        colors = data.get("colors")
        number_cards = data.get("number_cards")
        action_cards = data.get("action_cards")
        wild_cards = data.get("wild_cards")
        for color in colors:
            for number, count in number_cards.items():        
                self.cards.extend(Card(color, number) * count)
            for action_card in action_cards.get('types'):
                self.cards.extend(Card(color, action_card) * action_cards.get('count'))
        for type, count in wild_cards.items():
            self.cards.extend(Card(type, type) * count)

    def make_shuffled_pack(self) -> None:
        """Makes a new pack which is shuffled."""
        self.make_pack()
        return shuffle(self.cards)
    
    def get_starter_card(self) -> Card:
        """Returns a starter card that is not action card on wild card."""
        for i in range(len(self.cards)-1, 1, -1):
            try:
                int(self.cards[i].type)
                return self.cards.pop(i)
            except ValueError:
                continue


class Player:
    def __init__(self, name: str, is_bot: bool = False):
        """Need a name that will be used for the player during the game, is_bot tells if the player is going to be a bot player or not."""
        self.name = name
        self.deck = []
        self.is_bot = is_bot

    def __len__(self) -> int:
        """Returns how much cards the player has."""
        return len(self.deck)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    def __repr__(self) -> str:
        return f"Player({self.name})"
    
    def add_card(self, card: Card) -> None:
        """Adds a card to the players deck."""
        self.deck.append(card)
    
    def remove_card(self, card: Card) -> None:
        """Removes a card from the players deck."""
        for i in range(len(self.deck)-1):
            if self.deck[i] == card:
                self.deck.pop(i)
    
    def has_card_to_place_on(self, other: Card) -> bool:
        """Tells if the player has any card to place on another card"""
        for card in self.deck:
            if card.can_place_on(other):
                return True
        return False
    
    def get_colors_in_deck(self) -> list:
        """Returns a list with colors which are in the players deck"""
        colors = {}
        color_palette = get_colors()
        for color in color_palette:
            colors[color] = 0
        for card in self.deck:
            if card.color not in ["wild", "wild_draw_4"]:
                colors[card.color] += 1
        sorted_colors = sorted(colors.items(), key=lambda item: item[1], reverse=True)
        return sorted_colors
    
    def get_color_with_most_cards(self) -> str:
        """Returns the most often occurring color in the players deck"""
        return self.get_colors_in_deck()[0][0]

    

class Game:
    def __init__(self):
        """initializes the game
        Args:
            pack: makes a pack, then shuffles it
            round: shows the rounds in the game, it starts with 1
            playernow: returns the index of the player that is in turn
            clockwise: game starts in clockwise, but it can change
            players: list of players who are playing
            last_card: shows the last placed card, starter card in the beginning
        """
        self.pack = Pack()
        self.pack.make_shuffled_pack()
        self.round = 1
        self.players = []
        self.playernow = 0
        self.clockwise = True
        self.to_pull = 0
        self.skip = False
        self.last_card = self.pack.get_starter_card()
        self.winners = []

    def __str__(self):
        return(
            f"----------------------------------\n"
            f"Round: {self.round}, "
            f"in turn: {self.players[self.playernow] if self.players else None}, "
            f"remaining cards in pack: {len(self.pack)}\n"
            f"To pull: {self.to_pull}, Skip: {self.skip}, Clockwise: {self.clockwise}\n"
            f"last card: {self.last_card}\n"
            f"----------------------------------"
        )
    
    def __repr__(self):
        return f"Game({self.pack}, Round: {self.round}\nClockwise: {self.clockwise}, \n{self.players}, \nPlayer now: {self.playernow}, \nLast card: {self.last_card}\n To pull: {self.to_pull}, Skip: {self.skip})"

    def get_player_count(self):
        """Returns how many players are in game"""
        return len(self.players)
    
    def export_game_info(self, filename: str = LOG_FILE):
        player_info = {self.round: {str(el.name): len(el) for el in self.players}}
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}
        data.update(player_info)
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def add_player(self, name: str) -> None:
        """Adds player to the game, and gives 7 card to the player's deck"""
        self.players.append(Player(name))
        self.give_starting_deck()

    def add_bot(self) -> None:
        """Adds a bot to the game"""
        bot_player = Player(BOT_NAME, True)
        self.players.append(bot_player)
        self.give_starting_deck()

    def add_players(self, count) -> None:
        """You have to enter every players name, if only one will be added, then automatically adds a bot to the game.
        Args:
            count:
                how many players will be added to the game
        """
        for i in range(count):
            print(f"{i+1}; player")
            name = input("name: ")
            self.add_player(Player(name))
        if len(self.players) < 2:
            self.add_bot()
    
    def give_starting_deck(self, piece=START_CARDS):
        for _ in range(piece):
            card = self.pack.cards.pop(0)
            self.players[-1].add_card(card)
    
    def pull_card(self, name: Player) -> None:
        """Pulls a card for the player from the pack"""
        card = self.pack.cards.pop(0)
        name.add_card(card)
        print(f"-- {name.name} -- pulled: {card} --")

    def match_type(self, card: Card, name: Player) -> None:
        """Checks the type of the card and makes the required changes in the variables of the class.
            Args:
                card:
                    the card what the player drops
                name:
                    needs the player to check if is it a bot, so it can automatically select a color for wild cards
        """
        match(card.type):
            case "draw_2":
                self.to_pull = 2
            case "skip":
                self.skip = True
            case "reverse":
                if self.clockwise:
                    self.clockwise = False
                else:
                    self.clockwise = True
                if self.get_player_count() == 2:
                    self.next_player()
            case "wild":
                if name.is_bot:
                    color = name.get_color_with_most_cards()
                    card.color = color
                else:
                    card.ask_color()
            case "wild_draw_4":
                if name.is_bot:
                    color = name.get_color_with_most_cards()
                    card.color = color
                else:
                    card.ask_color()
                self.to_pull = 4
    
    def drop_card(self, name: Player) -> None:
        """Drops the choosen card from the player"""
        good_card = False
        while not good_card:
            try:
                card_idx = int(input("Which you want to drop? ")) - 1
                card = name.deck[card_idx]
                if card.can_place_on(self.last_card):
                    self.match_type(card, name)
                    good_card = True
                    dropped_card = name.deck.pop(card_idx)
                    self.last_card = dropped_card
                    print(f"-- {name.name} - dropped: {dropped_card} --")
                else: print(f"Can't place {card} on {self.last_card}")
            except Exception as e:
                print("Invalid card number.", e)

    def drop_card_by_idx(self, name: Player, card_idx) -> None:
        """Drops a card by index in the player's deck
            Args:
                name:
                    A player who drops the card.
                card_idx:
                    The index of the choosen card in the players deck.
        """
        dropped_card = name.deck.pop(card_idx)
        self.match_type(dropped_card, name)
        self.last_card = dropped_card
        print(f"-- {name.name} - dropped: {dropped_card} --")

    def bot_choose_card_to_drop(self, name: Player) -> int:
        """Returns one card's index in the player's deck to drop."""
        good_cards = {
            "number": {},
            "action": {},
            "wild": {}
        }
        for idx, card in enumerate(name.deck):
            if card.can_place_on(self.last_card):
                match(card.type):
                    case "skip"|"reverse"|"draw_2":
                        good_cards["action"][idx] = card
                    case "wild"|"wild_draw_4":
                        good_cards["wild"][idx] = card
                    case _:
                        try:
                            int(card.type)
                            good_cards["number"][idx] = card
                        except Exception as e:
                            print("Something went wrong.", e)
        if good_cards['number']:
            return next(iter(good_cards['number']))
        if good_cards['action']:
            return next(iter(good_cards['action']))
        else:
             return next(iter(good_cards['wild']))


    def turn(self, name: Player) -> None:
        """Gives a player a choice to pull or drop a card"""
        decor = 3*len(name)*'-'
        print(f"In turn:\n{decor}\n{' '*len(name)}{name}\n{decor}")
        if not name.is_bot:        
            for idx, card in enumerate(name.deck):
                print(f"{idx+1}. {card}")
            valid_command = False
            while not valid_command:
                action = input("pull or drop? ")
                if action in ["pull", "drop"]:
                    valid_command = True
                else:
                    print("Invalid command.")
            if action == "pull":
                self.pull_card(name)
            else:
                if name.has_card_to_place_on(self.last_card):
                    self.drop_card(name)    
                else:
                    print(f"Can't place any card on {self.last_card}, pull a card.\n")
                    self.pull_card(name)
        else:
            if name.has_card_to_place_on(self.last_card):
                idx = self.bot_choose_card_to_drop(name)
                self.drop_card_by_idx(name, idx)
            else:
                print(f"{name} can't place any card on {self.last_card}, pull one.")
                self.pull_card(name)

    def next_player(self) -> None:
        """Changes current player to the next in line and manages round count"""
        player_count = len(self.players)
        if self.clockwise:
            if self.playernow + 1 <= player_count - 1:
                self.playernow += 1
            else:
                self.playernow = 0
                self.round += 1
        else:
            if self.playernow - 1 < 0:
                self.playernow = player_count - 1
                self.round += 1
            else:
                self.playernow -= 1

    def players_with_card(self) -> int:
        """Returns a number of players with card"""
        player_count = 0
        for player in self.players:
            if len(player.deck) > 0:
                player_count += 1
        return player_count

    def run(self, player_count) -> None:
        """Game process this is where the magic happens."""
        self.add_players(player_count)

        while len(self.pack) > 0 and self.players_with_card() > 1:
            self.export_game_info()
            plot_game(LOG_FILE)
            current_player = self.players[self.playernow]
            print(self)
            if self.to_pull > 0:
                for i in range(self.to_pull):
                    self.pull_card(current_player)
                self.to_pull = 0
                self.next_player()
                continue
            if self.skip:
                self.skip = False
                self.next_player()
                continue
            self.turn(current_player)
            self.next_player()
            if len(current_player.deck) < 1:
                self.players.remove(current_player)
                self.winners.append(current_player)
                print(current_player, "ran out of cards, left the game.")

        print(f"\nGame over. Winner(s): {[f"{idx+1}: {player}" for idx, player in enumerate(self.winners)]}")


if __name__ == "__main__":
    count = int(input("player count: "))
    game = Game()
    game.run(count)