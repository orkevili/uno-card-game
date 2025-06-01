import json
from random import shuffle

CARD_DATA = "deck.json"
START_CARDS = 7

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
    def __init__(self, name):
        """Need a name that will be used for the player during the game."""
        self.name = name
        self.deck = []
    
    def __str__(self):
        return f"{self.name}"
    
    def __repr__(self):
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
    
    def get_colors_in_deck(self):
        """Returns what colors are in the playes deck"""
        colors = {}
        color_palette = get_colors()
        for color in color_palette:
            colors[color] = 0
        for card in self.deck:
            if card.color not in ["wild", "wild_draw_4"]:
                colors[card.color] += 1
        sorted_colors = sorted(colors.items(), key=lambda item: item[1], reverse=True)
        return sorted_colors
    
    def get_color_with_most_cards(self):
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

    def __str__(self):
        return(
            f"----------------------------------\n"
            f"Round: {self.round}, "
            f"in turn: {self.players[self.playernow] if self.players else None}, "
            f"remaining cards in pack: {len(self.pack)}\n"
            f"last card: {self.last_card}\n"
            f"To pull: {self.to_pull}, Skip: {self.skip}, Clockwise: {self.clockwise}\n"
            f"----------------------------------"
        )
    
    def __repr__(self):
        return f"Game({self.pack}, Round: {self.round}\nClockwise: {self.clockwise}, \n{self.players}, \nPlayer now: {self.playernow}, \nLast card: {self.last_card}\n To pull: {self.to_pull}, Skip: {self.skip})"


    def add_player(self, name: str) -> None:
        """Adds player to the game, and gives 7 card to the player's deck"""
        self.players.append(Player(name))
        self.give_starting_deck()
    
    def give_starting_deck(self, piece=START_CARDS):
        for _ in range(piece):
            card = self.pack.cards.pop(0)
            self.players[-1].add_card(card)
    
    def pull_card(self, name: Player) -> None:
        """Pulls a card for the player from the pack"""
        card = self.pack.cards.pop(0)
        name.add_card(card)
        print(f"--{name.name}-- pulled: {card} --")

    def match_type(self, card: Card, name: Player = None):
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
            case "wild":
                if name:
                    color = name.get_color_with_most_cards()
                    card.color = color
                else:
                    card.ask_color()
            case "wild_draw_4":
                if name:
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
                    self.match_type(card)
                    good_card = True
                    dropped_card = name.deck.pop(card_idx)
                    self.last_card = dropped_card
                    print(f"--{name.name}-- dropped: {dropped_card} --")
                else: print(f"Can't place {card} on {self.last_card}")
            except Exception as e:
                print("Invalid card number.", e)

    def add_bot(self) -> None:
        """Adds a bot to the game if only one player going to play"""
        self.players.append(Player("bot"))
        self.give_starting_deck()

    def drop_card_bot(self, name: Player, card_idx) -> None:
        dropped_card = name.deck.pop(card_idx)
        self.match_type(dropped_card, name)
        self.last_card = dropped_card
        print(f"--{name.name}-- dropped: {dropped_card} --")

    def turn(self, name: Player) -> None:
        """Gives a player a choice to pull or drop a card"""
        if name.name != "bot":        
            print(f"--{name}--")
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
                    print(f"Can not place any card on {self.last_card}, pull a card.")
                    self.pull_card(name)
        else:
            if name.has_card_to_place_on(self.last_card):
                hand = name.deck
                print(hand)
                for i in range(len(name.deck) - 1):
                    if hand[i].can_place_on(self.last_card):
                        if hand[i].type in ["wild", "wild_draw_4"]:
                            hand[i].color = name.get_colors_in_deck()[0][0]
                        self.drop_card_bot(name, i)
                        break
            else:
                print("A bot nem tud kártyát rakni, húz egyet")
                self.pull_card(name)

    def next_player(self) -> None:
        """Changes current player to the next in line and manages round count"""
        player_count = len(self.players)
        if self.playernow + 1 <= player_count - 1:
            self.playernow += 1
        else:
            self.playernow = 0
            self.round += 1

    def players_with_card(self) -> int:
        """Returns a number of players with card"""
        player_count = 0
        for player in self.players:
            if len(player.deck) > 0:
                player_count += 1
        return player_count

    def run(self):
        """Game process this is where the magic happens."""
        is_number = False
        while not is_number:
            player_count = input("How many players are gonna play? ")
            try:
                player_count = int(player_count)
                if player_count > 0:
                    is_number = True
                else: print("Number has to be greater than 0")
            except:
                print("You need to enter a valid number to continue.")

        for i in range(player_count):
            print(f"{i+1}; player")
            name = input("name: ")
            self.add_player(Player(name))
        if len(self.players) == 1:
            self.add_bot()

        while len(self.pack) > 0 and self.players_with_card() > 1:
            print(self)
            if self.to_pull > 0:
                for i in range(self.to_pull):
                    self.pull_card(self.players[self.playernow])
                self.to_pull = 0
                self.next_player()
            if self.skip:
                self.skip = False
                self.next_player()
            else:
                self.turn(self.players[self.playernow])
                self.next_player()
        winners = [p.name for p in self.players if not p.deck]
        print(f"Game over. Winner is: {winners[0] if winners else None}")

game = Game()
game.run()