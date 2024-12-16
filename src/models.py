from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base
import bcrypt
import jwt
from datetime import datetime, timedelta
from .database import engine

SECRET_KEY = "your-secret-key"  # Move this to environment variables in production

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    token = Column(String(255), unique=True, nullable=True)
    organizations = Column(String(255))  # Stored as comma-separated values
    
    repositories = relationship("Repository", back_populates="owner")

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def create_token(self) -> str:
        token = jwt.encode(
            {
                "sub": self.username,
                "exp": datetime.utcnow() + timedelta(days=1)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        self.token = token
        return token

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text)
    type = Column(String(50))
    org = Column(String(100), nullable=True)
    private = Column(Boolean, default=False)
    status_lfs = Column(Boolean, default=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="repositories") 

Base.metadata.create_all(bind=engine)