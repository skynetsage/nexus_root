from passlib.context import CryptContext

CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return CryptContext.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return CryptContext.verify(plain_password, hashed_password)
