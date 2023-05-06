import random
import sched
import threading
import time
import re
import os
import pixivpy3 as pixiv
from gppt import GetPixivToken

from .base import BaseService
from .parser.parser_factory import ParserFactory


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Pixiv(BaseService):

    def __init__(self, service_name, gfw, username, password, retry=5, interval=3599):
        super().__init__(service_name=service_name)
        self.pixivUsername = username
        self.pixivPassword = password
        self.gfw = gfw
        # Init pixiv api
        self.pixivTokenApi = GetPixivToken()
        if not self.gfw:
            self.pixivApi = pixiv.AppPixivAPI()
        else:
            # For gfw users
            self.pixivApi = pixiv.ByPassSniApi()
            self.pixivApi.require_appapi_hosts()
            self.pixivApi.set_accept_language("en-us")  # necessary ?
        self.token = None
        self.retry = retry
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.interval = interval
        # Init parser
        self.tagParser = ParserFactory.create_parser("tags")
        self.illustParser = ParserFactory.create_parser("illusts")

    def set_logger(self, logger):
        super().set_logger(logger)
        self.tagParser.set_logger(logger)
        self.illustParser.set_logger(logger)

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
                # Not graceful but can fix the bug !
                if success and retryCount == 4:
                    success = False
            retryCount += 1

        return success

    def get_illust_list_by_uid(self, uid) -> (list, bool, str):
        success = True
        msg = "Get illusts success!"

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
                l.extend(self.illustParser.parse(illusts))
                if res["next_url"] is None:
                    break
                offset = self.pixivApi.parse_qs(res["next_url"])["offset"]
            else:
                if len(l) == 0:
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
            else:
                l.extend(self.illustParser.parse(illusts))
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
            else:
                l.extend(self.tagParser.parse(tags))
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
            l.extend(self.illustParser.parse([illust]))
        else:
            success = False
            msg = f"{illust_id} do not exist!"
            self.logger.debug(msg)
        return l, success, msg

    def download_illust(self, iid, url, file_name) -> (bool, str):
        # Not graceful
        try:
            file_name = re.sub(r'[^\w\-_.()]', '_', file_name)
            file_name = f"{file_name}_{iid}"
            count = 1
            temp = file_name
            while os.path.exists(f"./Illusts/{file_name}.jpg"):
                file_name = f"{temp}_{str(count)}"
                count += 1
            self.logger.debug(f"file_name -> {file_name}")
            success = self.pixivApi.download(url=url, path=".",
                                             fname="Illusts/" + file_name + ".jpg")
            msg = file_name + ".jpg"
        except:
            # Exception type ?
            success = False
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
