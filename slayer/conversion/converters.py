from slayer import plugin_loader
from slayer.conversion import plugins


def get(converter_type):
    conversion_plugins = plugin_loader.get_plugins(plugins)
    data_converter = conversion_plugins[converter_type].Converter()
    return data_converter
