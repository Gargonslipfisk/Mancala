# -*- coding: utf-8 -*-

from src.board import *
from src.read_game import *
from src.parse_move import *

b = Board()
bp = BoardPic(b)
bp.plot()

game = Game('data/game.pgn')

def parse_move(board, move, status):
    pos = move[0] + move[1]
    if move[0] is 'A':
        count = board.south.front[move[1]]
        board.south.front[move[1]] = 0
        side = ('south', 'front')
        opposite = get_opposite(pos)
        capture = board.north.front[opposite[1]]
        count = count + capture
        board.north.front[opposite[1]] = 0
    elif move[0] is 'B':
        count = board.south.back[move[1]]
        board.south.back[move[1]] = 0
        side = ('south', 'back')
    elif move[0] is 'a':
        count = board.north.front[move[1]]
        board.north.front[move[1]] = 0
        side = ('north', 'front')
        opposite = get_opposite(pos)
        capture = board.south.front[opposite[1]]
        count = count + capture
        board.south.front[opposite[1]]
    else:
        count = board.north.back[move[1]]
        board.north.back[move[1]] = 0
        side = ('north', 'back')
    if status is 'namua':
        count += 1
    dir = check_direction(move[2], side, move[1])
    for i in range(count):
        actual = next(dir)
        to_eval = 'global b;' + 'b.' + actual + ' = ' + 'b.' + actual + '+ 1'
        exec(to_eval, globals())
    if eval('board.' + actual) > 1:
        tmp = regex.split('[\.\[]', actual)
        if tmp[0] == 'south' and tmp[1] == 'front':
            move = 'A'
        elif tmp[0] == 'south' and tmp[1] == 'back':
            move = 'B'
        elif tmp[0] == 'north' and tmp[1] == 'front':
            move= 'a'
        elif tmp[0] == 'north' and tmp[1] == 'back':
            move = 'b'
        move = move + regex.findall('\d', tmp[2])[0]
        parse_move(board, move, status)

for i in range(len(game.game['moves']) * 2):
    parse_move(board=b, move=game.next_move, status=game.check_status)
    bp.update(b)