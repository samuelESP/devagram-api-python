from typing import List

from pydantic import BaseModel, Field

from models import UsuarioModel
from models.ComentarioModel import ComentarioModel


class PostagemModel(BaseModel):
    id: str = Field(...)
    usuario: UsuarioModel = Field(...)
    foto: str = Field(...)
    legenda: str = Field(...)
    data: str = Field(...)
    curtidas: int = Field(...)
    comentarios: List[ComentarioModel] = Field(...)

    class Config:
        schema_extra = {
            "postagem": {
                "id": "string",
                "foto": "string",
                "legenda": "string",
                "data": "date",
                "curtidas": "int",
                "comentarios": "List[comentarios]"
            }
        }



class PostagemCriarModel(BaseModel):
    usuario: UsuarioModel = Field(...)
    foto: str = Field(...)
    legenda: str = Field(...)

    class Config:
        schema_extra = {
            "postagem": {
                "usuario": "UsuarioModel",
                "foto": "string",
                "legenda": "string",
            }
        }