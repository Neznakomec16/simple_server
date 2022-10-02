from fastapi import HTTPException


class TokenExpiredError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Token expired")


class UserDoesNotExistsHTTPError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User with this username noes not exists")
