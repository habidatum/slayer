import pandas as pd
from slayer import constants
import itertools
from datetime import datetime
from collections import OrderedDict


def extract_std_data(df):
    categories_columns = extract_categories_columns(df)
    default_columns = [constants.start_date_column,
                       constants.end_date_column,
                       constants.lon_column,
                       constants.lat_column,
                       constants.weight_column]

    return df[default_columns + categories_columns]


def extract_subsets(filepath, additive=True):
    df = load_dataframe(filepath)
    categories = extract_categories_columns(df)
    categories_options = extract_categories_options(df, categories)
    if additive:
        subsets = get_additive_subsets(categories, df)
    else:
        subsets = get_nonadditive_subsets(categories, categories_options)
    subsets = remove_categories_prefix(subsets)
    return subsets


def remove_categories_prefix(subsets):
    return [{category[len(constants.category_column_prefix):]: options
             for category, options in subset.items()}
            for subset in subsets]


def get_subset(subset_options, categories):
    if not isinstance(subset_options, list):
        subset_options = [subset_options]

    subset = {categories[i]: [option] for i, option in
              enumerate(subset_options)}
    return subset


def get_subset_nonadditive(subset_options, categories):
    subset = {categories[i]: options for i, options in
              enumerate(subset_options)}
    return subset


def dump_std_data(df, filepath):
    dump_dataframe(df, filepath)


def load_dataframe(filepath):
    return pd.read_csv(filepath)


def dump_dataframe(df, filepath):
    df.to_csv(filepath, index=None)


def sorted_categories(categories):
    return sorted(categories)


def extract_categories_columns(std_data):
    categories = [clmn for clmn in std_data.columns
                  if clmn.startswith(constants.category_column_prefix)]
    sorted_categories_names = sorted_categories(categories)
    return sorted_categories_names


def extract_categories_options(std_data, categories):
    def sorted_options(category_values):
        return sorted([str(opt) for opt in category_values.unique()])

    cats = {category: sorted_options(std_data[category])
            for category in categories}
    return OrderedDict(sorted(cats.items(), key=lambda tup: tup[0]))


def get_category_options_combinations(options):
    sizes = range(1, len(options) + 1)
    combinations_by_size = [itertools.combinations(options, size)
                            for size in sizes]
    return list(itertools.chain(*combinations_by_size))


def get_nonadditive_subsets(categories, categories_options):
    options_by_categories = [get_category_options_combinations(options)
                             for options in categories_options.values()]
    combinations = itertools.product(*options_by_categories)
    subsets = [{categories[i]: list(options)
                for (i, options) in enumerate(subset_options)}
               for subset_options in combinations]
    return subsets


def get_additive_subsets(categories, df):
    subsets = [get_subset(subset_options, categories)
               for subset_options, subset_slices in df.groupby(categories)]
    return subsets


def detect_dateformat(date_column):
    date_element = date_column.iloc[0]
    try:
        date = datetime.fromtimestamp(date_element)
        if date.year > 2100:  # Just some large enough year
            return constants.DateFormat.timestamp_ms
        else:
            return constants.DateFormat.timestamp
    except TypeError:
        return constants.DateFormat.datestring
    except ValueError:
        return constants.DateFormat.timestamp_ms
