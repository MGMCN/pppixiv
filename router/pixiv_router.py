from flask import Blueprint, request

pixiv_router = Blueprint('pixiv_router', __name__)

# Not graceful
mybpPixiv = None


def router_set_pixiv_api(api):
    global mybpPixiv
    mybpPixiv = api


def pack_json_data(l, success, message) -> dict:
    if success:
        json = {"status": 1, "message": "Get success! %s" % message, "list": l}
    else:
        json = {"status": 0, "message": "Get error... %s" % message, "list": {}}
    return json


@pixiv_router.route('/getIllustListByUid', methods=["POST"])
def getIllustListByUid():
    # Get uid from posted json
    uid = request.form["uid"]
    l, success, message = mybpPixiv.get_illust_list_by_uid(uid=uid)
    return pack_json_data(l, success, message)


@pixiv_router.route('/getTrendingTags', methods=["GET"])
def getTrendingTags():
    l, success, message = mybpPixiv.get_trending_tags()
    return pack_json_data(l, success, message)


@pixiv_router.route('/getIllustRanking', methods=["POST"])
def getIllustRanking():
    # Get mode from posted json
    mode = request.form["mode"]
    l, success, message = mybpPixiv.get_illust_ranking(mode=mode)
    return pack_json_data(l, success, message)


@pixiv_router.route('/get_illust_url', methods=["POST"])
def get_illust_url():
    # Get mode from posted json
    illust_id = request.form["illust_id"]
    l, success, message = mybpPixiv.get_illust_url(illust_id=illust_id)
    return pack_json_data(l, success, message)
