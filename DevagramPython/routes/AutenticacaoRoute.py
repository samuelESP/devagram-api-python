from fastapi import APIRouter, Body, HTTPException
from models.UsuarioModel import UsuarioLoginModel
from services.AuthService import login_service

router = APIRouter()


@router.post('/login')
async def login(usuario: UsuarioLoginModel = Body(...)):
    resultado = await login_service(usuario)

    if not resultado['status'] == 200:
        raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

    del resultado["dados"]["senha"]

    return resultado
