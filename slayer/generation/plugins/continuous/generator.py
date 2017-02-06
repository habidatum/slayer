from slayer import constants, file_utils
from slayer.generation import utils, volume, bin_aggregators
from slayer.generation.base import BaseGenerator

# Out of Date


class Generator(BaseGenerator):

    def generate_slisons(self, **kwargs):
        bbox, cell_size = kwargs.get('bbox'), kwargs.get('cell_size')
        weighted, aggregate_time = kwargs.get('weighted'), kwargs.get(
            'aggregate_time')

        ((self._x_size_, self._y_size_),
         (self._min_lon_, self._min_lat_),
         self._step_) = utils.get_bbox_geometry(bbox, cell_size)
        self._layer_id_ = kwargs.get('layer_id')

        std_data = file_utils.load_dataframe(kwargs.get('filepath'))

        agg_std_data = Generator.aggregate_date(std_data, aggregate_time)

        agg_std_data = utils.convert_lat(agg_std_data)
        categories_options = self.calculate_slices(agg_std_data, weighted)

        all_time_slices = agg_std_data.groupby(constants.start_date_column)

        self._z_size_ = len(all_time_slices)

        return {'x_size': self._x_size_,
                'y_size': self._y_size_,
                'z_size': self._z_size_,
                'categories': categories_options}

    def calculate_slices(self, std_data, weighted=False):
        categories = file_utils.extract_categories_columns(std_data)
        categories_options = file_utils.categories_options_dict(categories)

        for subset, option_slices in std_data.groupby(categories):
            time_slices = option_slices.groupby(constants.start_date_column)
            data_volume = self.calculate_volume(time_slices, weighted)
            self.export_volume(data_volume, subset)
            categories_options = file_utils.update_categories_options(
                categories_options, categories, subset)
        return categories_options

    def calculate_volume(self, slices, weighted=False):
        this_volume = volume.Volume()

        for slice_name, slice_df in slices:
            lats = slice_df[constants.lat_column].values
            lons = slice_df[constants.lon_column].values

            slice_index, slice_area, slice_counts = self.bin_count(lon=lons,
                                                                   lat=lats)
            if weighted:
                weights = slice_df[constants.weight_column].values
                final_slice_counts = bin_aggregators.bin_count_weighted(slice_index, slice_area, slice_counts, weights)
            else:
                final_slice_counts = slice_counts

            this_volume.add_slice((slice_name, final_slice_counts))

        return this_volume
