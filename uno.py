import json, os
from random import shuffle, choice
from plot import plot_game

LOG_FILE = "data/game_log.json"
CARD_DATA = "data/deck.json"
START_CARDS = 7
BOT_NAMES = ["bot_Fernandez", "bot_Javier", "bot_Vato", "bot_Loco"]
ACTION_CARDS = ["skip", "reverse", "draw_2"]
WILD_CARDS = ["wild", "wild_draw_4"]

def clear_log(filename: str = LOG_FILE):
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

def load_card_data(file: str = CARD_DATA) -> dict:
    """Loads cards from json file(CARD_DATA)"""
    with open(file, "r") as f:
        data = json.load(f)
    return data

def get_colors() -> list:
    """Loads the color variants from json file(CARD_DATA)"""
    data = load_card_data()
    return data['colors']

def get_player_number() -> int:
        is_number = False
        while not is_number:
            try:
                player_count = int(input("How many players are gonna play? "))
                if player_count > 0 and player_count < 5:
                    is_number = True
                else: print("Number has to be greater than 0 and maximum 4")
            except:
                print("You need to enter a valid number to continue.")
        return player_count


class Card:
    def __init__(self, color: str, type: str|int):
        self.color = color
        self.type = type

    def __str__(self):
        return f"{self.color}({self.type})"
    
    def __repr__(self):
        return f"Card({self.color}, {self.type})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return False
        return self.color == other.color and self.type == other.type
            
    def __mul__(self, n):
        """Returns multiple pieces of a card"""
        return [Card(self.color, self.type) for _ in range(n)]
    
    def can_place_on(self, other: "Card") -> bool:
        """Tells if the card can be placed on another card"""
        if self.color == other.color or self.type == other.type:
            return True
        if self.type in WILD_CARDS:
            return True
        return False

    def set_color(self, color: str) -> None:
        if color not in get_colors(): raise ValueError("Invalid color")
        if self.type not in WILD_CARDS: raise ValueError("Can't set the color of this card")
        self.color = color
    


class Pack:
    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)
    
    def __str__(self):
        return f"{self.cards}"

    def make_pack(self) -> None:
        """Makes a pack from cards"""
        data = load_card_data()
        colors = data["colors"]
        number_cards = data["number_cards"]
        action_cards = data["action_cards"]
        wild_cards = data["wild_cards"]
        for color in colors:
            for number, count in number_cards.items():        
                self.cards.extend(Card(color, number) * count)
            for action_card in action_cards['types']:
                self.cards.extend(Card(color, action_card) * action_cards['count'])
        for type, count in wild_cards.items():
            self.cards.extend(Card(type, type) * count)

    def make_shuffled_pack(self) -> None:
        """Makes a new pack which is shuffled."""
        self.make_pack()
        shuffle(self.cards)
    
    def get_starter_card(self) -> Card:
        """Returns:
            Card:
                a starter card that is not action card on wild card.
        """
        starter = Card("", "")
        for i in range(len(self.cards)-1, 1, -1):
            try:
                int(self.cards[i].type)
                starter = self.cards.pop(i)
                break
            except ValueError:
                continue
        return starter

    def pull_card(self) -> Card:
        "Returns the last card in the pack."
        return self.cards.pop(0)

class Player:
    def __init__(self, name: str, is_bot: bool = False):
        """"
        Args:
            name: this will be user for the player during the game
            is_bot: tells if the player is going to be a bot-player or not
        """
        self.name = name
        self.deck: list = []
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
        self.deck.remove(card)
    
    def has_card_to_place_on(self, other: Card) -> bool:
        """Tells if the player has any card to place on 'other' card"""
        for card in self.deck:
            if card.can_place_on(other):
                return True
        return False
    
    def get_most_occurring_color(self) -> list:
        """Returns the color which occurs the most often in the player's deck. Used for bot players."""
        colors = {}
        color_palette = get_colors()
        for color in color_palette:
            colors[color] = 0
        for card in self.deck:
            if card.color not in ["wild", "wild_draw_4"]:
                colors[card.color] += 1
        sorted_colors = sorted(colors.items(), key=lambda item: item[1], reverse=True)
        return sorted_colors[0][0]
    

class Game:
    def __init__(self, ui: "Ui"):
        """initializes the game
        Args:
            pack: makes shuffled pack
            round: shows the rounds in the game, it starts with 0 because of the logging
            playernow: returns the index of the player that is in turn
            clockwise: game starts in clockwise, but it can change
            players: list of players who are playing
            last_card: shows the last placed card, starter card in the beginning
        """
        self.ui = ui
        self.pack = Pack()
        self.pack.make_shuffled_pack()
        self.round = 0
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
            f"Round: {self.round+1}, "
            f"in turn: {self.players[self.playernow]}, "
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
        player_info = {player.name: len(player) for player in self.players}
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}
        for name, card_count in player_info.items():
            if name not in data:
                data[name] = []
            data[name].append(card_count)
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        plot_game()

    def is_name_free(self, name: str) -> bool:
        """Checks if the player name is in use or not.
        Args:
            name: A name that will be used
        Returns:
        True: 
         if the choosen name is not added to the game yet.
        False: 
         if the choosen name is already used in the game.
        """
        taken_names = [player.name for player in self.players]
        if name in taken_names:
            return False
        return True

    def add_player(self, name: str) -> None:
        """Adds player to the game, and gives 7 card to the player's deck"""
        if self.is_name_free(name):
            player = Player(name)
            self.players.append(player)
            self.give_starting_deck(player)
        else:
            raise ValueError("Name is already in use.")

    def add_bot(self, name: str = choice(BOT_NAMES)) -> None:
        """Adds a bot to the game
        Args:
            name: gets a random name from the given bot names list
        """
        while not self.is_name_free(name):
            name = choice(BOT_NAMES)
        bot_player = Player(name, True)
        self.players.append(bot_player)
        self.give_starting_deck(bot_player)

    
    def give_starting_deck(self, player: Player, piece=START_CARDS):
        """Gives the starting card for the given player"""
        for _ in range(piece):
            card = self.pack.pull_card()
            player.add_card(card)

    def get_starter_player(self) -> int:
        """Return a random index of a player who will start the game"""
        interval = self.get_player_count()
        numbers = [i for i in range(interval)]
        return choice(numbers)
    
    def rotate_player_list(self, shift_by: int) -> list:
        """Shift the player list to get the starter player in the first place. Needed for the round counter to work properly.
        Args:
            shift_by: The number of the shifts in the players list.
            player_list: A copy of the players list
        Returns: rotated list of the players in game.
        """
        player_list = self.players[:]
        if shift_by-1 > len(player_list):
            shift_by = len(player_list)
        for _ in range(shift_by):
            for i in range(len(player_list)-1):
                temp = player_list[i]
                player_list[i] = player_list[i+1]
                player_list[i+1] = temp
        return player_list

    def pull_card(self, player: Player) -> None:
        """Pulls a card for the player from the pack"""
        card = self.pack.pull_card()
        player.add_card(card)
        self.ui.print_pull_card(player)
        

    def match_type(self, card: Card, player: Player) -> None:
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
                self.clockwise = not self.clockwise
                if self.get_player_count() == 2:
                    self.skip = True
            case "wild":
                if player.is_bot:
                    color = player.get_most_occurring_color()
                    card.set_color(color)
                else:
                    color = self.ui.ask_color(card)
                    card.set_color(color)
            case "wild_draw_4":
                if player.is_bot:
                    color = player.get_most_occurring_color()
                    card.set_color(color)
                else:
                    color = self.ui.ask_color(card)
                    card.set_color(color)
                self.to_pull = 4

    def drop_card_by_idx(self, player: Player, card_idx) -> None:
        """Drops a card by index in the player's deck
            Args:
                player:
                    A player who drops the card.
                card_idx:
                    The index of the choosen card in the players deck.
        """
        self.match_type(player.deck[card_idx], player)
        dropped_card = player.deck.pop(card_idx)
        self.last_card = dropped_card
        self.ui.print_drop_card(player, dropped_card)

    def bot_choose_card_to_drop(self, name: Player) -> int:
        """Bot card selection method
        Args:
            name:
                Name of the bot player that has to drop a card.
        Returns:
            The index of selected card that will be dropped.
        """
        good_cards: dict = {
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
                        except Exception as e: raise ValueError("Something went wrong.", e)
        if good_cards['number']:
            return next(iter(good_cards['number']))
        if good_cards['action']:
            return next(iter(good_cards['action']))
        else:
             return next(iter(good_cards['wild']))


    def turn(self, player: Player) -> None:
        """Prints the turn info, checks if the player is bot or not, pulls or drops a card.
        Args:
            player: if player is bot check if it can place any card, if can't pull a card. If tha player is not a bot, the prints the deck, and get action
        """
        self.ui.print_turn_info(player)
        if player.is_bot:        
            if player.has_card_to_place_on(self.last_card):
                idx = self.bot_choose_card_to_drop(player)
                self.drop_card_by_idx(player, idx)
            else:
                self.pull_card(player)
        else:
            self.ui.print_deck(player)
            self.ui.next_move(player)
            
    def next_player(self) -> None:
        """Changes current player to the next in line and manages round count"""
        player_count = self.get_player_count()
        if self.clockwise:
            if self.playernow + 1 <= player_count - 1:
                self.playernow += 1
            else:
                self.playernow = 0
                self.round += 1
                self.export_game_info()
        else:
            if self.playernow - 1 < 0:
                self.playernow = player_count - 1
                self.round += 1
                self.export_game_info()
            else:
                self.playernow -= 1

    def players_with_card(self) -> int:
        """Returns the number of the players with card"""
        player_count = 0
        for player in self.players:
            if len(player.deck) > 0:
                player_count += 1
        return player_count

    def run(self, player_count, only_bots: bool = False) -> None:
        """This is the game logic.
        Args:
            player_count: The number of the players that will be playing
            only_bots: Default value is false, if set to true only bot players will be added to the game.
        """
        if only_bots:
            for i in range(player_count):
                self.add_bot()
        else:
            self.ui.add_players(player_count)
        starter_player_idx = self.get_starter_player()
        self.players = self.rotate_player_list(starter_player_idx)
        self.export_game_info()
        while self.players_with_card() > 1:
            if not self.pack:
                self.pack.make_shuffled_pack()
            current_player = self.players[self.playernow]
            if current_player not in self.winners:
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
                #TODO ui-ba áthelyezni a játékmenet kiíratást
                print(self)
                self.turn(current_player)
                self.next_player()
                if len(current_player.deck) == 0:
                    self.winners.append(current_player)
                    self.ui.print_ran_out_of_cards(current_player)
            else:
                self.next_player()
        self.export_game_info()
        self.ui.print_winners()

        
class Ui:
    def __init__(self, human: int, bots: bool = False):
        self.game = Game(self)
        self.game.run(human, bots)

    def add_players(self, count) -> None:
        """You have to enter every players name, if only one will be added, then automatically adds a bot to the game.
        Args:
            count:
                how many players will be added to the game
        """
        for i in range(count):
            print(f"{i+1}; player")
            is_free = False
            while not is_free:
                name = input("name: ")
                if self.game.is_name_free(name):
                    self.game.add_player(name)
                    is_free = True
                else:
                    print(f"Name '{name}' is already in use, please select another one.")
        if len(self.game.players) < 2:
            for _ in range(3):
                self.game.add_bot()

    def print_deck(self, player: Player):
        for idx, card in enumerate(player.deck):
                print(f"{idx+1}. {card}")

    def print_turn_info(self, player: Player) -> str:
        """
        Args:
            player: the player that is in turn
        Returns:
            str: a string with a little decoration to give some feedback of the gameplay.
        """
        decor = 3*len(player)*'-'
        print(f"In turn:\n{decor}\n{' '*len(player)}{player}\n{decor}")

    def next_move(self, player: Player) -> None:
        """Drops or pulls a card for the player depends on user input"""
        valid_number = False
        while not valid_number:
            try:
                number = int(input("Number: "))
                if number == 0:
                    self.game.pull_card(player)
                    valid_number = True
                else:
                    if player.has_card_to_place_on(self.game.last_card):
                        if player.deck[number-1].can_place_on(self.game.last_card):
                            self.game.drop_card_by_idx(player, number-1)
                            valid_number = True
                        else:
                            print(f"Can't place {player.deck[number-1]} on {self.game.last_card}")
                    else:
                        print(f"{player.name} does't have any card to drop on {self.game.last_card}. Please pull a card(0).")
            except Exception as e:
                print(f"Please enter a valid number between 0-{len(player.deck)}")

    def ask_color(self, card: Card) -> str:
        """Asks a color for wild or wild_draw_4 card"""
        valid_color = False
        if card.type in WILD_CARDS:
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
        return colors[selected_idx-1]
    
    def print_pull_card(self, player: Player):
        print(f"-- {player.name} -- pulled a card --")
    
    def print_drop_card(self, player: Player, card: Card):
        print(f"-- {player.name} - dropped: {card} --")


    def print_ran_out_of_cards(self, player: Player):
        print(player, "ran out of cards, left the game.")
    
    def print_winners(self):
        print(f"\nGame over. Winner(s): {[f"{idx+1}: {player}" for idx, player in enumerate(self.game.winners)]}")


if __name__ == "__main__":
    count = get_player_number()
    ui = Ui(count)