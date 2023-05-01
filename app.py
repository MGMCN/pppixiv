import logging
from flask import Flask
from router.pixiv_router import pixiv_router, router_set_pixiv_api
from services.pixiv import Pixiv


class App(Flask):
    def __init__(self, name, username, password, gfw):
        super().__init__(name)
        self.init(username, password, gfw)

    def init(self, username, password, gfw):
        self.logger.setLevel(logging.DEBUG)
        self.username = username
        self.password = password
        self.gfw = True if gfw == "1" else False
        self.myPixiv = Pixiv(service_name="pixiv", gfw=self.gfw, username=self.username, password=self.password,
                             interval=3500)
        self.register_blueprint(pixiv_router)
        self.pass_context()

    def run_services(self) -> (bool, str):
        self.logger.debug(f"gfw mode -> {self.gfw}")
        success, msg = self.myPixiv.start_pixiv_session()
        return success, msg

    def pass_context(self):
        self.myPixiv.set_logger(self.logger)
        # Not graceful
        router_set_pixiv_api(self.myPixiv)
