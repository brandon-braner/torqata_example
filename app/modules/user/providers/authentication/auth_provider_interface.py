from abc import ABCMeta, abstractmethod


class IAuthProvider(metaclass=ABCMeta):

    @abstractmethod
    def register(self, username: str, password: str):
        pass

    @abstractmethod
    def login(self, username: str, password: str):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def get_user(self, username: str):
        pass
