import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

SECRET_KEY = os.getenv('SECRET_KEY')
if SECRET_KEY is None:
    raise RuntimeError("SECRET_KEY environment variable is not set")
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes={"user": "Acesso como usuário normal", "public": "Acesso via API Key"}
)

def create_access_token(data: dict, scope: str, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    to_encode.update({"scope": scope})
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return encoded_jwt

def get_current_user(
    security_scopes: SecurityScopes, 
    token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        username: Optional[str] = payload.get("sub")
        token_scope: Optional[str] = payload.get("scope")
        token_role: Optional[str] = payload.get("role")

        if username is None or token_scope is None or token_role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if security_scopes.scopes:
        if token_scope not in security_scopes.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permissão insuficiente: requer um dos scopes '{security_scopes.scope_str}', mas o token tem scope '{token_scope}'",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return payload

def get_current_admin(current_user: dict = Security(get_current_user, scopes=["user"])):
    user_role = current_user.get("role")

    if user_role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de Admin ou Super Admin."
        )
        
    return current_user

def get_current_super_admin(current_user: dict = Security(get_current_user, scopes=["user"])):
    user_role = current_user.get("role")

    if user_role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de Super Admin."
        )
        
    return current_user