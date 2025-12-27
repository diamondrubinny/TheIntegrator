import os
import importlib
import inspect
from core.base_plugin import BasePlugin

class PluginManager:
    def __init__(self, config, logger, plugin_folder='plugins'):
        self.config = config
        self.logger = logger
        self.plugin_folder = plugin_folder
        self.plugins = []

    def discover_plugins(self):
        self.plugins = []
        if not os.path.exists(self.plugin_folder):
            os.makedirs(self.plugin_folder)

        for filename in os.listdir(self.plugin_folder):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f'{self.plugin_folder}.{module_name}')
                    # טעינה מחדש כדי לוודא שפלאגינים חדשים שנוצרו ע"י ה-AI נטענים
                    importlib.reload(module) 
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, BasePlugin) and obj is not BasePlugin:
                            instance = obj(self.config, self.logger)
                            self.plugins.append(instance)
                except Exception as e:
                    self.logger.error(f"Error loading {module_name}: {e}")

    def get_plugins(self):
        return self.plugins
