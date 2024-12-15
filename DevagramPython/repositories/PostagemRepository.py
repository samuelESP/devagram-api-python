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

    async def criar_postagem(self, postagem: PostagemCriarModel) -> dict:
        postagem_criado = await postagem_collection.insert_one(postagem.__dict__)

        nova_postagem = await postagem_collection.find_one({"_id": postagem_criado.inserted_id})
        return converterUtil.postagem_converter(nova_postagem)



    async def listar_postagem(self):
        return postagem_collection.find()



    async def buscar_postagem(self, id: str) ->dict:
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})
        if postagem:
            return converterUtil.postagem_converter(postagem)


    async def deletar_postagem(self, id: str):
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})
        if postagem:
            await postagem_collection.delete_one({"_id": ObjectId(id)})

