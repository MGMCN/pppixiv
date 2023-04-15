import logging
import os

from dotenv import load_dotenv
from flask import Flask

from router.pixiv_router import pixiv_router, router_set_pixiv_api
from services.pixiv import Pixiv

load_dotenv(verbose=True)

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

username = os.getenv("username")
password = os.getenv("password")
myPixiv = Pixiv(service_name="pixiv", username=username, password=password, interval=3500)
myPixiv.set_logger(app.logger)

app.register_blueprint(pixiv_router)


# Only to see if this server is running correctly
@app.route('/')
def lsp():
    return 'Hello World! lsp!'


if __name__ == '__main__':
    # Not graceful
    router_set_pixiv_api(myPixiv)
    app.logger.debug("Authorized on pixiv account %s. Please wait for authentication.", username)
    success = myPixiv.start_pixiv_session()
    if success:
        app.logger.debug("Pixiv Login Complete.")
        app.logger.debug("=================================================================")
        app.run(host='0.0.0.0', port=3333)
