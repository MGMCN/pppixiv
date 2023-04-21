from .base import BaseParser
from .tag import TagParser
from .illust import IllustParser


class ParserFactory:
    @staticmethod
    def create_parser(parser_type) -> BaseParser:
        if parser_type == "tags":
            return TagParser()
        elif parser_type == "illusts":
            return IllustParser()
        else:
            return None
