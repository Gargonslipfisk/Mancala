from src.board_position_notation import *
import pytest

ONE_D_SUBFEN = {'1': 0, '2': 2, '3': 1, '4': 3, '5': 4, '6': 14, '7': 9, '8': 2}
TWO_D_SUBFEN = {'1': 0, '2': 2, '3': 1, '4': 3, '5': 4, '6': 14, '7': 9, '8': 12}
BEGINNING_D_SUBFEN = {'1': 14, '2': 2, '3': 1, '4': 3, '5': 4, '6': 0, '7': 9, '8': 2}

subfen_test_cases = [
    ('02134D492', ONE_D_SUBFEN),
    ('02134D49D2', TWO_D_SUBFEN),
    ('D42134092', BEGINNING_D_SUBFEN)
]

@pytest.mark.parametrize('input, expected', subfen_test_cases)
def test_str2pos(input, expected):
    actual = str2pos(input)
    assert expected == actual

# '00001203/00009130/11007000/02020203'
# '03120002/00000000/02134D492/13220275'