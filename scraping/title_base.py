from abc import ABC, abstractmethod

class TitleStrategies(ABC):

    @abstractmethod
    def db_setting(self, setting):
        pass

    @abstractmethod
    def contains_title(self, title, markup, url):
        pass
