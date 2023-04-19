import logging
import os

from dotenv import load_dotenv
from flask import Flask

from router.pixiv_router import pixiv_router, router_set_pixiv_api
from services.pixiv import Pixiv


class App(Flask):
    def __init__(self, name: str):
        super().__init__(name)
        self.init()

    def init(self):
        load_dotenv(verbose=True)
        self.logger.setLevel(logging.DEBUG)
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        self.myPixiv = Pixiv(service_name="pixiv", username=self.username, password=self.password, interval=3500)
        self.register_blueprint(pixiv_router)
        self.pass_context()

    def run_services(self) -> (bool, str):
        success, msg = self.myPixiv.start_pixiv_session()
        return success, msg

    def pass_context(self):
        self.myPixiv.set_logger(self.logger)
        # Not graceful
        router_set_pixiv_api(self.myPixiv)
