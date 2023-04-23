from .base import BaseParser
from .tag import TagParser
from .illust import IllustParser


class ParserFactory:
    @staticmethod
    def create_parser(parser_type) -> BaseParser:
        # Python version should be higher than or equal to 3.10
        match parser_type:
            case "tags":
                return TagParser()
            case "illusts":
                return IllustParser()
            case _:
                return None
