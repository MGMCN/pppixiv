import time

import pixivpy3 as pixiv
from flask import Flask, request
from gppt import GetPixivToken
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


refresh_token = None
username = os.getenv("username")
password = os.getenv("password")


def getToken() -> (str, bool):
    global username, password
    retry = 5
    token = None
    err = False
    g = GetPixivToken()

    while retry > 0:
        try:
            res = g.login(headless=True, username=username, password=password)
            token = res["refresh_token"]
            break
        except ValueError:
            print("getToken error!")
        time.sleep(0.5)
        retry -= 1
    print(token)

    if token is None:
        err = True
    return token, err


def packIllustUrl(uid) -> str:
    return "https://www.pixiv.net/artworks/%s" % uid


@app.route('/getIllustListByUid', methods=["POST"])
def getIllustListByUid():
    global refresh_token
    # Get uid from posted json
    uid = request.form["uid"]
    # Only for test
    # uid = "4837211"
    returnJson = {"list": {}}
    err = False
    # load_dotenv(verbose=True)

    # Init pixiv api
    api = pixiv.AppPixivAPI()

    # Get pixiv token
    if refresh_token is None:
        refresh_token, err = getToken()

    if err:
        # returnJson["status"] = 0
        return {"status": 0}
    else:
        # Set pixiv token
        while True:
            try:
                api.auth(refresh_token=refresh_token)
                break
            except pixiv.utils.PixivError:
                print('The token has expired and needs to be reset!')
                refresh_token, err = getToken()
                if err:
                    # returnJson["status"] = 0
                    return {"status": 0}

    offset = 0

    while True:
        res = api.user_illusts(uid, type="illust", offset=offset)
        for item in res["illusts"]:
            # Title encoding type Unicode
            returnJson["list"][item["title"]] = packIllustUrl(item["id"])
        if res["next_url"] is None:
            break
        offset = api.parse_qs(res["next_url"])["offset"]

    returnJson["status"] = 1
    return returnJson


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
