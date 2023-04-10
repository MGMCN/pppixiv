import sched
import threading
import time

import pixivpy3 as pixiv
from gppt import GetPixivToken


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def packIllustUrl(uid) -> str:
    return "https://www.pixiv.net/artworks/%s" % uid


@singleton
class Pixiv:

    def __init__(self, username, password, retry=5, interval=3599):
        self.pixivUsername = username
        self.pixivPassword = password
        # Init pixiv api
        self.pixivTokenApi = GetPixivToken()
        self.pixivApi = pixiv.AppPixivAPI()
        self.token = None
        self.retry = retry
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.interval = interval

    def getToken(self) -> bool:
        success = True

        retryCount = 0
        while retryCount < self.retry:
            try:
                res = self.pixivTokenApi.login(headless=True, username=self.pixivUsername, password=self.pixivPassword)
                self.token = res["refresh_token"]
                break
            except ValueError:
                print("getToken error!")
            time.sleep(0.5)
            retryCount += 1
        print(self.token)

        if self.token is None:
            success = False
        return success

    def refreshToken(self) -> bool:
        refreshed = False

        try:
            self.token = self.pixivTokenApi.refresh(refresh_token=self.token)["refresh_token"]
            print("Token refreshed successfully!")
            refreshed = True
        except ValueError:
            print("Get error when refreshing the token!")
        print(self.token)

        return refreshed

    def authentication(self) -> bool:
        success = True

        retryCount = 0
        while retryCount < self.retry:
            try:
                self.pixivApi.auth(refresh_token=self.token)
                success = True
                break
            except pixiv.utils.PixivError:
                print('The token has expired and needs to be reset!')
                success = self.refreshToken()
            retryCount += 1

        return success

    def parseResponse(self, res) -> (list, bool, str):
        success = True
        msg = ""

        l = []

        if res["illusts"] is None:
            success = False
            msg = "uid does not exist!"
        else:
            for item in res["illusts"]:
                # Title encoding type Unicode
                l.append({
                    "title": item["title"],
                    "url": packIllustUrl(item["id"]),
                })
        return l, success, msg

    def getIllustListByUid(self, uid) -> (list, bool, str):
        success = True
        msg = uid

        offset = 0

        l = []

        while True:
            res = self.pixivApi.user_illusts(uid, type="illust", offset=offset)
            illusts = res["illusts"]
            if len(illusts) == 0:
                success = False
                msg = "uid does not exist!"
                break
            for item in illusts:
                # Title encoding type Unicode
                l.append({
                    "title": item["title"],
                    "url": packIllustUrl(item["id"]),
                })
            if res["next_url"] is None:
                break
            offset = self.pixivApi.parse_qs(res["next_url"])["offset"]

        return l, success, msg

    def getIllustRanking(self, mode="day", offset=0) -> (list, bool, str):
        success = True
        msg = None

        l = []

        res = self.pixivApi.illust_ranking(mode=mode, offset=offset)

        illusts = res["illusts"]
        if len(illusts) == 0:
            success = False
            msg = "Ranking retrieval failed!"
        for item in illusts:
            # Title encoding type Unicode
            l.append({
                "title": item["title"],
                "url": packIllustUrl(item["id"]),
            })

        return l, success, msg

    def getTrendingTags(self) -> (list, bool, str):
        success = True
        msg = None

        l = []

        res = self.pixivApi.trending_tags_illust()

        tags = res["trend_tags"]
        if len(tags) == 0:
            success = False
            msg = "Trend tags do not exist!"
        for item in tags:
            # Title encoding type Unicode
            l.append({
                "tag": item["tag"],
                "translated_tag": item["translated_name"],
            })

        return l, success, msg

    # @staticmethod
    # def my_decorator(func):
    #     def wrapper(*args, **kwargs):
    #         success = True
    #         msg = None
    #         l = []
    #
    #         res = func(**kwargs)
    #
    #         keys = [*args]
    #         tags = res[keys[0]]
    #         if len(tags) == 0:
    #             success = False
    #             msg = "Trend tags do not exist!"
    #         for item in tags:
    #             # Title encoding type Unicode
    #             l.append({
    #                 "tag": item["tag"],
    #                 "translated_tag": item["translated_name"],
    #             })
    #
    #     return wrapper

    def startPixivSession(self) -> bool:
        success = self.getToken()
        if not success:
            # Do we really need raise exception ? Or just retry and retry ?
            raise Exception('Get token error!')
        success = self.authentication()
        if not success:
            raise Exception('Authentication failed!')
        # Not graceful...
        self.scheduler.enter(self.interval, 0, self.runRefreshTokenTask)
        t = threading.Thread(target=self.scheduler.run)
        t.start()
        return success

    def runRefreshTokenTask(self) -> bool:
        success = self.refreshToken()
        if not success:
            raise Exception('Refresh token error!')
        success = self.authentication()
        if not success:
            raise Exception('Authentication failed!')
        self.scheduler.enter(self.interval, 0, self.runRefreshTokenTask)

        # Maybe we don't need this ?
        return success
