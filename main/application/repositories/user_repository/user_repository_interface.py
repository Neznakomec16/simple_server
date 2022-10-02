from abc import ABC, abstractmethod

from main.application.repositories.user_repository.models import UserRecordWithPassword


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_user_by_username(self, username: str, raise_if_not_exists: bool = True) -> UserRecordWithPassword:
        ...

    @abstractmethod
    async def create_user(self, username: str, email: str, password: str) -> UserRecordWithPassword:
        ...

    @abstractmethod
    async def update_last_login(self, username: str) -> UserRecordWithPassword:
        ...

    @abstractmethod
    async def disable_user(self, username: str) -> UserRecordWithPassword:
        ...

    @abstractmethod
    async def get_user_by_email_or_username(
        self, username: str | None, email: str | None, raise_if_not_exists: bool = True
    ) -> UserRecordWithPassword | None:
        ...
