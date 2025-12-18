from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemes.user import LoginRequest, LoginResponse, UserResponse, UserCreate
from app.models.user import User
from app.database.core import get_db
from passlib.context import CryptContext

router = APIRouter(prefix="/api/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return user info"""
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пароль неверный"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не найден"
        )
    
    return LoginResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        message="Вход выполнен успешно!"
    )

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register new user (admin only in production)"""
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Имя пользователя занято"
        )
    
    password = user_data.password

# ВАЛИДАЦИЯ ПАРОЛЯ
    if len(user_data.password) < 6:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Пароль должен содержать не менее 6 символов"
    )

    if len(user_data.password) > 15:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Пароль должен содержать не более 15 символов"
    )

    if not any(c.isupper() for c in user_data.password):
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Пароль должен содержать хотя бы одну заглавную букву"
    )

    if not any(c.islower() for c in user_data.password):
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Пароль должен содержать хотя бы одну строчную букву"
    )

    if not any(c.isdigit() for c in user_data.password):
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Пароль должен содержать хотя бы одну цифру"
    )

    if ' ' in user_data.password:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Пароль не должен содержать пробелы"
    )

# Валидация логина
    if len(user_data.username) < 6:
       raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Логин должен содержать не менее 6 символов"
    )

    if len(user_data.username) > 15:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Логин должен содержать не более 15 символов"
        )

# Проверка наличия символа @
    if '@' not in user_data.username:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Логин должен быть в формате email (содержать @)"
    )

# Проверка на пробелы
    if ' ' in user_data.username:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Логин не должен содержать пробелы"
    )

# Проверка полного имени
    if len(user_data.full_name) < 6:
       raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Имя должно содержать не менее 6 символов"
    )

    if len(user_data.full_name) > 15:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Имя должно содержать не более 15 символов"
        )
        
    new_user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse.from_orm(new_user)
