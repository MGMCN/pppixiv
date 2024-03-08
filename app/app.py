import logging
from flask import Flask
from router.pixiv_router import pixivServiceRouter
from router.static_router import staticServiceRouter
from services.pixiv import Pixiv


class App(Flask):
    def __init__(self, name):
        super().__init__(name)

    def init(self, config):
        self.logger.setLevel(logging.DEBUG)

        # init pixiv api
        self.username = config["username"]
        self.password = config["password"]
        self.myPixiv = Pixiv(service_name="pixiv", username=self.username, password=self.password,
                             interval=3500)

        # set router and pass pixivApi
        pixiv_router = pixivServiceRouter('pixiv_router', self.myPixiv)
        self.register_blueprint(pixiv_router.get_router())

        static_router = staticServiceRouter('static_router')
        self.register_blueprint(static_router.get_router())

        # pass logger to other services
        self.set_logger()

    def run_services(self) -> (bool, str):
        success, msg = self.myPixiv.start_pixiv_session()
        return success, msg

    def set_logger(self):
        self.myPixiv.set_logger(self.logger)
