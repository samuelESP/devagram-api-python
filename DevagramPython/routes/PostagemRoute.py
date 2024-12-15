import os
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile

from middleware.JWTmiddleware import verificar_token
from models.PostagemModel import PostagemCriarModel
from models.UsuarioModel import UsuarioCriarModel
from services.AuthService import decodificar_token_jwt


router = APIRouter()


@router.post("/", response_description="Rota para criar um novo post")
async def rota_criar_postagem(file: UploadFile, usuario: PostagemCriarModel = Depends(PostagemCriarModel)):
    try:

        caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}.jpg'

        with open(caminho_foto, 'wb+') as arquivo:
            arquivo.write(file.file.read())

        #resultado = await registrar_usuario(usuario, caminho_foto)

        os.remove(caminho_foto)
    except Exception as error:
        raise error


@router.get(
    "/",
    response_description="Rota par listar as postagens",
    dependencies=[Depends(verificar_token)]
)
async def buscar_info_usuario_logado(Authorization: str = Header(default='')):
    try:

        return {
            'try': "teste"
        }

    except Exception as error:
        raise error