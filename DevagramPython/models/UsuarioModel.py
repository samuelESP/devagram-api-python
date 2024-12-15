from fastapi import Form, UploadFile
from pydantic import BaseModel, Field, EmailStr


class Usuariomodel(BaseModel):
    id: str = Field(...)
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "string",
                "email": "string",
                "senha": "string",
                "foto": "string"
            }
        }


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


@form_body
class UsuarioCriarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "string",
                "email": "string",
                "senha": "string",
            }
        }


class UsuarioLoginModel(BaseModel):
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "email": "string",
                "senha": "string",
            }
        }


@form_body
class UsuarioAtualizarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: UploadFile = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "string",
                "email": "string",
                "senha": "string",
            }
        }
