from typing import Dict, List
from itertools import zip_longest
from enum import Enum

class Custom_SemiBoard:
    """

    """
    def __init__(self, front_letter, back_letter, front_position, back_position):
        self.opponent = None
        self.front = front_position
        self.front_letter = front_letter
        self.back = back_position
        self.back_letter = back_letter

class Custom_Board:
    """

    """
    def __init__(self, sf_position, sb_position, nf_position, nb_position):
        self.south = Custom_SemiBoard('A', 'B', sf_position, sb_position)
        self.north = Custom_SemiBoard('a', 'b', nf_position, nb_position)
        self.south.opponent = self.north
        self.north.opponent = self.south

    @staticmethod
    def pos2str(pos: Dict) -> str:
        dicto = {'1': 'D', '2': 'V'}

        pos = [str(i) for i in pos.values()]
        pos = [dicto[i[0]] + i[1] if len(i) == 2 else i for i in pos]
        return ''.join(pos)

    @property
    def FEN(self):

        def parser(*args):
            return '/'.join(args)

        nb = self.pos2str(self.north.back)
        nf = self.pos2str(self.north.front)
        sf = self.pos2str(self.south.front)
        sb = self.pos2str(self.south.back)

        return(parser(nb, nf, sf, sb))

class Decenas(Enum):
    """

    """
    D = '1'
    V = '2'

def r_str2list(subfen:str) -> List:
    """

    :param subfen:
    :return:
    """
    restricted = ['D', 'V']
    listo = []
    while subfen:
        head, *tail = subfen
        if head in restricted:
            body, *tail = tail
            listo.append(Decenas[head].value + body)
        else:
            listo.append(head)
        subfen = tail
    return listo

def str2list(subfen: str) -> List:
    """

    :param subfen:
    :return:
    """
    restricted = ['D', 'V', None]
    listo = [Decenas[i].value + j if i in restricted else j for i, j in zip_longest(subfen, subfen[1:]) if j not in restricted]
    if len(listo) == 8:
        return listo
    else:
        return [subfen[0]] + listo

def str2pos(subfen: str) -> Dict:
    """

    :param subfen:
    :return:
    """
    if len(subfen) == 8:
        return {str(idx):int(i) for idx, i in enumerate(subfen, start=1)}
    else:
        listo = str2list(subfen)
        return {str(idx):int(i) for idx, i in enumerate(listo, start=1)}

def board_position(fen: str) -> Custom_Board:
    """
    Visualize mancala position given a string notation

    :param fen: string
    :return:
    """
    nb, nf, sf, sb = [str2pos(i) for i in fen.split('/')]

    return Custom_Board(sf, sb, nf, nb)




