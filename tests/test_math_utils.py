import pytest
import numpy as np
from src.math_utils import descriptive_stats, moving_average, normalize, matrix_multiply


class TestDescriptiveStats:
    def test_basic(self):
        result = descriptive_stats([1, 2, 3, 4, 5])
        assert result["mean"] == pytest.approx(3.0)
        assert result["median"] == pytest.approx(3.0)
        assert result["std"] == pytest.approx(np.std([1, 2, 3, 4, 5]))

    def test_single_value(self):
        result = descriptive_stats([42])
        assert result["mean"] == 42.0
        assert result["median"] == 42.0
        assert result["std"] == 0.0

    def test_negative_values(self):
        result = descriptive_stats([-3, -1, 0, 1, 3])
        assert result["mean"] == pytest.approx(0.0)
        assert result["median"] == pytest.approx(0.0)


class TestMovingAverage:
    def test_window_of_one(self):
        data = [10, 20, 30]
        assert moving_average(data, 1) == pytest.approx([10, 20, 30])

    def test_full_window(self):
        data = [2, 4, 6]
        assert moving_average(data, 3) == pytest.approx([4.0])

    def test_typical(self):
        data = [1, 3, 5, 7, 9]
        result = moving_average(data, 3)
        assert result == pytest.approx([3.0, 5.0, 7.0])

    def test_invalid_window(self):
        with pytest.raises(ValueError):
            moving_average([1, 2], 0)
        with pytest.raises(ValueError):
            moving_average([1, 2], 5)


class TestNormalize:
    def test_basic(self):
        result = normalize([0, 5, 10])
        assert result == pytest.approx([0.0, 0.5, 1.0])

    def test_already_normalized(self):
        result = normalize([0, 0.5, 1])
        assert result == pytest.approx([0.0, 0.5, 1.0])

    def test_constant_values(self):
        result = normalize([7, 7, 7])
        assert result == pytest.approx([0.0, 0.0, 0.0])

    def test_negative_range(self):
        result = normalize([-10, 0, 10])
        assert result == pytest.approx([0.0, 0.5, 1.0])


class TestMatrixMultiply:
    def test_identity(self):
        identity = [[1, 0], [0, 1]]
        matrix = [[5, 6], [7, 8]]
        assert matrix_multiply(identity, matrix) == [[5, 6], [7, 8]]

    def test_2x2(self):
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        assert matrix_multiply(a, b) == [[19, 22], [43, 50]]

    def test_non_square(self):
        a = [[1, 2, 3]]
        b = [[4], [5], [6]]
        assert matrix_multiply(a, b) == [[32]]
