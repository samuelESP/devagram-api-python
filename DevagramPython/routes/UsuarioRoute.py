from fastapi import APIRouter, Body
router = APIRouter()


@router.post("/", response_description="Rota para criar um novo usuário")
async def rota_criar_usuario(usuario: dict = Body(...)):
    return {
        "mensagem": "Usuario cadastrado com sucesso"
    }
