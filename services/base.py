import logging


class BaseService:
    def __init__(self, service_name: str):
        self.serviceName = service_name
        self.logger = None

    def set_logger(self, logger: logging.Logger):
        self.logger = logger

    def get_service_name(self) -> str:
        return self.serviceName
