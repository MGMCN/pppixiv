import time

import pixivpy3 as pixiv
from gppt import GetPixivToken
import sched
import threading


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
        self.interval = interval  # 3300s

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
                    item["title"]: packIllustUrl(item["id"]),
                })
            if res["next_url"] is None:
                break
            offset = self.pixivApi.parse_qs(res["next_url"])["offset"]

        return l, success, msg

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
