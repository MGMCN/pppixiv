from .base import BaseParser


class TagParser(BaseParser):

    def parse(self, data):
        result = []
        for item in data:
            result.append({
                "tag": item["tag"],
                "translated_tag": item["translated_name"],
            })
            self.logger.debug(f"Parse item[tag] -> {item['tag']}")
        return result
