from os import path, listdir
from slayer import file_utils
from slisonner import encoder


def pack_slisons(layer_id, slice_duration, x_size, y_size):
    slices_dir = file_utils.slices_dirpath(layer_id)

    for subset_id in listdir(slices_dir):
        subset_path = path.join(slices_dir, subset_id)
        slisons_dir = file_utils.slisons_dirpath(layer_id, subset_id)

        for f in listdir(subset_path):
            timestamp, ext = path.splitext(f)
            if not ext == '.raw':
                continue

            file_path = path.join(subset_path, f)

            encoder.encode_slice(filepath=file_path,
                                 slice_duration=slice_duration,
                                 timestamp=int(timestamp),
                                 layer_id=layer_id,
                                 x_size=x_size,
                                 y_size=y_size,
                                 value_type='float32',
                                 out_dir=slisons_dir)
