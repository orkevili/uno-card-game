import json
from random import shuffle

CARD_DATA = "deck.json"

def load_card_data(file: str):
    """Load cards from json file(CARD_DATA)"""
    with open(file, "r") as f:
        data = json.load(f)
    return data


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
    
    def get_colors(self) -> list:
        """Loads the color variants from json file(CARD_DATA)"""
        data = load_card_data(CARD_DATA)
        return data['colors']


    def ask_color(self):
        """Asks a color for wild or wild_draw_4 card"""
        valid_color = False
        if self.type in ["wild", "wild_draw_4"]:
            colors = self.get_colors()
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

    def make_pack(self):
        """Makes a pack from cards
        Args:
            cards
        Returns:
            List of cards that makes a pack.
        """
        data = load_card_data(CARD_DATA)
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
        return f"{self.name}: {self.deck}"
    
    def __repr__(self):
        return f"Player({self.name})"
    
    def add_card(self, card:Card) -> None:
        """Adds a card to the players deck."""
        pass
    
    def has_card_to_place_on(self, card: Card) -> bool:
        """Tells if the player has any card to place on another card"""
        pass

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
        self.playernow = 0
        self.clockwise = True
        self.players = []
        self.last_card = self.pack.get_starter_card()

    def __str__(self):
         pass

    def __repr__(self):
        pass

    def add_player(self, name: str) -> None:
       """Adds player to game"""
       pass
    
    def pull_card(self, name: Player) -> None:
        """Pulls a card for the player from the pack"""
        pass
    
    def drop_card(self, name: Player) -> None:
        """Drops the choosen card from the player"""
        pass
    
    def turn(self, name: Player) -> None:
        """Gives a player a choice to pull or drop a card"""
        pass

    def next_player(self) -> None:
       """Changes current player to the next in line"""
       pass

    def players_with_card(self) -> int:
       """Returns a number of players with card"""
       pass

    def run(self):
       """Game process this is where the magic happens."""
       pass
