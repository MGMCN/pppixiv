from flask import Blueprint, send_from_directory

static_router = Blueprint('static_router', __name__)


# Only to see if this server is running correctly
@static_router.route('/')
def lsp():
    return 'Hello World! lsp!'


@static_router.route('/Illusts/<path:path>')
def send_illusts(path):
    return send_from_directory('Illusts', path)
