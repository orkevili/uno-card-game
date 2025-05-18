"""An example source module."""


def greeting(name: str, formal: bool = True) -> str:
    """Returns a greeting message
    
    Args:
        name: The full name of the greeted person: "Firstname [Middlename] Lastname".
        formal: Sets the formality of the greeting.
    
    Returns:
        A single-line sentence.
    
    >>> greeting("Ann")
    'Good day to you, Ann!'
    >>> greeting("Bob", False)
    'Hi Bob!'
    """
    if formal:
        return f"Good day to you, {name}!"
    else:
        return f"Hi {name.split()[0]}!"
