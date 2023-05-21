from abc import ABC, abstractmethod


class Scraper(ABC):
    @abstractmethod
    def _run(self):
        pass

    @staticmethod
    @abstractmethod
    def get_df(self):
        pass
