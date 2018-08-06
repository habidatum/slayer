from slayer.generation import utils
from slayer.generation.base import BaseGenerator


class Generator(BaseGenerator):
    get_bbox_geometry_function = utils.get_bbox_geometry_by_degree

    def generate_slisons(self, **kwargs):
        kwargs['mercator_conversion'] = False
        super(Generator, self).generate_slisons(**kwargs)

