from .base import BaseRouter
from flask import Blueprint, request, render_template


def pack_json_data(l, success, message) -> dict:
    if success:
        json = {"status": 1, "message": f"Get success! {message}", "list": l}
    else:
        json = {"status": 0, "message": f"Get error... {message}", "list": {}}
    return json


class pixivServiceRouter(BaseRouter):

    def __init__(self, router_name, service_api):
        super().__init__(router_name=router_name)
        self.router = Blueprint(router_name, __name__)
        self.service_api = service_api
        self.register_routes()

    def register_routes(self):
        api = self.service_api

        @self.router.route('/dashboard', methods=["GET"])
        def getDashBoard():
            return render_template("html/index.html")

        @self.router.route('/getIllustListByUid', methods=["POST"])
        def getIllustListByUid():
            # Get uid from posted json
            uid = request.form["uid"]
            l, success, message = api.get_illust_list_by_uid(uid=uid)
            return pack_json_data(l, success, message)

        @self.router.route('/getTrendingTags', methods=["GET"])
        def getTrendingTags():
            l, success, message = api.get_trending_tags()
            return pack_json_data(l, success, message)

        @self.router.route('/getIllustRanking', methods=["POST"])
        def getIllustRanking():
            # Get mode from posted json
            mode = request.form["mode"]
            l, success, message = api.get_illust_ranking(mode=mode)
            return pack_json_data(l, success, message)

        @self.router.route('/getIllustDownloadUrl', methods=["POST"])
        def getIllustDownloadUrl():
            # Get illust_id from posted json
            illust_id = request.form["illust_id"]
            l, success, message = api.get_illust_download_url(illust_id=illust_id)
            return pack_json_data(l, success, message)

        @self.router.route('/download', methods=["POST"])
        def downloadIllust():
            iid = request.form["id"]
            url = request.form["download_url"]
            title = request.form["title"]
            success, msg = api.download_illust(iid=iid, url=url, file_name=title)
            return pack_json_data([], success, msg)
