from typing import Any

from pydantic import BaseModel


class Ret(BaseModel):
    code: int
    msg: str
    data: Any

    def __init__(self, code: int, msg: str, data: Any):
        super().__init__(code=code, msg=msg, data=data)

    @classmethod
    def success(cls, msg: str, data: Any = None):
        return cls(code=200, msg=msg, data=data)

    @classmethod
    def fail(cls, msg: str, data: Any = None):
        return cls(code=400, msg=msg, data=data)

    @classmethod
    def error(cls, msg: str, data: Any = None):
        return cls(code=500, msg=msg, data=data)


class UserToken(BaseModel):
    code: int
    access_token: str
    refresh_token: str
    token_type: str

    def __init__(self, access_token: str, refresh_token: str, token_type: str):
        super().__init__(
            code=200,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
        )


class LoginRet(Ret):
    data: UserToken
