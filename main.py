# -*- coding: utf-8 -*-

from src.board import *
from src.read_game import *
from src.parse_move import *

b = Board()
bp = BoardPic(b)
bp.plot()

game = Game('data/game2.pgn')


for i in range(len(game.game['moves']) * 2):
    print(game.current_move + 1)
    if game.current_move + 1 == 9:
        print("hola")
    parse_move(board=b, move=game.next_move, status=game.check_status)
    bp.update(b)