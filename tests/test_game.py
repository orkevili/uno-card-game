from uno import Game, Player


def test_add_player():
    game = Game()
    game.add_player("test")
    assert len(game.players) == 1
    game.add_player("test2")
    assert len(game.players) == 2

def test_pull_card():
    """Game starts with 108 cards
    107 in the game start, because of the starter card
    adding a player, player starts with 7 cards so 100 left in pack.
    pulling a card for the player so 99 cards left in the pack.
    """
    game = Game()
    assert len(game.pack) == 107
    game.add_player("test")
    assert len(game.pack) == 100
    game.pull_card(Player("test"))
    assert len(game.pack) == 99

def test_next_player():
    game = Game()
    game.add_player("test")
    game.add_player("test2")
    assert game.playernow == 0
    game.next_player()
    assert game.playernow == 1
    game.next_player()
    assert game.playernow == 0

def test_players_with_card():
    game = Game()
    assert game.players_with_card() == 0
    game.add_player("test")
    assert game.players_with_card() == 1