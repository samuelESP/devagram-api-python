from models.UsuarioModel import UsuarioCriarModel
from repositories.UsuarioRepository import (
    criar_usuario,
    buscar_usuario_email,
    buscar_usuario
)


async def registrar_usuario(usuario: UsuarioCriarModel):
    try:
        usuario_encontrado = await buscar_usuario_email(usuario.email)

        if usuario_encontrado:
            return {
                "mensagem": f"{usuario.email} já cadastrado no nosso banco de dados",
                "dados": "",
                "status": 400
            }
        else:
            return {
                "mensagem": f'Usuário com id: {id} não foi encontrado',
                "dados": "",
                "status": 404
            }

    except Exception as error:
        return {
            "mensagem": "Erro interno no servidor",
            "dados": str(error),
            "status": 500
        }


async def buscar_usuario_logado(id: str):
    try:
        usuario_encontrado = await buscar_usuario(id)
        if usuario_encontrado:
            return {
                "mensagem": f"Usuario encontrado",
                "dados": usuario_encontrado,
                "status": 200
            }

        else:
            return {
                "mensagem": f"Usuario encontrado",
                "dados": usuario_encontrado,
                "status": 200
            }

    except Exception as error:
        print(error)
        return {
            "mensagem": "Erro interno no servidor",
            "dados": str(error),
            "status": 500
        }
