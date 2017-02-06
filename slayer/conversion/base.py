import pandas as pd
from slayer import constants


class BaseConverter(object):
    def __init__(self, **kwargs):
        pass

    def convert_data(self, **kwargs):

        raise NotImplementedError

    @staticmethod
    def convert_dates(raw_data, source_date_format, start_date_column,
                      end_date_column=None, date_format=None):
        start_slices = convert_date_column(raw_data[start_date_column],
                                           source_date_format, date_format)
        raw_data[constants.start_date_column] = start_slices

        if end_date_column:
            end_slices = convert_date_column(raw_data[end_date_column],
                                             source_date_format, date_format)
            raw_data[constants.end_date_column] = end_slices
        else:
            raw_data[constants.end_date_column] = start_slices

        return raw_data

    @staticmethod
    def convert_categories(raw_data, categories):
        renamed_columns = {category: constants.category_column_prefix + category
                           for category in categories}
        raw_data.rename(columns=renamed_columns, inplace=True)
        return raw_data

    @staticmethod
    def add_default_category(raw_data):
        raw_data[constants.default_category] = constants.default_option
        return raw_data, [constants.default_category]

    @staticmethod
    def add_default_weight(raw_data):
        raw_data[constants.weight_column] = 1.0
        return raw_data

    @staticmethod
    def convert_weight(raw_data, weight_column):
        if weight_column:
            renamed_columns = {weight_column: constants.weight_column}
            raw_data.rename(columns=renamed_columns, inplace=True)
        else:
            raw_data = BaseConverter.add_default_weight(raw_data)
        return raw_data


def convert_date_column(date_column, source_date_format, date_format):
    if source_date_format == constants.DateFormat.timestamp:
        return pd.to_datetime(date_column, unit='s',
                              infer_datetime_format=True, utc=True)
    return pd.to_datetime(date_column, format=date_format,
                          infer_datetime_format=True, utc=True)

