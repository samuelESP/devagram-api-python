from fastapi import APIRouter, HTTPException, Depends, Header

from middleware.JWTmiddleware import verificar_token
from models.UsuarioModel import UsuarioCriarModel
from services.AuthService import decodificar_token_jwt
from services.UsuarioService import (
    registrar_usuario,
    buscar_usuario_logado
)

router = APIRouter()


@router.post("/", response_description="Rota para criar um novo usuário")
async def rota_criar_usuario(usuario: UsuarioCriarModel):
    try:
        resultado = await registrar_usuario(usuario)

        if not resultado['status'] == 201:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

        return resultado
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@router.get(
    "/me",
    response_description="Rota de Busca de informações do usuario logado",
    dependencies=[Depends(verificar_token)]
)
async def buscar_info_usuario_logado(Authorization: str = Header(default='')):
    try:

        token = Authorization.split(" ")[1]
        payload = decodificar_token_jwt(token)
        resultado = await buscar_usuario_logado(payload["usuario_id"])
        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

        return resultado
    except:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
