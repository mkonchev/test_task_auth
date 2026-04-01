from fastapi import HTTPException, status


class JWTError(HTTPException):
    def __init__(
        self,
        detail: str = "Authentication error",
        status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail)
