from flask import Blueprint, request

pixiv = Blueprint('pixiv', __name__)

# Not graceful
mybpPixiv = None


def set_pixiv_api(api):
    global mybpPixiv
    mybpPixiv = api


def pack_json_data(l, success, message) -> dict:
    if success:
        json = {"status": 1, "message": "Get success! %s" % message, "list": l}
    else:
        json = {"status": 0, "message": "Get error... %s" % message, "list": {}}
    return json


@pixiv.route('/getIllustListByUid', methods=["POST"])
def getIllustListByUid():
    # Get uid from posted json
    uid = request.form["uid"]
    l, success, message = mybpPixiv.get_illust_list_by_uid(uid=uid)
    return pack_json_data(l, success, message)


@pixiv.route('/getTrendingTags', methods=["GET"])
def getTrendingTags():
    l, success, message = mybpPixiv.get_trending_tags()
    return pack_json_data(l, success, message)


@pixiv.route('/getIllustRanking', methods=["POST"])
def getIllustRanking():
    # Get mode from posted json
    mode = request.form["mode"]
    l, success, message = mybpPixiv.get_illust_ranking(mode=mode)
    return pack_json_data(l, success, message)
