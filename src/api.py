from typing import Dict, List, Optional, Tuple, Union
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User, Repository
from .schemas import UserCreate, UserLogin, RepositoryCreate, RepositoryResponse
import requests

ENDPOINT = "https://api.templatehub.org"

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/api/")
async def root():
    return {"message": "Welcome to the TemplateHub API"}

@app.post("/api/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not user.verify_password(user_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = user.create_token()
    return {"username": user.username, "token": token}

@app.post("/api/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Implement token invalidation if needed
    return {"message": "Successfully logged out"}

@app.get("/api/whoami")
async def whoami(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    return {
        "username": user.username,
        "token": token,
        "orgs": user.organizations
    }

@app.post("/api/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user_data.username,
        password_hash=user_data.password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User successfully registered"}

@app.post("/api/repos/init")
async def init_repo(
    repo_data: RepositoryCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    
    new_repo = Repository(
        name=repo_data.name,
        description=repo_data.description,
        type=repo_data.type,
        org=repo_data.org,
        private=repo_data.private,
        status_lfs=repo_data.status_lfs,
        owner_id=user.id
    )
    
    db.add(new_repo)
    db.commit()
    db.refresh(new_repo)
    
    return RepositoryResponse.from_orm(new_repo)

@app.delete("/api/repos/drop")
async def drop_repo(
    repo_name: str,
    org: Optional[str] = None,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    repo = db.query(Repository).filter(
        Repository.name == repo_name,
        Repository.org == org,
        Repository.owner_id == user.id
    ).first()
    
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    db.delete(repo)
    db.commit()
    
    return {"message": "Repository successfully deleted"}

def get_current_user(token: str, db: Session):
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user