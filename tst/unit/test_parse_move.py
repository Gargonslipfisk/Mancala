from src.parse_move import *
from src.board_position_notation import *
# from src.utils.singleton import SingletonMetaclass
import pytest

# class Single_Board(Board, metaclass=SingletonMetaclass):
#     pass

FIRST = '00000000/00006220/00006031/00000001'

subfen_test_parser_move = [
    ('00000000/00006220/00006220/00000000', 'A6>*', 'namua', FIRST),
]

@pytest.mark.parametrize('initial_position, move, status, expected_position', subfen_test_parser_move)
def test_parse_move(initial_position, move, status, expected_position):
    b = board_position(initial_position)
    parse_move(board=b, move=move, status=status)
    assert expected_position == b.FEN

# def tearDown(self):
#     # Remove the config object and clear it from the singleton cache
#     del self.cfg
#     SingletonMetaclass.clear_instances()