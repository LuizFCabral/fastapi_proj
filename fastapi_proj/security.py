from pwdlib import PasswordHash
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode

pwd_content = PasswordHash.recommended()

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MIN = 30


def get_password_hash(password: str):
    return pwd_content.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_content.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MIN
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
