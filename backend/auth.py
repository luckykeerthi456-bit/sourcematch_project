from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from .models import get_db
from fastapi.security import OAuth2PasswordBearer
from .models import User
import os
import logging

SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# bcrypt has a 72-byte input limitation. We validate user-provided passwords
# and return a clear error instead of letting passlib/bcrypt raise a server 500.
MAX_BCRYPT_PASSWORD_BYTES = 72

# Prefer a pure-Python algorithm for development to avoid bcrypt binary issues.
# Keep bcrypt listed so existing bcrypt hashes still verify.
pwd_context = CryptContext(schemes=["sha256_crypt", "bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logger = logging.getLogger(__name__)


def _ensure_bcrypt_compatible(password: str) -> None:
    """Raise ValueError when password is longer than bcrypt's 72-byte limit.

    The message is intentionally user-friendly so the API can return a 400.
    """
    if not isinstance(password, str):
        # let passlib handle non-string inputs later (will fail safely)
        return
    b = password.encode("utf-8")
    if len(b) > MAX_BCRYPT_PASSWORD_BYTES:
        raise ValueError(
            f"Password is too long for bcrypt (max {MAX_BCRYPT_PASSWORD_BYTES} bytes). Please use a shorter password."
        )


def verify_password(plain, hashed):
    """Verify a password, but treat overly-long passwords as invalid credentials.

    Returning False for too-long passwords prevents a 500 and makes login a
    normal invalid-credential case.
    """
    try:
        if isinstance(plain, str) and len(plain.encode("utf-8")) > MAX_BCRYPT_PASSWORD_BYTES:
            # Too long: treat as invalid (don't attempt to call bcrypt which would error)
            logger.debug("Password provided to verify_password exceeds bcrypt byte limit; treating as invalid.")
            return False
        return pwd_context.verify(plain, hashed)
    except Exception:
        # Any verify error should be treated as a failed verification
        return False


def get_password_hash(password):
    # Use the configured pwd_context (sha256_crypt preferred in dev). If hashing
    # fails for any reason, raise a ValueError so routes can return HTTP 400.
    try:
        return pwd_context.hash(password)
    except Exception:
        logger.exception("password hashing failed; falling back prevented")
        raise ValueError(
            "Unable to hash password due to hashing backend error. Please check server hashing configuration."
        )


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_recruiter(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Dependency that returns current user if they are a recruiter, else raises 403."""
    user = get_current_user(token=token, db=db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    if getattr(user, "role", None) != "recruiter":
        raise HTTPException(status_code=403, detail="Recruiter role required")
    return user
