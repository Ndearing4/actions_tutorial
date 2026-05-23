import numpy as np


def descriptive_stats(data):
    """Return mean, median, and std dev for a list of numbers."""
    arr = np.array(data, dtype=float)
    return {
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr)),
    }


def moving_average(data, window):
    """Compute a simple moving average using a convolution kernel."""
    arr = np.array(data, dtype=float)
    if window < 1 or window > len(arr):
        raise ValueError("window must be between 1 and the length of data")
    kernel = np.ones(window) / window
    return np.convolve(arr, kernel, mode="valid").tolist()


def normalize(data):
    """Min-max normalize an array to the [0, 1] range."""
    arr = np.array(data, dtype=float)
    min_val = np.min(arr)
    max_val = np.max(arr)
    if min_val == max_val:
        return np.zeros_like(arr).tolist()
    return ((arr - min_val) / (max_val - min_val)).tolist()


def matrix_multiply(a, b):
    """Multiply two 2-D matrices."""
    return (np.array(a) @ np.array(b)).tolist()
