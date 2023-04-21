from .base import BaseParser


def pack_illust_url(uid) -> str:
    return f"https://www.pixiv.net/artworks/{uid}"


class IllustParser(BaseParser):

    def parse(self, data):
        result = []
        for item in data:
            result.append({
                "title": item["title"],
                "url": pack_illust_url(item["id"]),
                "download_url": item["image_urls"]["large"],
            })
            self.logger.debug(f"Parse item[id] -> {item['id']}")
        return result
