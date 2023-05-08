import pytest

#from your_module import compute_sum
from main import compute_sum

def test_compute_sum_with_positive_integer():
    assert compute_sum(5) == 15

def test_compute_sum_with_zero():
    with pytest.raises(ValueError) as e:
        compute_sum(0)
    assert str(e.value) == "n must be a positive integer."

def test_compute_sum_with_negative_integer():
    with pytest.raises(ValueError) as e:
        compute_sum(-5)
    assert str(e.value) == "n must be a positive integer."
