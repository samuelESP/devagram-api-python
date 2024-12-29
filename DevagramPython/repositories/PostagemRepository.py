from datetime import datetime

import motor
from bson import ObjectId
from decouple import config
from motor import motor_asyncio
from models.PostagemModel import PostagemCriarModel
from utils.Converterutil import ConverterUtil

MONGODB_URL = config("MONGODB_URL")

cliente = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = cliente.devagram

postagem_collection = database.get_collection("postagem")

converterUtil = ConverterUtil()
class PostagemRepository:

    async def criar_postagem(self, postagem: PostagemCriarModel, usuario_id) -> dict:

        postagem_dict = {
            "usuario_id": ObjectId(usuario_id),
            "legenda": postagem.legenda,
            "curtidas": 0,
            "comentarios": [],
            "data": datetime.now()
        }


        postagem_criado = await postagem_collection.insert_one(postagem_dict)
        nova_postagem = await postagem_collection.find_one({"_id": postagem_criado.inserted_id})
        print(nova_postagem)
        return converterUtil.postagem_converter(nova_postagem)


    async def atualizar_postagem(self, id: str, dados_postagem: dict):
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

        if postagem:
            await postagem_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": dados_postagem}
            )

            postagem_atualizada = await postagem_collection.find_one({
                "_id": ObjectId(id)
            })

            return converterUtil.postagem_converter(postagem_atualizada)


    async def listar_postagem(self):
        postagens_encontradas = postagem_collection.aggregate([{
            "$lookup": {
                "from": "usuario",
                "localField": "usuario_id",
                "foreignField": "_id",
                "as": "usuario"
            }
        }])
        postagens =[]

        async for postagem in postagens_encontradas:
            postagens.append(converterUtil.postagem_converter(postagem))

        return postagens


    async def buscar_postagem(self, id: str) ->dict:
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})
        if postagem:
            return converterUtil.postagem_converter(postagem)


    async def deletar_postagem(self, id: str):
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})
        if postagem:
            await postagem_collection.delete_one({"_id": ObjectId(id)})

