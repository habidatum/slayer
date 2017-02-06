from slayer import file_utils, constants
from collections import OrderedDict
import pandas as pd
from os import path


def test_subset_id_nonadditive():
    subset = ('close', 'short')
    categories_options = reference_categories_options()
    subset_id = file_utils.get_subset_id_nonadditive(subset, categories_options)
    assert subset_id == reference_subset_id()


def test_subset_id_additive():
    subset = ('close', 'short')
    subset_id = file_utils.get_subset_id(subset)
    assert subset_id == 'close_short'


def test_categories_extraction():
    std_data = std_df()
    categories = file_utils.extract_categories_columns(std_data)
    assert categories == reference_categories()


def test_category_options_extraction():
    std_data = std_df()
    categories = file_utils.extract_categories_columns(std_data)
    categories_options = file_utils.extract_categories_options(std_data,
                                                               categories)
    assert categories_options == reference_categories_options()


def test_nonadditive_slison_url():
    layer_id = 'layer'
    categories_options = reference_categories_options()
    slison_url = file_utils.slisons_url_format(layer_id, categories_options,
                                               additive=False)
    reference_url = path.join(constants.slison_URL_format, layer_id,
                              'sl_category_distance_{close}_{far}_{really_far}_sl_category_time_{long}_{short}/${ID}.slison')
    assert slison_url == reference_url


def test_additive_slison_url():
    layer_id = 'layer'
    categories_options = reference_categories_options()
    slison_url = file_utils.slisons_url_format(layer_id, categories_options,
                                               additive=True)
    reference_url = path.join(constants.slison_URL_format, layer_id,
                              '{sl_category_distance}_{sl_category_time}/${ID}.slison')
    assert slison_url == reference_url


# Reference Mock Data
def std_df():
    std_data = pd.DataFrame(
        {'sl_category_time': ['short', 'long', 'short', 'long'],
         'sl_category_distance': ['close', 'far', 'really_far', 'far']})
    return std_data


def reference_categories_options():
    categories_options = {'sl_category_time': sorted(['short', 'long']),
                          'sl_category_distance': sorted(['close', 'far',
                                                          'really_far'])}
    return OrderedDict(sorted(categories_options.items(),
                              key=lambda tup: tup[0]))


def reference_categories():
    return file_utils.sorted_categories(['sl_category_time',
                                         'sl_category_distance'])


def reference_subset_id():
    return 'sl_category_distance_on_off_off_sl_category_time_off_on'
