"""
Programming 1 project by: Örkényi Vilmos

Summary: UNO card game.
"""
from uno import Game


if __name__ == "__main__":
    game = Game()
    game.add_player("test")
    game.run()
