from injector import Injector, Module
from src.infra.mysql.db import session
from src.infra.mysql.repository.user import UserRepo
from src.domain.repository.user import IUserRepo

class DIModule(Module):
    def configure(self, binder):
        binder.bind(IUserRepo, to=UserRepo(session))

class InjectorManager:

    _injector = None

    @classmethod
    def get_injector(cls):
        if cls._injector is None:
            cls._injector = Injector(modules=[DIModule()])
        return cls._injector


def get_injector():
    return InjectorManager.get_injector()
