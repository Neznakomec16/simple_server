class PostgresUserRepositoryError(Exception):
    ...


class UserAlreadyExistsError(PostgresUserRepositoryError):
    ...


class UserDoesNotExistsError(PostgresUserRepositoryError):
    ...
