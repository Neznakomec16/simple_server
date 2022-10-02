class AuthServerError(Exception):
    pass


class EnvFileNotFound(AuthServerError):
    pass
