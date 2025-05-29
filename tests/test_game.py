from uno import Game, Player


def test_drop_card():
    pass

def test_next_player():
    game.add_player("test")
    game.add_player("test2")
    assert game.playernow == 0
    game.next_player()
    assert game.playernow == 1
    game.next_player()
    assert game.playernow == 0

def test_players_with_card():
    assert game.players_with_card() == 0
    game.add_player("test")
    assert game.players_with_card() == 1