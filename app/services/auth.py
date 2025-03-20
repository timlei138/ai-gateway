from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError, jwt
from tortoise.exceptions import DoesNotExist
from ..models.user import User
from ..config import settings
from ..schemas.user import UserInDB, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    expires_delta = timedelta(minutes=settings.Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.Settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.Settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    try:
        user = await User.get(username=username)
        if not user.verify_password(password):
            return None
        return user
    except DoesNotExist:
        user.hashed_password  # Dummy call for timing attack protection
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.Settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.Settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    try:
        user = await User.get(username=username)
    except DoesNotExist:
        raise credentials_exception
    return user


async def get_current_admin_user(
        current_user: User = Depends(get_current_user)
):
    if not current_user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    return current_user


async def login_user(form_data: OAuth2PasswordRequestForm):
    user = await User.filter(username=form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        return None

    # 检查强制密码修改
    # if user.force_password_change:
    #     raise ForcedPasswordChangeException()

    return {
        "access_token": create_access_token(data={"sub": str(user.id)}),
        "token_type": "bearer",
        "user": await UserInDB.from_tortoise_orm(user)
    }