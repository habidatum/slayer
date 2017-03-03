from enum import Enum
from geopy import point

time_column = 'time_slice'
lon_column = 'lon'
lat_column = 'lat'
weight_column = 'sl_weight'
category_column_prefix = 'sl_category_'
default_category = 'main'
default_option = 'all'


class DateFormat(Enum):
    datestring = 0
    timestamp = 1
    timestamp_ms = 2


class Bbox:
    def __init__(self, bottom_right_lon, bottom_right_lat,
                 top_left_lon, top_left_lat):
        self.__south_east__ = point.Point(latitude=bottom_right_lat,
                                          longitude=bottom_right_lon)
        self.__north_west__ = point.Point(latitude=top_left_lat,
                                          longitude=top_left_lon)

    @property
    def min_lat(self):
        return self.__south_east__.latitude

    @property
    def min_lon(self):
        return self.__north_west__.longitude

    @property
    def max_lat(self):
        return self.__north_west__.latitude

    @property
    def max_lon(self):
        return self.__south_east__.longitude

    def geo_bounds(self):
        bounds = {'cornerBottomRight': {'lon': self.__south_east__.longitude,
                                        'lat': self.__south_east__.latitude},
                  'cornerTopLeft': {'lon': self.__north_west__.longitude,
                                    'lat': self.__north_west__.latitude}}
        return bounds


start_date_column = 'sl_start_date'
end_date_column = 'sl_end_date'
