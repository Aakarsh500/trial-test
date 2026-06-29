from fastapi import FastAPI, HTTPException, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt, JWTError
import crud
import models
import schemas
import security
from database import engine, SessionLocal, Base

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    token_cookie = request.cookies.get("access_token")
    if not token_cookie or not token_cookie.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = token_cookie.split(" ")[1]
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = security.create_access_token(data={"sub": user.email})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="lax",
        secure=True
    )
    return {"message": "Session initialized successfully"}

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user_from_cookie)):
    return current_user

@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Session cleared successfully"}
