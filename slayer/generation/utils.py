import math
from geopy.distance import vincenty
from geopy.point import Point
from os import path
from slayer import file_utils, constants
from datetime import datetime
from isodate import parse_datetime, parse_duration, datetime_isoformat
import pytz
import pandas as pd


def lat2y(a):
    return 180.0 / math.pi * math.log(
        math.tan(math.pi / 4.0 + a * (math.pi / 180.0) / 2.0))


def y2lat(a):
    return 180.0/math.pi*(2.0*math.atan(math.exp(a*math.pi/180.0))-math.pi/2.0)


def convert_lat(std_data):
    new_lat = std_data[constants.lat_column].apply(lat2y)
    std_data[constants.lat_column] = new_lat
    return std_data


def convert_time_intervals(time_intervals):
    return [[parse_datetime(time_int[0]), parse_datetime(time_int[1])]
            for time_int in time_intervals]


def filter_df_time_intervals(data, time_intervals):
    dfs = [data[time_int[0]:time_int[1]] for time_int in time_intervals]
    return pd.concat(dfs)


def index_datetime(std_data, tz='UTC'):
    std_data.index = pd.to_datetime(std_data[constants.start_date_column],
                                    infer_datetime_format=True)
    std_data.index = std_data.index.tz_localize('UTC').tz_convert(tz)
    std_data.sort_index(inplace=True)
    return std_data


def clap_time_intervals(time_intervals, slice_duration):
    intervals = convert_time_intervals(time_intervals)
    freq = parse_duration(slice_duration)
    grouper = pd.TimeGrouper(freq=freq)

    def clap(boundary): return pd.DataFrame(index=[boundary]).groupby(grouper)

    def extract(boundary): return next(iter(boundary.groups))

    clapped_time_intervals = [[datetime_isoformat(extract(clap(boundary)))
                               for boundary in time_int]
                              for time_int in intervals]
    return clapped_time_intervals


def approximated_time_intervals(tz):
    source_intetval = [datetime(1970, 1, 2, 0, 0, 0),
                       datetime(1970, 1, 3, 0, 0, 0)]
    utc_interval = [pytz.timezone(tz).localize(dt).astimezone(pytz.UTC) for dt in source_intetval]
    return [datetime_isoformat(dt) for dt in utc_interval]


def fit_bbox(bottom_right_lon, bottom_right_lat, top_left_lon, top_left_lat, cell_size):
    size, (min_lon, min_lat), step = get_bbox_geometry(constants.Bbox(bottom_right_lat=bottom_right_lat,
                                     bottom_right_lon=bottom_right_lon,
                                     top_left_lat=top_left_lat,
                                     top_left_lon=top_left_lon), cell_size)

    new_bottom_right_lon = min_lon + step * size[0]
    new_top_left_lat = y2lat(min_lat + step * size[1])
    return bottom_right_lon, bottom_right_lat, top_left_lon, top_left_lat


def get_bbox_geometry(bbox, cell_size):
    min_lat, max_lat = lat2y(bbox.min_lat), lat2y(bbox.max_lat)

    width = vincenty(Point(latitude=bbox.min_lat, longitude=bbox.min_lon),
                     Point(latitude=bbox.min_lat, longitude=bbox.max_lon)).meters

    height = vincenty(Point(latitude=bbox.min_lat, longitude=bbox.min_lon),
                      Point(latitude=bbox.max_lat, longitude=bbox.min_lon)).meters

    x_size = math.ceil(width / cell_size)
    y_size = math.ceil(height / cell_size)
    size = (x_size, y_size)

    print('Volume Size: {}'.format(size))

    step = round(abs((bbox.max_lon - bbox.min_lon) / x_size), 5)

    return size, (bbox.min_lon, min_lat), step


def export_slice(data_slice, value_type, dataset, subset_id, timestamp):
    slice_dir = file_utils.slices_dirpath(dataset, subset_id)

    filepath = path.join(slice_dir, "{}.raw".format(timestamp))

    data_slice.astype(value_type).tofile(filepath)

