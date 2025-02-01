from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import Response
from . import schemas as sm
from . import services as ss
from .auth import create_access_token, get_current_user_id
from ..database import SessionDep

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/")
async def register_user(user_registration: sm.UserRegistration, session: SessionDep) -> dict:
    already_exists = await ss.is_user_already_exist(
        session=session,
        phone_number=user_registration.phone_number,
        email=user_registration.email
    )
    if already_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_id = await ss.create_user(
        name=user_registration.name,
        phone_number=user_registration.phone_number,
        email=user_registration.email,
        password=user_registration.password,
        is_admin=False,
        session=session
    )
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_credential: sm.CredentialUserAuth, session: SessionDep):
    credential_type = user_credential.get_credential_type()
    phone_number = ''
    email = ''
    if credential_type == 'email':
        email = user_credential.user_credential
    elif credential_type == 'phone_number':
        phone_number = user_credential.user_credential
    user = await ss.login_user(
        session=session,
        phone_number=phone_number,
        email=email,
        password=user_credential.password,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль'
        )
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@router.get("/me/")
async def get_me(session: SessionDep, user_id: int = Depends(get_current_user_id)):
    user = await ss.get_user_by_id(session, user_id)
    return {'id': user_id, 'name': user.name, 'is_admin': user.is_admin}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
