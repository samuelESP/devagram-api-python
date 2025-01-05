from typing import List

import motor
from bson import ObjectId
from decouple import config
from motor import motor_asyncio
from models.UsuarioModel import UsuarioCriarModel, Usuariomodel
from utils.AuthUtil import Authutil
from utils.Converterutil import ConverterUtil

MONGODB_URL = config("MONGODB_URL")

cliente = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = cliente.devagram

usuario_collection = database.get_collection("usuario")


converterutil = ConverterUtil()
authUtil = Authutil()

class UsuarioRepository:

    async def criar_usuario(self, usuario: UsuarioCriarModel) -> Usuariomodel:
        usuario.senha = authUtil.gerar_senha_criptografada(usuario.senha)

        usuario_dict = {
            "nome": usuario.nome,
            "email": usuario.email,
            "senha": usuario.senha,
            "seguidores": [],
            "seguindo": []
        }

        usuario_criado = await usuario_collection.insert_one(usuario_dict)

        novo_usuario = await usuario_collection.find_one({"_id": usuario_criado.inserted_id})

        return converterutil.usuario_converter(novo_usuario)


    async def listar_usuarios(self, nome) -> List[Usuariomodel]:
        usuarios_encontrados = usuario_collection.find({
            "nome": {
                "$regex": nome,
                '$options': 'i'
            }
        })

        usuarios = []


        usuarios = []

        async for usuario in usuarios_encontrados:
            usuarios.append(converterutil.usuario_converter(usuario))

        return usuarios


    async def buscar_usuario(self, id: str) -> Usuariomodel:
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})
        if usuario:
            return converterutil.usuario_converter(usuario)


    async def buscar_usuario_email(self, email: str) -> Usuariomodel:
        usuario = await usuario_collection.find_one({"email": email})

        if usuario:
            return converterutil.usuario_converter(usuario)
    async def atualizar_usuario(self, id: str, dados_usuario: dict) -> Usuariomodel:
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})
        if usuario:
            if 'senha' in dados_usuario and dados_usuario['senha'] is not usuario.get('senha'):
                dados_usuario['senha'] = authUtil.gerar_senha_criptografada(dados_usuario['senha'])
                
            await usuario_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": dados_usuario}
            )

            usuario_encontrado = await usuario_collection.find_one({
                "_id": ObjectId(id)
            })
            return converterutil.usuario_converter(usuario_encontrado)


    async def deletar_usuario(self, id: str):
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})
        if usuario:
            await usuario_collection.delete_one({"_id": ObjectId(id)})

