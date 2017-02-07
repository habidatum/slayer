import numpy as np


def weighted_mean(index, slice_area, counts, weights):
    weighted = np.bincount(index, minlength=slice_area, weights=weights)
    weighted_counts = weighted/counts
    # The NaNs here represent the places with no measurements
    return weighted_counts


def weighted_sum(index, slice_area, counts, weights):
    weighted = np.bincount(index, minlength=slice_area, weights=weights)
    # The NaNs here represent the places with no measurements
    weighted[counts == 0.0] = np.nan
    return weighted
