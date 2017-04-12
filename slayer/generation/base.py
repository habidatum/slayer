import numpy as np

from slayer import constants, file_utils
from slayer.generation import utils, volume, bin_aggregators
from slisonner import encoder
from isodate import datetime_isoformat


class BaseGenerator:
    def __init__(self, **kwargs):
        bbox, cell_size = kwargs.get('bbox'), kwargs.get('cell_size')
        bbox = constants.Bbox(**bbox)

        ((self._x_size_, self._y_size_),
         (self._min_lon_, self._min_lat_),
         self._step_) = utils.get_bbox_geometry(bbox, cell_size)
        self._layer_id_ = kwargs.get('layer_id')
        self._slice_duration_ = kwargs.get('slice_duration')
        self._value_type_ = kwargs.get('value_type', 'float32')
        self._tz_ = kwargs.get('tz', 'UTC')
        self._approximated_ = kwargs.get('approximated', False)
        time_intervals = kwargs.get('time_intervals', None)
        if time_intervals:
            self._time_intervals_ = utils.convert_time_intervals(time_intervals)

        self._progress_callback_ = None
        self._finish_callback_ = None

    def bind_callbacks(self, progress_callback, finish_callback):
        self._progress_callback_ = progress_callback
        self._finish_callback_ = finish_callback

    def generate_slisons(self, **kwargs):
        raise NotImplementedError

    def calculate_slices(self, *args):
        raise NotImplementedError

    def calculate_volume(self, slices, weight_function=None):
        subset_volume = volume.Volume()

        for slice_id, slice_df in slices:
            if len(slice_df):
                slice_data = self.calculate_slice(slice_df, weight_function)
                subset_volume.add_slice((slice_id, slice_data))

        return subset_volume

    def calculate_slice(self, slice_df, weight_function):
        lats = slice_df[constants.lat_column].values
        lons = slice_df[constants.lon_column].values

        (slice_index, slice_area,
         slice_counts, mask) = self.bin_count(lon=lons, lat=lats)
        if weight_function:
            weights = slice_df[constants.weight_column].values
            weights = weights[mask]
            aggregator = bin_aggregators.aggregator(weight_function)

            final_slice_counts = aggregator(slice_index, slice_area,
                                            slice_counts, weights)
        else:
            final_slice_counts = slice_counts
        return final_slice_counts

    def bin_count(self, lon, lat):
        '''
        Calculate the number of points in each bin in the slice
        :param lon: the list of longitudes
        :param lat: the list of latitudes
        :return: (linear index of counts in each bin, square area of the slice,
                  counts for each bin, boolean mask of indices in the bbox)
        '''
        lon_index, lon_mask = self.clip_index(lon, self._min_lon_, self._x_size_)
        lat_index, lat_mask = self.clip_index(lat, self._min_lat_, self._y_size_)

        index = (lat_index * self._x_size_ + lon_index).astype('int64')
        mask = lon_mask & lat_mask
        index = index[mask]

        slice_area = self._x_size_ * self._y_size_
        counts = np.bincount(index, minlength=slice_area)

        return index, slice_area, counts, mask

    def clip_index(self, values, start_value, clip_size):
        '''
        Converts lat/lon list to a list of their bin indices
        :param values: the list of lat/lon values
        :param start_value: the starting value of the bbox
        :param clip_size: the x/y size of the slice
        :return: (indices of the bins, mask of the values that are inside bbox)
        '''
        relative_values = np.abs((values - start_value) / self._step_)
        round_values = np.floor(relative_values)
        index_mask = (round_values >= 0) & (round_values < clip_size)
        clipped_index = np.clip(round_values, 0, clip_size - 1)
        return clipped_index, index_mask

    def export_volume(self, subset, data_volume):
        if self._progress_callback_:
            slisons = self.slices_to_slisons(data_volume.slices)
            subset = file_utils.remove_categories_prefix([subset])[0]
            self._progress_callback_(subset, slisons)
        return data_volume.min, data_volume.max

    def export_locally(self, subset, data_volume):
        for timestamp, slice_data in data_volume.slices.items():
            utils.export_slice(slice_data, self._value_type_, self._layer_id_,
                               subset, timestamp)

    def slices_to_slisons(self, slices):
        meta = self.shared_slison_meta()
        slisons = []
        for time_slice, slice_data in slices.items():
            if not sum(~np.isnan(slice_data)):
                continue
            utc_slice = time_slice.tz_convert('UTC')
            meta['timestamp'] = datetime_isoformat(utc_slice)
            slice_data_typed = slice_data.astype(self._value_type_)
            slice_meta, slison = encoder.encode_slice(slice_data_typed, **meta)
            slisons.append({'datetime': utc_slice,
                            'bytes': slison})
        return slisons

    def shared_slison_meta(self):
        return {'slice_duration': self._slice_duration_,
                'layer_id': self._layer_id_,
                'x_size': self._x_size_,
                'y_size': self._y_size_,
                'value_type': self._value_type_}
