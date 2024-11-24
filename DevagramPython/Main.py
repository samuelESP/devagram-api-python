from fastapi import FastAPI

from routes.UsuarioRoute import router as UsuarioRoute

from routes.AutenticacaoRoute import router as AutenticacaoRouter



app = FastAPI()
app.include_router(UsuarioRoute, tags=["Usuario"], prefix="/api/usuario")
app.include_router(AutenticacaoRouter, tags=["Autenticação"], prefix="/api/auth")
@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "OK"
    }
