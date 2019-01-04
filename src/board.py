# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import bokeh as bk
import bokeh.plotting as bkpt
import bokeh.models as bkmd
from copy import deepcopy
# from f_string import f
from typing import Dict

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

hole_style = {'line_width': 2,
              'line_color': 'black',
              'fill_color': 'white',
              'fill_alpha': 0.0}

seed_style = {'line_color': 'black',
              'fill_color': 'black'}

seed_text_style = {'text_align': 'center',
                   'text_baseline': 'middle',
                   'text_font_style': 'bold',
                   'text_font_size': '1.0em'}

seed_coords = {1: [(0.0, 0.0)],
               2: [(0.08, 0), (-0.08, 0)],
               3: [(0.08, -0.02), (-0.08, -0.02), (0.0, 0.1)],
               4: [(0.08, 0.08), (0.08, -0.08), (-0.08, 0.08), (-0.08, -0.08)],
               5: [(0.1, 0.1), (0.1, -0.1), (-0.1, 0.1), (-0.1, -0.1), (0.0, 0.0)],
               6: [(0.12, 0.08), (0.12, -0.08), (0.0, 0.08), (0.0, -0.08), (-0.12, 0.08), (-0.12, -0.08)],
               7: [(0.12, 0.08), (0.12, -0.08), (0.0, 0.13), (0.0, 0.0), (0.0, -0.13), (-0.12, 0.08), (-0.12, -0.08)],
               8: [(0.12, 0.13), (0.12, 0.0), (0.12, -0.13), (0.0, 0.08), (0.0, -0.08), (-0.12, 0.13), (-0.12, 0.0),
                   (-0.12, -0.13)],
               9: [(0.13, 0.13), (0.13, 0.0), (0.13, -0.13), (0.0, 0.13), (0.0, 0.0), (0.0, -0.13), (-0.13, 0.13),
                   (-0.13, 0.0), (-0.13, -0.13)]}

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class SemiBoard:
    """

    """
    def __init__(self, front_letter, back_letter):
        self.opponent = None
        self.front = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 6, '6': 2, '7': 2, '8': 0}
        self.front_letter = front_letter
        self.back = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
        self.back_letter = back_letter


class Board:
    """

    """
    def __init__(self):
        self.south = SemiBoard('A', 'B')
        self.north = SemiBoard('a', 'b')
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

class BoardPic:
    """

    """
    def __init__(self, board):
        self.board = deepcopy(board)
        self.img = None
        self.fig_south = bkpt.figure(plot_width=400, plot_height=120,
                                     tools='', toolbar_location=None,
                                     x_range=list(self.board.south.front),
                                     y_range=[self.board.south.back_letter, self.board.south.front_letter])

        self.fig_south.add_layout(bkmd.CategoricalAxis(), 'right')
        self.fig_south.min_border_top = 0
        self.fig_south.grid.visible = False

        self.fig_north = bkpt.figure(plot_width=400, plot_height=120,
                                     tools='', toolbar_location=None,
                                     x_range=list(self.board.north.front)[::-1],
                                     y_range=[self.board.north.front_letter, self.board.north.back_letter])
        self.fig_north.above = self.fig_north.below
        self.fig_north.below = []
        self.fig_north.add_layout(bkmd.CategoricalAxis(), 'right')
        self.fig_north.min_border_bottom = 0
        self.fig_north.grid.visible = False

        self.seed_glyphs = {}

        for (sb, fig) in [(self.board.south, self.fig_south), (self.board.north, self.fig_north)]:
            square = [sb.front_letter, '5']
            circles = [[row, col] for row in [sb.back_letter, sb.front_letter] for col in list(sb.front)
                       if not [row, col] == square]
            fig.circle(x=[x for [y, x] in circles], y=[y for [y, x] in circles], radius=0.45, **hole_style)
            fig.rect(x=[square[1]], y=[square[0]], width=0.90, height=0.90, **hole_style)
            for row, row_letter in [(sb.front, sb.front_letter), (sb.back, sb.back_letter)]:
                for x in list(row):
                    self.seed_glyphs[(row_letter, x)] = self.draw_seeds(fig, row_letter, x, row[x])

    def update_board(self, new_board):
        for (new_sb, old_sb, fig) in [(new_board.south, self.board.south, self.fig_south),
                                      (new_board.north, self.board.north, self.fig_north)]:
            for new_row, old_row, row_letter in [(new_sb.front, old_sb.front, old_sb.front_letter),
                                                 (new_sb.back, old_sb.back, old_sb.back_letter)]:
                for x in list(old_row):
                    if not (old_row[x] == new_row[x]):
                        for glyph in self.seed_glyphs[(row_letter, x)]:
                            fig.renderers.remove(glyph)
                        self.seed_glyphs[(row_letter, x)] = self.draw_seeds(fig, row_letter, x, new_row[x])

        self.board = deepcopy(new_board)

    @staticmethod
    def draw_seeds(fig, row, col, number):

        def dot(x_d, y_d):
            return fig.circle(x=bk.transform.dodge('x', x_d, range=fig.x_range),
                              y=bk.transform.dodge('y', y_d, range=fig.y_range),
                              source=bkmd.ColumnDataSource({'y': [row], 'x': [col]}),
                              radius=0.05, **seed_style)

        if number == 0:
            return []
        elif number <= 9:
            return [dot(x_d, y_d) for (x_d, y_d) in seed_coords[number]]
        else:
            return [fig.text(x='x', y='y', text='text',
                             source=bkmd.ColumnDataSource({'y': [row], 'x': [col], 'text': [f'{number}']}),
                             **seed_text_style)]

    def plot(self):
        self.img = bkpt.show(bk.layouts.column(self.fig_north, self.fig_south), notebook_handle=True)

    def update_pic(self):
        if not self.img:
            self.plot()
        else:
            try:
                bk.io.push_notebook(self.img)
            except ConnectionError:
                pass

    def update(self, board):
        self.update_board(board)
        self.update_pic()

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

        nb = self.pos2str(self.board.north.back)
        nf = self.pos2str(self.board.north.front)
        sf = self.pos2str(self.board.south.front)
        sb = self.pos2str(self.board.south.back)

        return(parser(nb, nf, sf, sb))



