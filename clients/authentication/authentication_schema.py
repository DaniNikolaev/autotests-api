from pydantic import BaseModel, Field, EmailStr

from tools.fakers import fake


class LoginRequestSchema(BaseModel):
    """
    Описание структуры запроса на аутентификацию.
    """
    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)


class TokenSchema(BaseModel):
    """
    Описание структуры аутентификационных токенов.
    """
    token_type: str = Field(alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class LoginResponseSchema(BaseModel):
    """
    Описание структуры ответа аутентификации.
    """
    token: TokenSchema


class RefreshRequestSchema(BaseModel):
    """
    Описание структуры запроса для обновления токена.
    """
    refresh_token: str = Field(alias="refreshToken", default_factory=fake.sentence)


class RefreshResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления токена.
    """
    token: TokenSchema
