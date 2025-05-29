from uno import *

def test_making_card():
    cards = []
    cards.append(Card("red", "skip"))
    cards.append(Card("blue", 2))
    cards.append(Card("yellow", "draw_two"))
    cards.append(Card("wild", "wild"))
    for card in cards:
        print(card)
        if card.type == "wild":
            card.ask_color()
            print(card)
        
def test_card_can_place_on_other():
    print("red(8) on red(wild)")
    print(Card("red", 8).can_place_on(Card("red", "wild")))
    print("blue(8) on green(8)")
    print(Card("blue", 8).can_place_on(Card("green", 8)))
    print("wild_draw_4(wild_draw_4) on blue(6)")
    print(Card("wild_draw_4", "wild_draw_4").can_place_on(Card("blue", "6")))
    print("blue(6) on wild_draw_4(wild_draw_4)")
    print(Card("blue", "6").can_place_on(Card("wild_draw_4", "wild_draw_4")))

test_making_card()
test_card_can_place_on_other()


def test_make_pack():
    pack = Pack()
    pack.make_pack()
    print(pack)

def test_make_shuffled_pack():
    pack = Pack()
    pack.make_shuffled_pack()
    print(pack) 
    print(f"Size of pack: {len(pack)}")
    print(f"Starter card: {pack.get_starter_card()}")

test_make_pack()
print("--------------")
test_make_shuffled_pack()