from slayer.conversion.base import BaseConverter
from slayer import file_utils


class Converter(BaseConverter):

    def convert_data(self, **kwargs):

        raw_data = file_utils.load_dataframe(kwargs.get('filepath'))
        output_filepath = kwargs.get('output_filepath')
        start_date_column = kwargs.get('start_date_column')
        categories = kwargs.get('categories_columns')
        end_date_column = kwargs.get('end_date_column', None)
        weight_column = kwargs.get('weight_column', None)
        lat_column = kwargs.get('lat_column', 'lat')
        lon_column = kwargs.get('lat_column', 'lon')

        if not categories:
            raw_data, categories = Converter.add_default_category(raw_data)

        data = Converter.convert_categories(raw_data, categories)
        data = Converter.convert_dates(data, start_date_column, end_date_column)
        data = Converter.convert_weight(data, weight_column)
        data = Converter.convert_spatial(data, lat_column, lon_column)

        std_df = file_utils.extract_std_data(data)
        file_utils.dump_std_data(std_df, output_filepath)
