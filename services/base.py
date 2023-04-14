class BaseService:
    def __init__(self, service_name):
        self.serviceName = service_name
        self.logger = None

    def set_logger(self, logger):
        self.logger = logger
