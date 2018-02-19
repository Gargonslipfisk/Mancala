import regex
from itertools import cycle

def get_opposite(shimo):
    number = list(reversed(range(1, 9)))
    if shimo[0].isupper():
        return shimo[0].lower() + str(number[int(shimo[1]) - 1])
    else:
        return shimo[0].upper() + str(number[int(shimo[1]) - 1])

def check_direction(direction, side, number):
    sf = [side[0] + '.front' + '[' + '"' + str(i) + '"' + ']' for i in list(range(1, 9))]
    sb = [side[0] + '.back' + '[' + '"' + str(i) + '"' + ']' for i in list(reversed(range(1, 9)))]
    if direction is '>' and side[1] is 'front':
        listo = sf + sb
        pos = side[0] + '.' + side[1] + '[' + '"' + number + '"' + ']'
        cut_point = listo.index(pos) + 1
        listo = listo[cut_point:] + listo[0:cut_point]
        return cycle(listo)
    elif direction is '<' and side[1] is 'front':
        listo = list(reversed(sf)) + list(reversed(sb))
        pos = side[0] + '.' + side[1] + '[' + '"' + number + '"' + ']'
        cut_point = listo.index(pos) + 1
        listo = listo[cut_point:] + listo[0:cut_point]
        return cycle(listo)
    elif direction is '>' and side[1] is 'back':
        listo = list(reversed(sf)) + list(reversed(sb))
        pos = side[0] + '.' + side[1] + '[' + '"' + number + '"' + ']'
        cut_point = listo.index(pos) + 1
        listo = listo[cut_point:] + listo[0:cut_point]
        return cycle(listo)
    elif direction is '<' and side[1] is 'back':
        listo = sf + sb
        pos = side[0] + '.' + side[1] + '[' + '"' + number + '"' + ']'
        cut_point = listo.index(pos) + 1
        listo = listo[cut_point:] + listo[0:cut_point]
        return cycle(listo)