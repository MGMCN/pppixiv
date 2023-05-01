from dotenv import load_dotenv
import os
from app import App
from flask import send_from_directory

load_dotenv(verbose=True)

username = os.getenv("username")
password = os.getenv("password")
port = os.getenv("port")
gfw = os.getenv("gfw")

app = App(__name__, username, password, gfw)


# Only to see if this server is running correctly
@app.route('/')
def lsp():
    return 'Hello World! lsp!'


@app.route('/Illusts/<path:path>')
def send_illusts(path):
    return send_from_directory('Illusts', path)


if __name__ == '__main__':
    app.logger.debug("=====================================================================================")
    app.logger.debug(f"Authorized on pixiv account {username}. Please wait for authentication.")
    success, msg = app.run_services()
    if success:
        app.logger.debug("Pixiv Login Complete.")
        app.logger.debug("=====================================================================================")
        app.run(host='0.0.0.0', port=port)
    else:
        app.logger.debug(msg)
        app.logger.debug("Application ends gracefully.")
        app.logger.debug("=====================================================================================")
