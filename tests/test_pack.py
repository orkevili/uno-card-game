from uno import Pack

pack = Pack()

def test_pack():
    pack.make_pack()
    assert len(pack.cards) > 0

    pack.make_shuffled_pack()
    assert len(pack.cards) > 0

def test_get_starter_card():
    pack.make_pack()
    assert pack.get_starter_card()

    pack.make_shuffled_pack()
    assert pack.get_starter_card()