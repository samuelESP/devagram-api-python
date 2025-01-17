from typing import List

from fastapi import UploadFile
from pydantic import BaseModel, Field, EmailStr
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


class Usuariomodel(BaseModel):
    id: str = Field(...)
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: str = Field(...)
    seguidores: List
    seguindo: List
    total_seguidores: int
    total_seguindo: int
    postagens: List
    total_postagem: int
    token: str

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "string",
                "email": "string",
                "senha": "string",
                "foto": "string",
                "seguidores": "List",
                "seguindo": "List"
            }
        }


@decoratorUtil.form_body
class UsuarioCriarModel(BaseModel):
    nome: str = Field(max_length=25, min_length=3)
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


@decoratorUtil.form_body
class UsuarioAtualizarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: UploadFile = None

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "usuario": {
                "nome": "string",
                "email": "string",
                "senha": "string",
            }
        }
