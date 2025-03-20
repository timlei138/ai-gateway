from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..services.auth import authenticate_user, create_access_token, get_current_user
from tortoise.exceptions import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB, UserLoginResponse

router = APIRouter(tags=["Authentication"], prefix="/auth")


@router.post("/login",response_model=UserLoginResponse,
             status_code=status.HTTP_200_OK,
             summary="用户登录",responses={
                 status.HTTP_401_UNAUTHORIZED: {
                     "description": "Incorrect username or password"
                 }
             })
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserInDB,
             status_code=status.HTTP_201_CREATED,
             summary="用户注册")
async def register_user(user_data: UserCreate):
    try:
        # 创建普通用户，默认角色为USER
        user = await User.create_user(
            username=user_data.username,
            password=user_data.password
        )
        return await UserInDB.from_tortoise_orm(user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名已存在"
        )

@router.get(
    "/me",
    response_model=UserInDB,
    summary="获取当前用户信息"
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return await UserInDB.from_tortoise_orm(current_user)


