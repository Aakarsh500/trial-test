from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
import security

def create_user(db: Session, user: UserCreate):
    hashed_pwd = security.get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, user_data: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    db_user.name = user_data.name
    db_user.email = user_data.email
    db_user.hashed_password = security.get_password_hash(user_data.password)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user
