import math
from geopy.distance import vincenty
from geopy.point import Point
from os import path
from slayer import file_utils, constants


def lat2y(a):
    return 180.0 / math.pi * math.log(
        math.tan(math.pi / 4.0 + a * (math.pi / 180.0) / 2.0))


def convert_lat(std_data):
    new_lat = std_data[constants.lat_column].apply(lat2y)
    std_data[constants.lat_column] = new_lat
    return std_data


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

