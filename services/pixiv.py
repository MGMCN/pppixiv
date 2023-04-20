import random
import sched
import threading
import time
import re

import pixivpy3 as pixiv
from gppt import GetPixivToken
from .base import BaseService


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def pack_illust_url(uid) -> str:
    return f"https://www.pixiv.net/artworks/{uid}"


@singleton
class Pixiv(BaseService):

    def __init__(self, service_name, username, password, retry=5, interval=3599):
        super().__init__(service_name=service_name)
        self.pixivUsername = username
        self.pixivPassword = password
        # Init pixiv api
        self.pixivTokenApi = GetPixivToken()
        self.pixivApi = pixiv.AppPixivAPI()
        self.token = None
        self.retry = retry
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.interval = interval

    def get_token(self) -> bool:
        success = True

        retries_count = 0
        while retries_count < self.retry:
            try:
                res = self.pixivTokenApi.login(headless=True, username=self.pixivUsername, password=self.pixivPassword)
                self.token = res["refresh_token"]
                self.logger.debug(f"get token -> {self.token}")
                break
            except ValueError:
                self.logger.debug("getToken error!")
            time.sleep(0.5)
            retries_count += 1

        if self.token is None:
            success = False
        return success

    def refresh_token(self) -> bool:
        refreshed = False

        try:
            self.token = self.pixivTokenApi.refresh(refresh_token=self.token)["refresh_token"]
            refreshed = True
            self.logger.debug(f"Token refreshed successfully! -> {self.token}")
        except ValueError:
            self.logger.debug("Get error when refreshing the token!")

        return refreshed

    def authentication(self) -> bool:
        success = True

        retryCount = 0
        while retryCount < self.retry:
            try:
                self.pixivApi.auth(refresh_token=self.token)
                success = True
                self.logger.debug("Authentication success!")
                break
            except pixiv.utils.PixivError:
                # Maybe we do not need this?
                self.logger.debug("The token has expired and needs to be reset!")
                success = self.refresh_token()
            retryCount += 1

        return success

    def get_illust_list_by_uid(self, uid) -> (list, bool, str):
        success = True
        msg = None

        offset = 0

        l = []

        while True:
            res = self.pixivApi.user_illusts(uid, type="illust", offset=offset)

            if res.illusts is not None:
                illusts = res["illusts"]
                if len(illusts) == 0:
                    if len(l) == 0:
                        success = False
                        msg = "Get illusts error!"
                        self.logger.debug(msg)
                    break
                for item in illusts:
                    # Title encoding type Unicode
                    l.append({
                        "title": item["title"],
                        "url": pack_illust_url(item["id"]),
                        "download_url": item["image_urls"]["large"],
                    })
                    self.logger.debug(f"Parse item[id] -> {item['id']}")
                if res["next_url"] is None:
                    break
                offset = self.pixivApi.parse_qs(res["next_url"])["offset"]
            else:
                success = False
                msg = f"{uid} do not exist!"
                self.logger.debug(msg)
                break

        return l, success, msg

    def get_illust_ranking(self, mode="day", offset=0) -> (list, bool, str):
        success = True
        msg = None

        l = []

        # day, week, month, day_male, day_female, week_original, week_rookie, day_manga
        res = self.pixivApi.illust_ranking(mode=mode, offset=offset)

        if res.illusts is not None:
            illusts = res['illusts']
            if len(illusts) == 0:
                success = False
                msg = "Ranking retrieval failed!"
                self.logger.debug(msg)
            for item in illusts:
                # Title encoding type Unicode
                l.append({
                    "title": item["title"],
                    "url": pack_illust_url(item["id"]),
                    "download_url": item["image_urls"]["large"],
                })
                self.logger.debug(f"Parse item[id] -> {item['id']}")
        else:
            success = False
            msg = f"{mode} do not exist!"
            self.logger.debug(msg)
        return l, success, msg

    def get_trending_tags(self) -> (list, bool, str):
        success = True
        msg = None

        l = []

        res = self.pixivApi.trending_tags_illust()

        if res.trend_tags is not None:
            tags = res["trend_tags"]
            if len(tags) == 0:
                success = False
                msg = "Get trend tags error!"
                self.logger.debug(msg)
            for item in tags:
                # Title encoding type Unicode
                l.append({
                    "tag": item["tag"],
                    "translated_tag": item["translated_name"],
                })
                self.logger.debug(f"Parse item[tag] -> {item['tag']}")
        else:
            success = False
            msg = "Trend tags do not exist!"
            self.logger.debug(msg)
        return l, success, msg

    def get_illust_download_url(self, illust_id) -> (list, bool, str):
        success = True
        msg = None

        l = []

        res = self.pixivApi.illust_detail(illust_id)

        if res.illust is not None:
            illust = res["illust"]
            if len(illust) == 0:
                success = False
                msg = "Get illustration error!"
                self.logger.debug(msg)
            else:
                # Title encoding type Unicode
                l.append({
                    "title": illust["title"],
                    "url": pack_illust_url(illust_id),
                    "download_url": illust["image_urls"]["large"],
                })
            self.logger.debug(f"Parse item[title] -> {illust['title']}")
        else:
            success = False
            msg = f"{illust_id} do not exist!"
            self.logger.debug(msg)
        return l, success, msg

    def download_illust(self, url, file_name) -> (bool, str):
        msg = "Download illust success!"
        try:
            file_name = re.sub(r'[^\w\-_.()]', '_', file_name)
            # 1/10000 Not graceful
            file_name += str(random.randint(1, 100))
            file_name += "_"
            file_name += str(random.randint(1, 100))
            file_name += "_"
            self.logger.debug(f"file_name -> {file_name}")
            success = self.pixivApi.download(url=url, path=".",
                                             fname="Illusts/" + file_name + ".jpg")
        except:
            # Exception type ?
            success = False
        if not success:
            msg = "Download illust failed!"
        self.logger.debug(msg)
        return success, msg

    def start_pixiv_session(self) -> (bool, str):
        msg = "lsp"
        success = self.get_token()
        if not success:
            # Do we really need raise exception? Or just retry and retry?
            msg = "Failed to get token, please check if you are blocked by pixiv or possibly because of reCAPTCHA v2 " \
                  "detection."
        else:
            success = self.authentication()
            if not success:
                msg = "For unknown reasons, the authentication failed."
            else:
                # Not graceful...
                self.scheduler.enter(self.interval, 0, self.run_refresh_token_task)
                t = threading.Thread(target=self.scheduler.run)
                t.start()
        return success, msg

    def run_refresh_token_task(self):
        success = False
        while not success:
            success = self.refresh_token()
            self.logger.debug(f"Token refreshed -> {success}")
        success = False
        while not success:
            success = self.authentication()
            self.logger.debug(f"Authentication success -> {success}")
        self.scheduler.enter(self.interval, 0, self.run_refresh_token_task)
