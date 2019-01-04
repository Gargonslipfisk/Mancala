import regex
from itertools import cycle

def get_opposite(shimo):
    number = list(reversed(range(1, 9)))
    if shimo[0].isupper():
        return shimo[0].lower() + str(number[int(shimo[1]) - 1])
    else:
        return shimo[0].upper() + str(number[int(shimo[1]) - 1])

def check_direction(direction, side, number, status):
    sf = [side[0] + '.front' + '[' + '"' + str(i) + '"' + ']' for i in list(range(1, 9))]
    sb = [side[0] + '.back' + '[' + '"' + str(i) + '"' + ']' for i in list(reversed(range(1, 9)))]
    if direction is '>' and side[1] is 'front':
        # lista flat del recorrido que haria sobre el tablero
        listo = sf + sb
        # genera la posición para buscar su localización en la lista
        pos = side[0] + '.' + side[1] + '[' + '"' + number + '"' + ']'
        # PATCH almacen
        if number == '5' and status is not 'combo':
            listo = list(reversed(sf)) + list(reversed(sb))
        else:
            # el punto de corte (donde inicia el movimiento) es el hueco siguiente a pos
            cut_point = listo.index(pos) + 1
            # genera un nuevo listo asociado al punto de corte
            listo = listo[cut_point:] + listo[0:cut_point]
        # retorna un ciclo en atención a que puede dar varias vueltas (si tiene suficientes semillas)
        return cycle(listo)
    elif direction is '<' and side[1] is 'front':
        listo = list(reversed(sf)) + list(reversed(sb))
        pos = side[0] + '.' + side[1] + '[' + '"' + number + '"' + ']'
        # PATCH almacen
        if number == '5' and status is not 'combo':
            listo = sf + sb
        else:
            cut_point = listo.index(pos) + 1
            listo = listo[cut_point:] + listo[0:cut_point]
        return cycle(listo)
    elif direction is '>' and side[1] is 'back':
        listo = sf + sb
        pos = side[0] + '.' + side[1] + '[' + '"' + number + '"' + ']'
        cut_point = listo.index(pos) + 1
        listo = listo[cut_point:] + listo[0:cut_point]
        return cycle(listo)
    elif direction is '<' and side[1] is 'back':
        listo = list(reversed(sf)) + list(reversed(sb))
        pos = side[0] + '.' + side[1] + '[' + '"' + number + '"' + ']'
        cut_point = listo.index(pos) + 1
        listo = listo[cut_point:] + listo[0:cut_point]
        return cycle(listo)

def parse_move(board, move, status):
    pos = move[0] + move[1]
    direction = move[2]
    final = move[-1]
    # si namua entonces es que está añadiendo una semilla del banquillo
    # count = 1 if status is 'namua' else 0
    if status == 'namua':
        count = 1
    # PATCH
    elif status == 'combo':
        if move[0] is 'A':
            count = board.south.front[move[1]]
        elif move[0] is 'B':
            count = board.south.back[move[1]]
        elif move[0] is 'a':
            count = board.north.front[move[1]]
        else:
            count = board.north.back[move[1]]
    else:
        count = 0
    if move[0] is 'A':
        # cuenta las semillas en la casilla 7 (sabiendo que está en A)
        if move[1] == '5':
            if move[-1] == '+':
                count += board.south.front[move[1]]
                board.south.front[move[1]] = 0
            else:
                board.south.front[move[1]] = board.south.front[move[1]] + count
                count = 0
        else:
            if move[-1] == '*':
                count += board.south.front[move[1]]
                # actualiza el numero de semillas en la casilla a 0
                board.south.front[move[1]] = 0
            elif move[-1] == '+':
                count += board.south.front[move[1]]
                board.south.front[move[1]] = 0
            else:
                board.south.front[move[1]] = board.south.front[move[1]] + count
                count = 0
        # donde estamos (se pasara a check_direction)
        side = ('south', 'front')
        # obtiene la casilla opuesta para comprobar si se captura
        opposite = get_opposite(pos)
        # capture cuenta el numero de semillas en la casilla opuesta
        capture = board.north.front[opposite[1]]
        # actualiza la cuenta añadiendo las capturadas
        count = count + capture
        # actualiza el numero de semillas en la casilla opuesta a 0 (haya o no)
        board.north.front[opposite[1]] = 0
    elif move[0] is 'B':
        count += board.south.back[move[1]]
        board.south.back[move[1]] = 0
        side = ('south', 'back')
    elif move[0] is 'a':
        if move[1] == '5':
            if move[-1] == '+':
                count += board.north.front[move[1]]
                board.north.front[move[1]] = 0
            else:
                board.north.front[move[1]] = board.north.front[move[1]] + count
                count = 0
        else:
            if move[-1] == '*':
                count += board.north.front[move[1]]
                board.north.front[move[1]] = 0
            elif move[-1] == '+':
                count += board.north.front[move[1]]
                board.north.front[move[1]] = 0
            else:
                # PATCH
                if status == 'combo':
                    board.north.front[move[1]] = 0
                else:
                    board.north.front[move[1]] = board.north.front[move[1]] + count
                    count = 0
        side = ('north', 'front')
        opposite = get_opposite(pos)
        capture = board.south.front[opposite[1]]
        count = count + capture
        board.south.front[opposite[1]] = 0
    else:
        count = board.north.back[move[1]]
        board.north.back[move[1]] = 0
        side = ('north', 'back')
    # retorna un ciclo con todas las casillas en que se movería desde el punto de corte
    dir = check_direction(move[2], side, move[1], status)
    for i in range(count):
        # actual = posición
        actual = next(dir)
        to_eval = 'board.' + actual + ' = ' + 'board.' + actual + '+ 1'
        exec(to_eval)
    # en caso de que se combinen movimientos
    if eval('board.' + actual) > 1:
        # PATCH: si cae en almacén y no tiene +
        if actual[-3] == '5' and final is not '+':
            pass
        else:
            tmp = regex.split('[\.\[]', actual)
            if tmp[0] == 'south' and tmp[1] == 'front':
                move = 'A'
            elif tmp[0] == 'south' and tmp[1] == 'back':
                move = 'B'
            elif tmp[0] == 'north' and tmp[1] == 'front':
                move= 'a'
            elif tmp[0] == 'north' and tmp[1] == 'back':
                move = 'b'
            # PATCH
            if pos[1] == '5':
                if direction == '<':
                    direction = '>'
                else:
                    direction = '<'
            move = move + regex.findall('\d', tmp[2])[0] + direction + final if final == '+' else move + regex.findall('\d', tmp[2])[0] + direction
            parse_move(board, move, 'combo')