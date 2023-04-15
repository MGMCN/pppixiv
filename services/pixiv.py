import sched
import threading
import time
from typing import Callable, List, Tuple, Union

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

    def __init__(self, service_name: str,
                 username: str,
                 password: str,
                 retry: int = 5,
                 interval: int = 3599,):
        super().__init__(service_name=service_name)
        self._pixivUsername = username
        self._pixivPassword = password
        # Init pixiv api
        self.pixivTokenApi = GetPixivToken()
        self.pixivApi = pixiv.AppPixivAPI()
        self.token = None
        self.retry = retry
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.interval = interval

    def _retry_on_failure(self, func: Callable, *args, **kwargs) -> Union[None, bool, str]:
        retries_count = 0
        result = None
        while retries_count < self.retry:
            try:
                result = func(*args, **kwargs)
                break
            except (ValueError, pixiv.utils.PixivError) as e:
                self.logger.debug(f"Error occurred in {func.__name__}: {str(e)}")
                time.sleep(0.5)
                retries_count += 1

        return result

    def get_token(self) -> bool:
        def login():
            res = self.pixivTokenApi.login(
                headless=True, username=self._pixivUsername, password=self._pixivPassword
            )
            self.token = res["refresh_token"]
            self.logger.debug(f"get token -> {self.token}")

        self._retry_on_failure(login)

        return self.token is not None


    def refresh_token(self) -> bool:
        def refresh():
            self.token = self.pixivTokenApi.refresh(
                refresh_token=self.token)["refresh_token"]
            self.logger.debug(f"Token refreshed successfully! -> {self.token}")

        self._retry_on_failure(refresh)

        return self.token is not None

    def authentication(self) -> bool:
        def auth():
            self.pixivApi.auth(refresh_token=self.token)
            self.logger.debug("Authentication success!")

        def reset_token():
            self.logger.debug("The token has expired and needs to be reset!")
            self.refresh_token()

        while True:
            try:
                self._retry_on_failure(auth)
                return True
            except pixiv.utils.PixivError:
                reset_token()

    def get_illust_list_by_uid(self, uid) -> (list, bool, str):
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
                self.logger.debug("uid does not exist!")
                break
            for item in illusts:
                # Title encoding type Unicode
                l.append({
                    "title": item["title"],
                    "url": pack_illust_url(item["id"]),
                })
                self.logger.debug(f"Parse item[id] -> {item['id']}")
            if res["next_url"] is None:
                break
            offset = self.pixivApi.parse_qs(res["next_url"])["offset"]

        return l, success, msg

    def get_illust_ranking(self, mode="day", offset=0) -> (list, bool, str):
        success = True
        msg = None

        l = []

        # day, week, month, day_male, day_female, week_original, week_rookie, day_manga
        res = self.pixivApi.illust_ranking(mode=mode, offset=offset)

        illusts = res["illusts"]
        if len(illusts) == 0:
            success = False
            msg = "Ranking retrieval failed!"
            self.logger.debug("Ranking retrieval failed!")
        for item in illusts:
            # Title encoding type Unicode
            l.append({
                "title": item["title"],
                "url": pack_illust_url(item["id"]),
            })
            self.logger.debug(f"Parse item[id] -> {item['id']}")
        return l, success, msg

    def get_trending_tags(self) -> (list, bool, str):
        success = True
        msg = None

        l = []

        res = self.pixivApi.trending_tags_illust()

        tags = res["trend_tags"]
        if len(tags) == 0:
            success = False
            msg = "Trend tags do not exist!"
            self.logger.debug("Trend tags do not exist!")
        for item in tags:
            # Title encoding type Unicode
            l.append({
                "tag": item["tag"],
                "translated_tag": item["translated_name"],
            })
            self.logger.debug(f"Parse item[tag] -> {item['tag']}")
        return l, success, msg


    def get_illust_url(self, illust_id: Union[int, str]) -> (list, bool, str):
        success = True
        msg = None

        l = []

        if not isinstance(illust_id, int):
            illust_id = int(illust_id)

        res = self.pixivApi.illust_detail(illust_id)

        illust = res["illust"]
        if len(illust) == 0:
            success = False
            msg = "Illustration do not exist!"
            self.logger.debug("Illustration do not exist!")
        # Title encoding type Unicode
        l.append({
            "illust_id": illust["id"],
            "image_url": illust["image_urls"]["large"],
        })
        self.logger.debug(f"Parse item[illust_id] -> {illust['id']}")
        return l, success, msg

    def start_pixiv_session(self) -> bool:
        if not self.get_token():
            raise Exception('Get token error!')
        if not self.authentication():
            raise Exception('Authentication failed!')
        # Not graceful...
        self.scheduler.enter(self.interval, 0, self.run_refresh_token_task)
        t = threading.Thread(target=self.scheduler.run)
        t.start()

        # Maybe we don't need this?
        return True

    def run_refresh_token_task(self) -> bool:
        if not self.refresh_token():
            raise Exception('Refresh token error!')
        if not self.authentication():
            raise Exception('Authentication failed!')
        # Will this scheduler resetting impact the performance after a long time?
        self.scheduler.enter(self.interval, 0, self.run_refresh_token_task)

        return True
