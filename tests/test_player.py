from uno import Player, Card

blue_7 = Card("blue", 7)
green_3 = Card("green", 3)
yellow_7 = Card("yellow", 7)

def test_add_card():
    test = Player("test")
    test.add_card(blue_7)
    assert len(test.deck) == 1
    test.add_card(green_3)
    assert len(test.deck) == 2

def test_remove_card():
    test = Player("test")
    test.add_card(blue_7)
    test.add_card(green_3)
    test.remove_card(blue_7)
    assert len(test.deck) == 1

def test_has_card_to_place_on():
    test = Player("test")
    test.add_card(blue_7)
    test.add_card(green_3)
    assert test.has_card_to_place_on(yellow_7)