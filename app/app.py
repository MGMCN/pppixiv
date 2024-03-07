import logging
from flask import Flask
from router.pixiv_router import pixiv_router, router_set_pixiv_api
from router.static_router import static_router
from services.pixiv import Pixiv


class App(Flask):
    def __init__(self, name):
        super().__init__(name)

    def init(self, config):
        self.logger.setLevel(logging.DEBUG)
        self.username = config["username"]
        self.password = config["password"]
        self.myPixiv = Pixiv(service_name="pixiv", username=self.username, password=self.password,
                             interval=3500)
        self.register_blueprint(pixiv_router)
        self.register_blueprint(static_router)
        self.pass_context()

    def run_services(self) -> (bool, str):
        success, msg = self.myPixiv.start_pixiv_session()
        return success, msg

    def pass_context(self):
        self.myPixiv.set_logger(self.logger)
        # Not graceful
        router_set_pixiv_api(self.myPixiv)
