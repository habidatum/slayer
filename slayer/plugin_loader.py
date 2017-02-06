import pkgutil


def get_plugins(plugins_module):
    plugins = {}
    prefix = plugins_module.__name__ + "."
    for importer, modname, ispkg in pkgutil.iter_modules(plugins_module.__path__,
                                                         prefix):
        module = importer.find_module(modname).load_module(modname)
        modname = modname.split('.')[-1]
        plugins[modname] = module

    return plugins
