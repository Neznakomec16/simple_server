from fastapi import HTTPException


class UserAlreadyExistsError(HTTPException):
    pass
