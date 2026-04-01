import jwt
from datetime import datetime
from app.db.config import settings
from app.exceptions.jwt_exceptions import JWTError


class AuthHandler(object):

    @staticmethod
    async def sign_jwt(user_id: int):
        payload = {
            "user_id": user_id,
            "exp": datetime.now() + settings.EXP_AT
        }

        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        return token

    @staticmethod
    async def decode_jwt(token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithm=settings.JWT_ALGORITHM
            )
            if decoded_token["exp"] >= datetime.now().timestamp():
                return decoded_token
            return None
        except Exception as e:
            raise JWTError(detail=f"Auth failed: {str(e)}")
