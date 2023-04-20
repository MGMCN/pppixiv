from flask import Blueprint, request, render_template

pixiv_router = Blueprint('pixiv_router', __name__)

# Not graceful
mybpPixiv = None


def router_set_pixiv_api(api):
    global mybpPixiv
    mybpPixiv = api


def pack_json_data(l, success, message) -> dict:
    if success:
        json = {"status": 1, "message": f"Get success! {message}", "list": l}
    else:
        json = {"status": 0, "message": f"Get error... {message}", "list": {}}
    return json


@pixiv_router.route('/dashboard', methods=["GET"])
def getDashBoard():
    return render_template("html/index.html")


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


@pixiv_router.route('/getIllustDownloadUrl', methods=["POST"])
def getIllustDownloadUrl():
    # Get illust_id from posted json
    illust_id = request.form["illust_id"]
    l, success, message = mybpPixiv.get_illust_download_url(illust_id=illust_id)
    return pack_json_data(l, success, message)


@pixiv_router.route('/download', methods=["POST"])
def downloadIllust():
    url = request.form["download_url"]
    title = request.form["title"]
    success, msg = mybpPixiv.download_illust(url=url, file_name=title)
    return pack_json_data([], success, msg)
