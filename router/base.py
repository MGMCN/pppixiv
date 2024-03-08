class BaseRouter:
    def __init__(self, router_name: str):
        self.routerName = router_name
        self.router = None
        self.service_api = None
        self.logger = None

    def register_routes(self):
        return

    def get_router(self):
        return self.router

    def set_service_api(self, service_api):
        self.service_api = service_api

    # customizable
    def set_logger(self, logger):
        self.logger = logger
