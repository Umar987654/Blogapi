from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
from models import Post, User
from database import get_db
from jose import JWTError, jwt
from security import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/posts")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = db.exec(select(User).where(User.email == email)).first()
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/")
def create_post(post: Post, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post.owner_id = user.id
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    return db.exec(select(Post)).all()

@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}")
def update_post(post_id: int, updated: Post, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.get(Post, post_id)
    if not post or post.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    post.title = updated.title
    post.content = updated.content
    db.add(post)
    db.commit()
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.get(Post, post_id)
    if not post or post.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
