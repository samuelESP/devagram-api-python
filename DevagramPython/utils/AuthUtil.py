from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])

class Authutil:
    def gerar_senha_criptografada(self, senha):
        return pwd_context.hash(senha)


    def verificar_senha(self, senha, senhacriptografada):
        return pwd_context.verify(senha, senhacriptografada)

