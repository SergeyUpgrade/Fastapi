from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.testing.pickleable import User
from starlette.responses import Response

from app.users.auth import get_password_hash, create_access_token, authenticate_user_email, \
    authenticate_user_phone_number
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.schemas import SUserRegister, CredentialUserAuth

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    user_dict['re_password'] = get_password_hash(user_data.re_password)
    await UsersDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_credential: CredentialUserAuth):
    user = None
    credential_type = user_credential.get_credential_type()
    if credential_type == 'email':
        user = await authenticate_user_email(
            email=user_credential.user_credential,
            password=user_credential.password
        )
    elif credential_type == 'phone_number':
        user = await authenticate_user_phone_number(
            phone_number=user_credential.user_credential,
            password=user_credential.password
        )
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
