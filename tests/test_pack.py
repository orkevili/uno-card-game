from uno import Pack, Card


def test_make_pack():
    pack = Pack()
    pack.make_pack()
    assert len(pack.cards) == 108

def test_make_shuffled_pack():
    pack = Pack()
    pack.make_shuffled_pack()
    assert len(pack.cards) == 108

def test_get_starter_card():
    pack = Pack()
    pack.make_pack()
    starter = pack.get_starter_card()
    assert isinstance(starter, Card)

    pack.make_shuffled_pack()
    shuffled_starter = pack.get_starter_card()
    assert isinstance(shuffled_starter, Card)