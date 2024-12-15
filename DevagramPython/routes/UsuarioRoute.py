import os
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, Body

from middleware.JWTmiddleware import verificar_token
from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from services.AuthService import decodificar_token_jwt
from services.UsuarioService import UsuarioService

router = APIRouter()


usuarioService = UsuarioService()


@router.post("/", response_description="Rota para criar um novo usuário")
async def rota_criar_usuario(file: UploadFile, usuario: UsuarioCriarModel = Depends(UsuarioCriarModel)):
    try:
        caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}.jpg'

        with open(caminho_foto, 'wb+') as arquivo:
            arquivo.write(file.file.read())

        resultado = await usuarioService.registrar_usuario(usuario, caminho_foto)

        os.remove(caminho_foto)

        if not resultado['status'] == 201:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

        return resultado
    except Exception as error:
        raise error


@router.get(
    "/me",
    response_description="Rota de Busca de informações do usuario logado",
    dependencies=[Depends(verificar_token)]
)
async def buscar_info_usuario_logado(authorization: str = Header(default='')):
    try:

        token = authorization.split(" ")[1]
        payload = decodificar_token_jwt(token)
        resultado = await usuarioService.buscar_usuario_logado(payload["usuario_id"])
        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

        return resultado
    except Exception as error:
        raise error


@router.put(
    "/me",
    response_description="Rota para atualizar as informações do usuario logado",
    dependencies=[Depends(verificar_token)]
)
async def atualizar_usuario_logado(
        authorization: str = Header(default=''),
        usuario_atualizar: UsuarioAtualizarModel = Body(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decodificar_token_jwt(token)
        resultado = await usuarioService.atualizar_usuario_logado(payload["id"], usuario_atualizar)
        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

        return resultado
    except Exception as error:
        print(error)
        raise error
