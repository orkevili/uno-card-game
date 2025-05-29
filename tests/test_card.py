from uno import Card

red_draw_2 = Card("red", "draw_2")
red_8 = Card("red", "8")
blue_8 = Card("blue", "8")
wild = Card("wild", "wild")


def test_cards():
    assert red_draw_2
    assert red_8
    assert blue_8
    assert wild

def test_multiply_card():
    assert red_8 * 2 == [red_8, red_8]

def test_can_place_on():
    assert red_draw_2.can_place_on(red_8)
    assert red_8.can_place_on(blue_8)
    assert wild.can_place_on(blue_8)

