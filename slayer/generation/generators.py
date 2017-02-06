from slayer import plugin_loader
from slayer.generation import plugins


def get(plugin_id):
    generation_plugins = plugin_loader.get_plugins(plugins)
    data_generator = generation_plugins[plugin_id].Generator
    return data_generator
