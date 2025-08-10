from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import User
from database import get_db
from security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users")

@router.post("/signup")
def signup(user: User, db: Session = Depends(get_db)):
    user.hashed_password = hash_password(user.hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
