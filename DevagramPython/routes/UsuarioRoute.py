import os
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, Form, File

from middleware.JWTmiddleware import verificar_token
from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from services.AuthService import AuthService
from services.UsuarioService import UsuarioService

router = APIRouter()

authService = AuthService()
usuarioService = UsuarioService()


@router.post("/", response_description="Rota para criar um novo usuário")
async def rota_criar_usuario(nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    file: UploadFile = File(...)):
    try:
        caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}.jpg'

        with open(caminho_foto, 'wb+') as arquivo:
            arquivo.write(file.file.read())
        usuario = UsuarioCriarModel(nome=nome, email=email, senha=senha)
        resultado = await usuarioService.registrar_usuario(usuario, caminho_foto)
        os.remove(caminho_foto)

        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

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

        usuario_logado = await authService.buscar_usuario_logado(authorization)
        resultado = await usuarioService.buscar_usuario(usuario_logado.id)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

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
        nome: str = Form(...),
        email: str = Form(...),
        senha: str = Form(...),
        foto: UploadFile = File(None)):
    try:
        usuario_logado = await authService.buscar_usuario_logado(authorization)
        caminho_foto = None
        if foto:
            caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}.jpg'
            with open(caminho_foto, 'wb+') as arquivo:
                arquivo.write(foto.file.read())
        usuario_atualizar = UsuarioAtualizarModel(
            nome=nome,
            email=email,
            senha=senha,
            foto=foto
        )

        resultado = await usuarioService.atualizar_usuario_logado(usuario_logado.id, usuario_atualizar)

        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as error:
        print(error)
        raise error


@router.put(
    '/seguir/{usuario_id}',
    response_description="Rota para follow/unfollow em um usuário.",
    dependencies=[Depends(verificar_token)]
)
async def follow_unfollow_usuario(usuario_id: str, Authorization: str = Header(default='')):
    usuario_logado = await authService.buscar_usuario_logado(Authorization)
    resultado = await usuarioService.follow_unfollow_usuario(usuario_logado.id, usuario_id)

    if not resultado.status == 201:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado


@router.get(
    '/',
    response_description='Rota para listar todos usuários.',
    dependencies=[Depends(verificar_token)]
    )
async def listar_usuarios(nome: str):
    try:
        resultado = await usuarioService.listar_usuarios(nome)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro


@router.get(
    "/{usuario_id}",
    response_description="Rota de Busca de informações do usuario logado",
    dependencies=[Depends(verificar_token)]
)
async def buscar_info_usuario_logado(usuario_id: str):
    try:
        resultado = await usuarioService.buscar_usuario(usuario_id)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as error:
        raise error

