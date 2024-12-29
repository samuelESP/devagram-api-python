from fastapi import APIRouter, HTTPException, Depends, Header
from middleware.JWTmiddleware import verificar_token
from models.PostagemModel import PostagemCriarModel
from services.AuthService import decodificar_token_jwt
from services.UsuarioService import UsuarioService
from services.PostagemService import PostagemService

router = APIRouter()

usuarioService = UsuarioService()
postagemService = PostagemService()


@router.post("/", response_description="Rota para criar um novo Post.", dependencies=[Depends(verificar_token)])
async def rota_criar_postagem(
        authorization: str = Header(default=''),
        postagem: PostagemCriarModel = Depends(PostagemCriarModel)
):
    try:

        token = authorization.split(" ")[1]
        payload = decodificar_token_jwt(token)
        resultado_usuario = await usuarioService.buscar_usuario_logado(payload["usuario_id"])
        usuario_logado = resultado_usuario["dados"]
        resultado = await postagemService.cadastrar_postagem(postagem, usuario_logado["id"])
        if not resultado:
            return {
                "Errei": "errei"
            }
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

        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

        return resultado
    except Exception as error:
        raise error