# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import regex

class Game:
    """

    """
    def __init__(self, path):
        self.game = self.read_game(path)
        self.current_player = False
        self.current_move = 0

    @staticmethod
    def read_game(path):
        """

        :param path:
        :return:
        """
        f = open(path, 'r', encoding='UTF-8')

        game = {}
        game['metadata'] = {}
        game['moves'] = []
        line = f.readline()

        while line.startswith("["):
            line_splitted = line.split()
            key = regex.sub('\[', '', line_splitted[0])
            value = regex.sub('\]', '', line_splitted[1])
            game['metadata'][key] = eval(value)
            line = f.readline()

        while line.isspace():
            line = f.readline()

        while line:
            try:
                line_splitted = line.split()
                # number = regex.findall('\d+', line_splitted[0])
                game['moves'].append((line_splitted[1], line_splitted[2]))
                line = f.readline()
            except Exception:
                break

        return game

    @property
    def next_move(self):
        out = self.game['moves'][self.current_move][self.current_player]
        self.current_player = not self.current_player
        if not self.current_player:
            self.current_move += 1
        return out

    @property
    def previous_move(self):
        self.current_player = not self.current_player
        if self.current_player:
            self.current_move -= 1
        return self.game['moves'][self.current_move][self.current_player]

    @property
    # TODO
    def check_status(self):
        return 'namua' if self.current_move < 22 else 'mtaji'
