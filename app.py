import logging
import os

from dotenv import load_dotenv
from flask import Flask, request

from services.pixiv import Pixiv

load_dotenv(verbose=True)

app = Flask(__name__)
# set app logger
app.logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
app.logger.handlers.clear()
app.logger.addHandler(handler)

username = os.getenv("username")
password = os.getenv("password")
myPixiv = Pixiv(service_name="pixiv", username=username, password=password, interval=3500)
myPixiv.set_logger(app.logger)


def pack_json_data(l, success, message) -> dict:
    if success:
        json = {"status": 1, "message": "Get success! %s" % message, "list": l}
    else:
        json = {"status": 0, "message": "Get error... %s" % message, "list": {}}
    return json


# Only to see if this server is running correctly
@app.route('/')
def lsp():
    return 'Hello World! lsp!'


@app.route('/getIllustListByUid', methods=["POST"])
def getIllustListByUid():
    # Get uid from posted json
    uid = request.form["uid"]
    l, success, message = myPixiv.get_illust_list_by_uid(uid=uid)
    return pack_json_data(l, success, message)


@app.route('/getTrendingTags', methods=["GET"])
def getTrendingTags():
    l, success, message = myPixiv.get_trending_tags()
    return pack_json_data(l, success, message)


@app.route('/getIllustRanking', methods=["POST"])
def getIllustRanking():
    # Get mode from posted json
    mode = request.form["mode"]
    l, success, message = myPixiv.get_illust_ranking(mode=mode)
    return pack_json_data(l, success, message)


if __name__ == '__main__':
    app.logger.info("Authorized on pixiv account %s. Please wait for authentication.", username)
    success = myPixiv.start_pixiv_session()
    if success:
        app.logger.info("                    Pixiv Login Complete.")
        app.logger.info("======================================================================")
        app.run(host='0.0.0.0', port=5000, debug=True)
