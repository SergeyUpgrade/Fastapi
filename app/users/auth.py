from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone, time
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request

from app.config import get_auth_data, settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

        def verify_jwt(self, jwtoken: str) -> bool:
            isTokenValid: bool = False
            try:
                payload = decode_token(jwtoken)
            except:
                payload = None
            if payload:
                isTokenValid = True
            return isTokenValid
        async def __call__(self, request: Request):
            credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
            if credentials:
                if not credentials.scheme == "Bearer":
                    raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
                if not self.verify_jwt(credentials.credentials):
                    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
                return credentials.credentials
            else:
                raise HTTPException(status_code=403, detail="Invalid authorization code.")




def create_access_token(data: dict) -> dict:
    auth_data = get_auth_data()
    access_token_expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # Короткий срок
    access_token_payload = data.copy()
    access_token_payload.update({"exp": access_token_expire})
    access_token = jwt.encode(access_token_payload, auth_data['secret_key'], algorithm=auth_data['algorithm'])

    # Refresh Token
    refresh_token_expire = datetime.now(timezone.utc) + timedelta(days=30)  # Долгий срок
    refresh_token_payload = data.copy()
    refresh_token_payload.update({"exp": refresh_token_expire})
    refresh_token = jwt.encode(refresh_token_payload, auth_data['secret_key'], algorithm=auth_data['algorithm'])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


#def get_token(request: Request):
#    token = request.cookies.get('users_access_token')
#    if not token:
#        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
#    return token


#def decode_jwt(token: str) -> dict:
#    try:
#        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#        return decoded_token if decoded_token["expires"] >= time() else None
#    except:
#        return {}


def decode_token(token: str):
    auth_data = get_auth_data()
    try:
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    return int(user_id)
