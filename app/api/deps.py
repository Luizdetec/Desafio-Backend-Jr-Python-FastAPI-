from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.infrastructure.security.jwt_handler import SECRET_KEY, ALGORITHM
from app.api.response_handler import error_response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class CustomHTTPException(HTTPException):
    """Exception customizada que retorna nosso formato de erro"""
    def __init__(self, status_code: int, message: str, code: str):
        self.status_code = status_code
        self.message = message
        self.code = code
        super().__init__(status_code=status_code)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise CustomHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Could not validate credentials",
                code="UNAUTHORIZED"
            )
        return {"username": username, "role": role}
    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid or expired token",
            code="UNAUTHORIZED"
        )


def RoleChecker(allowed_roles: list):
    async def _role_checker(user: dict = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise CustomHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Only admin can perform this action",
                code="FORBIDDEN"
            )
        return user

    return _role_checker