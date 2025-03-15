import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def simple_matrix_2x2():
    return [
        [3, 1],
        [2, 4]
    ]

@pytest.fixture
def matrix_with_saddle_point():
    return [
        [4, 0, 6, 2],
        [3, 8, 4, 4],
        [1, 2, 5, 6]
    ]

@pytest.fixture
def matrix_without_pure_nash():
    return [
        [0, 1],
        [1, 0]
    ]

@pytest.fixture
def prisoners_dilemma():
    return [
        [-1, -3],
        [0, -2]
    ] 