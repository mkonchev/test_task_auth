import jwt
from datetime import datetime
from app.db.config import settings
from app.exceptions.jwt_exceptions import JWTError


class AuthHandler(object):

    @staticmethod
    async def sign_jwt(user_id: int):
        exp_timestamp = datetime.now().timestamp() + settings.EXP_AT
        expire = datetime.fromtimestamp(exp_timestamp)
        payload = {
            "user_id": user_id,
            "exp": expire
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
                algorithms=[settings.JWT_ALGORITHM]
            )
            exp = decoded_token.get("exp")
            if exp and datetime.now().timestamp() > exp:
                return None
            return decoded_token
        except Exception as e:
            raise JWTError(detail=f"Auth failed: {str(e)}")
