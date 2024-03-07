from dotenv import load_dotenv
import os


class Config:
    def __init__(self):
        load_dotenv(verbose=True)
        self.config = {
            "port": None,
            "username": None,
            "password": None,
        }

    def load_dotenv(self):
        for key in self.config:
            self.config[key] = os.getenv(key)

    def get_config(self) -> dict:
        return self.config
