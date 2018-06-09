from slayer.conversion.base import BaseConverter
import numpy as np
from slayer import file_utils, constants


class Converter(BaseConverter):

    def convert_data(self, **kwargs):
        if kwargs.get('filepath', None):
            raw_data = file_utils.load_dataframe(kwargs.get('filepath'))
        else:
            raw_data = kwargs.get('df')
        output_filepath = kwargs.get('output_filepath', None)
        start_date_column = kwargs.get('start_date_column')
        categories = kwargs.get('categories_columns')
        end_date_column = kwargs.get('end_date_column', None)
        dataset_time_zone = kwargs.get('dataset_time_zone', None)
        weight_column = kwargs.get('weight_column', None)
        lat_column = kwargs.get('lat_column', 'lat')
        lon_column = kwargs.get('lon_column', 'lon')

        raw_data.dropna(subset=[lon_column, lat_column, start_date_column],
                        how='any', inplace=True)

        if not categories:
            raw_data, categories = Converter.add_default_category(raw_data)

        data = Converter.convert_categories(raw_data, categories)
        data = Converter.convert_dates(data, start_date_column, end_date_column,
                                       dataset_time_zone=dataset_time_zone)
        data = Converter.convert_weight(data, weight_column)
        data = Converter.convert_spatial(data, lat_column, lon_column)

        std_df = file_utils.extract_std_data(data)
        if output_filepath:
            file_utils.dump_std_data(std_df, output_filepath)
        if weight_column:
            data_type = [nice_type for nice_type, np_types
                         in np.sctypes.items()
                         if std_df[constants.weight_column].dtype in np_types][-1]
            return {'data_type': data_type,
                    'df': std_df}
        else:
            return {'data_type': 'uint',
                    'df': std_df}
