"""
Programming 1 project by: Örkényi Vilmos

Summary: UNO card game.
"""
CARD_DATA = "deck.json"

class Card:
    def __init__(self, color: str, type: str|int):
        self.color = color
        self.type = type

    def __str__(self):
        return f"{self.color}({self.type})"
    
    def __repr__(self):
        return f"Card({self.color}, {self.type})"
    
    def __mul__(self, n):
        """Returns multiple pieces of a card"""
        return [Card(self.color, self.type) for _ in range(n)]
    
    def load_card_data(self, file: str):
        """Load cards from json file(CARD_DATA)"""
        pass

    def get_colors(self, file: str) -> list:
        """Loads the color variants from json file(CARD_DATA)"""
        pass

    def ask_color(self):
        """Asks a color for wild or wild_draw_4 card"""
        pass
    
    def can_place_on(self, other: "Card") -> bool:
        """Tells if the card can be placed on another card"""
        pass

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
        pass

    def shuffle_pack(self) -> "Pack":
        """Returns a shuffled pack."""
        pass

    def get_starter_card(self) -> Card:
        """Gives a starter card that is not action card on wild card.
        Returns:
            Card:
                A card to start the game with.
        """
        pass


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
        self.pack.shuffle_pack()
        self.round = 1
        self.playernow = 0
        self.clockwise = True
        self.players = []
        self.last_card = self.pack.get_starter_card()

    def __str__(self):
         pass

    def __repr__(self):
        pass

    def add_player(self, name: Player) -> None:
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



if __name__ == "__main__":
    game = Game()
    game.add_player("test")
    game.run()
