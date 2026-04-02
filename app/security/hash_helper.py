from bcrypt import checkpw, hashpw, gensalt


class HashHelper(object):

    @staticmethod
    async def verify_password(plain_password: str, hash_password: str):

        if checkpw(plain_password.encode(), hash_password.encode()):
            return True
        else:
            return False

    @staticmethod
    async def get_password_hash(plain_password: str):
        return hashpw(
            plain_password.encode(),
            gensalt()
        ).decode()
