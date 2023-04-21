from abc import abstractmethod


class BaseParser:

    def __init__(self):
        self.logger = None

    def set_logger(self, logger):
        self.logger = logger

    @abstractmethod
    def parse(self, data):
        pass
