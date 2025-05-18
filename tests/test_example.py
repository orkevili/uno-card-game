from example import greeting


def test_formal_greeting():
    name = "John Doe"
    result = greeting(name)
    assert name in result
    assert "good day" in result.lower()
    assert result[-1] in "!."


def test_informal_greeting():
    fname = "John"
    lname = "Doe"
    result = greeting(f"{fname} {lname}", formal=False)
    assert fname in result
    assert result.lower()[:2] == "hi"
    assert result[-1] in "!."
