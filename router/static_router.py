from .base import BaseRouter
from flask import Blueprint, send_from_directory


class staticServiceRouter(BaseRouter):

    def __init__(self, router_name):
        super().__init__(router_name=router_name)
        self.router = Blueprint(router_name, __name__)
        self.register_routes()

    def register_routes(self):
        # Only to see if this server is running correctly
        @self.router.route('/')
        def lsp():
            return 'Hello World! lsp!'

        @self.router.route('/Illusts/<path:path>')
        def send_illusts(path):
            return send_from_directory('Illusts', path)
