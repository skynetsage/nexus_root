# utils/auth_util.py

from passlib.context import CryptContext

# Configure the CryptContext with preferred hashing scheme
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)
