from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])


def gerar_senha_criptografada(senha):
    return pwd_context.hash(senha)


def verificar_senha(senha, senhacriptografada):
    return pwd_context.verify(senha, senhacriptografada)

