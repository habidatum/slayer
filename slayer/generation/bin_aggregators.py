import numpy as np


def weighted_mean(index, slice_area, counts, weights):
    weighted = np.bincount(index, minlength=slice_area, weights=weights)
    weighted_counts = weighted/counts

    nans_index = np.isnan(weighted_counts)
    weighted_counts[nans_index] = 0.0
    return weighted_counts


def weighted_sum(index, slice_area, counts, weights):
    weighted = np.bincount(index, minlength=slice_area, weights=weights)
    return weighted
