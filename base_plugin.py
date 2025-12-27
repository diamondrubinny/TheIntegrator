from abc import ABC, abstractmethod

class BasePlugin(ABC):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def run(self):
        """Main execution logic"""
        pass
