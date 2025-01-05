from fastapi import FastAPI

from routes.UsuarioRoute import router as UsuarioRoute
from routes.AutenticacaoRoute import router as AutenticacaoRouter
from routes.PostagemRoute import router as PostagemRouter
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UsuarioRoute, tags=["Usuario"], prefix="/api/usuario")
app.include_router(AutenticacaoRouter, tags=["Autenticação"], prefix="/api/auth")
app.include_router(PostagemRouter, tags=["Postagem"], prefix="/api/postagem")




@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "OK"
    }
