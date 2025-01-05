from fastapi import APIRouter, HTTPException, Depends, Header, Body
from middleware.JWTmiddleware import verificar_token
from models.ComentarioModel import ComentarioCriarModel, ComentarioAtualizarModel
from models.PostagemModel import PostagemCriarModel
from services.AuthService import AuthService
from services.UsuarioService import UsuarioService
from services.PostagemService import PostagemService

router = APIRouter()

usuarioService = UsuarioService()
postagemService = PostagemService()
authService = AuthService()

@router.post("/", response_description="Rota para criar um novo Post.", dependencies=[Depends(verificar_token)])
async def rota_criar_postagem(
        authorization: str = Header(default=''),
        postagem: PostagemCriarModel = Depends(PostagemCriarModel)
):
    try:
        usuario_logado = await authService.buscar_usuario_logado(authorization)
        resultado = await postagemService.cadastrar_postagem(postagem, usuario_logado.id)
        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado
    except Exception as error:
        raise error


@router.get(
    "/",
    response_description="Rota para listar postagens",
    dependencies=[Depends(verificar_token)]
)
async def listar_postagens():
    try:
        resultado = await postagemService.listar_postagens()

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as error:
        raise error


@router.get(
    "/{usuario_id}",
    response_description="Rota para listar postagens de um usuario especifico",
    dependencies=[Depends(verificar_token)]
)
async def listar_postagens_usuario(usuario_id: str):
    try:
        resultado = await postagemService.listar_postagens_usuario(usuario_id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as error:
        raise error




@router.put(
    "/curtir/{postagem_id}",
    response_description="Rota para curtir e descurtir uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def curtir_descurtir_postagem(postagem_id: str, Authorization: str = Header(default='')):
    usuario_logado = await authService.buscar_usuario_logado(Authorization)

    resultado = await postagemService.curtir_descurtir(postagem_id, usuario_logado.id)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado


@router.put(
    '/comentar/{postagem_id}',
    response_description="Rota para criar um comentário em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def comentar_postagem(postagem_id: str, Authorization: str = Header(default=''), comentario_model: ComentarioCriarModel = Body(...)):
    usuario_logado = await authService.buscar_usuario_logado(Authorization)

    resultado = await postagemService.criar_comentario(postagem_id, usuario_logado.id, comentario_model.comentario)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado


@router.delete(
    "/deletar/{postagem_id}",
    response_description="Rota para Deletar uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def deletar_postagen(postagem_id: str, Authorization: str = Header(default='')):
    usuario_logado = await authService.buscar_usuario_logado(Authorization)
    resultado = await postagemService.deletar_postagem(postagem_id, usuario_logado.id)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado



@router.delete(
    '/{postagem_id}/comentario/{comentario_id}',
    response_description="Rota para deletar um comentario",
    dependencies=[Depends(verificar_token)]
)
async def deletar_comentario(postagem_id: str, comentario_id: str, Authorization: str = Header(default='')):
    usuario_logado = await authService.buscar_usuario_logado(Authorization)
    resultado = await postagemService.deletar_comentario(postagem_id, usuario_logado.id, comentario_id)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado


@router.put(
    '/{postagem_id}/comentario/{comentario_id}',
    response_description="Rota para Atualizar um comentário em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def atualizar_comentario(postagem_id: str, comentario_id: str, Authorization: str = Header(default=''), comentario_model: ComentarioAtualizarModel = Body(...)):
    usuario_logado = await authService.buscar_usuario_logado(Authorization)

    resultado = await postagemService.atualizar_comentario(postagem_id, usuario_logado.id, comentario_id, comentario_model.comentario)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado