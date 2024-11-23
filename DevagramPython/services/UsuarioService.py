from models.UsuarioModel import UsuarioCriarModel
from repositories.UsuarioRepository import (
    criar_usuario,
    atualizar_usuario,
    listar_usuarios,
    buscar_usuario_email,
    deletar_usuario
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
            novo_usuario = await criar_usuario(usuario)
        return {
            "mensagem": f'Usuário cadastrado com sucesso!',
            "dados": novo_usuario,
            "status": 201
        }
    except Exception as error:
        return {
            "mensagem": "Erro interno no servidor",
            "dados": str(error),
            "status": 500
        }

