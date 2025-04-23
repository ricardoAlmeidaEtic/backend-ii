import pytest
from challenge_factorial import factorial

@pytest.mark.parametrize("n, result", [
    (0, 1),
    (1, 1),
    (5, 120),
    (7, 5040)
])
def test_factorial(n, result):
    assert factorial(n) == result
