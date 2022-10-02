import datetime

from asyncpg import Pool

from ..models import UserRecord, UserRecordWithPassword
from ..user_repository_interface import UserRepositoryInterface
from .exceptions import UserAlreadyExistsError, UserDoesNotExistsError


class PostgresUserRepository(UserRepositoryInterface):
    def __init__(self, conn: Pool):
        self._conn = conn

    async def _safe_fetchrow(self, query, *args):
        async with self._conn.acquire() as connection:
            async with connection.transaction():
                return await connection.fetchrow(query, *args)

    async def get_user_by_username(
        self, username: str, raise_if_not_exists: bool = True
    ) -> UserRecordWithPassword | None:

        result = await self._conn.fetchrow(
            """
            SELECT id, username, password, email, last_login, created_dt
            FROM users
            WHERE username=$1
            """,
            username,
        )
        if result is None:
            if raise_if_not_exists:
                raise UserDoesNotExistsError(f"User with {username=} does not exists")
            else:
                return None
        return UserRecordWithPassword(**result)

    async def get_user_by_email_or_username(
        self, username: str | None, email: str | None, raise_if_not_exists: bool = True
    ) -> UserRecordWithPassword | None:
        result = await self._conn.fetchrow(
            """
            SELECT id, username, password, email, last_login, created_dt
            FROM users
            WHERE username=$1 or email=$2
            """,
            username,
            email,
        )
        if result is None:
            if raise_if_not_exists:
                raise UserDoesNotExistsError(f"User with {username=} does not exists")
            else:
                return None
        return UserRecordWithPassword(**result)

    async def create_user(self, username: str, email: str, password: str) -> UserRecordWithPassword:
        user = await self.get_user_by_email_or_username(username, email, False)
        if user is not None:
            raise UserAlreadyExistsError(f"User with {username=} already exists")
        result = await self._safe_fetchrow(
            """
            INSERT INTO users(username, password, email, disabled)
            VALUES ($1, $2, $3, false)
            RETURNING id, username, password, email, last_login, created_dt, disabled
            """,
            username,
            password,
            email,
        )
        return UserRecordWithPassword(**result)

    async def update_last_login(self, username: str) -> UserRecordWithPassword:
        await self.get_user_by_username(username)  # Raises if username does not exist
        result = await self._conn.fetchrow(
            """
            UPDATE users
            SET last_login=$1
            WHERE username=$2
            RETURNING id, username, password, email, last_login, created_dt, disabled
            """,
            datetime.datetime.utcnow(),
            username,
        )
        return UserRecordWithPassword(**result)

    async def disable_user(self, username: str) -> UserRecordWithPassword:
        await self.get_user_by_username(username)  # Raises if username does not exist
        result = await self._conn.fetchrow(
            """
            UPDATE users
            SET disabled=true
            WHERE username=$1
            RETURNING id, username, password, email, last_login, created_dt, disabled
            """,
            username,
        )
        return UserRecordWithPassword(**result)
