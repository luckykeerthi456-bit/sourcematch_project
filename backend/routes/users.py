from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models import get_db, User, init_db
from ..schemas import UserCreate, UserOut
from ..auth import get_password_hash, create_access_token, verify_password
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        password_hash = get_password_hash(payload.password)
    except ValueError as e:
        # Friendly client error when password exceeds bcrypt's limit
        raise HTTPException(status_code=400, detail=str(e))

    user = User(email=payload.email, password_hash=password_hash, role=payload.role, full_name=payload.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "role": user.role, "full_name": user.full_name}}
