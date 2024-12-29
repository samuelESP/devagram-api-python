from typing import List

from fastapi import UploadFile
from pydantic import BaseModel, Field
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()

class PostagemModel(BaseModel):
    id: str = Field(...)
    usuario: str = Field(...)
    foto: str = Field(...)
    legenda: str = Field(...)
    data: str = Field(...)
    curtidas: int = Field(...)
    comentarios: List = Field(...)

    class Config:
        schema_extra = {
            "postagem": {
                "id": "string",
                "foto": "string",
                "legenda": "string",
                "data": "date",
                "curtidas": "int",
                "comentarios": "list"
            }
        }


@decoratorUtil.form_body
class PostagemCriarModel(BaseModel):
    foto: UploadFile = Field(...)
    legenda: str = Field(...)

    class Config:
        schema_extra = {
            "postagem": {
                "foto": "string",
                "legenda": "string",
            }
        }
