from flask import Flask, request
from dotenv import load_dotenv
import os
from services.pixiv import Pixiv

load_dotenv(verbose=True)

app = Flask(__name__)
username = os.getenv("username")
password = os.getenv("password")
myPixiv = Pixiv(username=username, password=password, interval=3500)
myPixiv.startPixivSession()


# Only to see if this server is running correctly
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getIllustListByUid', methods=["POST"])
def getIllustListByUid():
    # Get uid from posted json
    uid = request.form["uid"]
    l, success, message = myPixiv.getIllustListByUid(uid)
    if success:
        json = {"status": 1, "message": "Get success! %s" % message, "list": l}
    else:
        json = {"status": 0, "message": "Get error... %s" % message}
    return json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
