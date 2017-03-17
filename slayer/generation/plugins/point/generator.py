from slayer import constants, file_utils
from slayer.generation import utils
from slayer.generation.base import BaseGenerator
from isodate import parse_duration
import numpy as np
from pandas import TimeGrouper, to_datetime


class Generator(BaseGenerator):

    def generate_slisons(self, **kwargs):
        weight_function = kwargs.get('weight_function', None)
        additive = kwargs.get('additive', True)
        std_data = file_utils.load_dataframe(kwargs.get('filepath'))

        data = utils.index_datetime(std_data, self._tz_)
        data = utils.filter_df_time_intervals(data, self._time_intervals_)
        data = utils.convert_lat(data)
        categories_options = self.calculate_slices(data, weight_function, additive)

        result = {'x_size': self._x_size_, 'y_size': self._y_size_,
                  'categories': categories_options}
        if self._finish_callback_:
            self._finish_callback_(**result)

        return result

    def calculate_slices(self, data, weight_function=None, additive=True):
        categories = file_utils.extract_categories_columns(data)
        categories_options = file_utils.extract_categories_options(data, categories)
        self._slices_calculation(additive)(data, categories, categories_options, weight_function)

        return categories_options

    def additive(self, data, categories, categories_options, weight_function=None):
        for subset_options, subset_data in data.groupby(categories):
            self.calculate_subset(subset_data, weight_function, subset_options,
                                  categories, file_utils.get_subset)

    def nonadditive(self, data, categories, categories_options, weight_function=None):
        subsets = file_utils.get_nonadditive_subsets(categories_options)

        for subset_options in subsets:
            subset_data = self.non_additive_subset_data(data, subset_options)
            self.calculate_subset(subset_data, weight_function, subset_options,
                                  categories, file_utils.get_subset_nonadditive)

    def calculate_subset(self, subset_data, weight_function, subset_options,
                         categories, subset_function):
        slice_duration = parse_duration(self._slice_duration_)
        slice_data = self.group_by_time(subset_data, slice_duration)
        data_volume = self.calculate_volume(slice_data, weight_function)
        subset = subset_function(subset_options, categories)
        self.export_volume(subset, data_volume)

    def group_by_time(self, data, slice_duration):
        time_slices = data.groupby(TimeGrouper(freq=slice_duration))
        return time_slices

    def non_additive_subset_data(self, data, subset_options):
        subsets_boolean = [data[category].isin(options) for
                           (category, options) in subset_options.items()]
        subset_index = np.logical_and(*subsets_boolean)
        return data[subset_index]

    def _slices_calculation(self, additive):
        return {True: self.additive,
                False: self.nonadditive}[additive]
