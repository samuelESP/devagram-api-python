import os
from datetime import datetime

from bson import ObjectId
from dtos.ResponseDTO import ResponseDTO
from providers.AWSprovider import AWSprovider
from repositories.PostagemRepository import PostagemRepository


awsProvider = AWSprovider()

postagemRepository = PostagemRepository()


class PostagemService:
    async def cadastrar_postagem(self, postagem, usuario_id):
        try:

            nova_postagem = await postagemRepository.criar_postagem(postagem, usuario_id)
            try:
                caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}.jpg'

                with open(caminho_foto, 'wb+') as arquivo:
                    arquivo.write(postagem.foto.file.read())

                url_foto = awsProvider.upload_arquivo_s3(
                    f'fotos-postagem/{nova_postagem.id}.jpg',
                    caminho_foto
                )
                nova_postagem = await postagemRepository.atualizar_postagem(nova_postagem.id, {"foto": url_foto})

                os.remove(caminho_foto)
            except Exception as erro:
                return (erro)

            return ResponseDTO("Postagem criada com sucesso!", nova_postagem, 201)

        except Exception as erro:
            return ResponseDTO("Erro interno no servidor", str(erro), 500)

    async def listar_postagens(self):
        try:

            postagens = await postagemRepository.listar_postagem()

            for p in postagens:
                p.total_curtidas = len(p.curtidas)

            return ResponseDTO("Postagens listadas com sucesso!", postagens, 200)
        except Exception as erro:
            print(erro)
            return ResponseDTO("Erro interno no servidor", str(erro), 500)

    async def listar_postagens_usuario(self, usuario_id):
        try:
            postagens = await postagemRepository.listar_postagens_usuario(usuario_id)

            for p in postagens:
                p.total_curtidas = len(p.curtidas)
                p.total_comentarios = len(p.comentarios)

            return ResponseDTO("Postagens listadas com sucesso!", postagens, 200)

        except Exception as erro:
            print(erro)
            return ResponseDTO("Erro interno no servidor", str(erro), 500)

    async def curtir_descurtir(self, postagem_id, usuario_id):
        try:

            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)

            if postagem_encontrada.curtidas.count(usuario_id) > 0:
                postagem_encontrada.curtidas.remove(usuario_id)
            else:
                postagem_encontrada.curtidas.append(ObjectId(usuario_id))

            postagem_atualizada = await postagemRepository.atualizar_postagem(
                postagem_encontrada.id,
                {"curtidas": postagem_encontrada.curtidas}
            )

            return ResponseDTO("Postagem atualizada", postagem_atualizada, 200)

        except Exception as erro:
            return ResponseDTO("Erro interno no servidor", str(erro), 500)

    async def criar_comentario(self, postagem_id, usuario_id, comentario):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)
            postagem_encontrada.comentarios.append({
                "comentario_id": ObjectId(),
                "usuario_id": ObjectId(usuario_id),
                "comentario": comentario
            })

            postagem_atualizada = await postagemRepository.atualizar_postagem(
                postagem_encontrada.id,
                {"comentarios": postagem_encontrada.comentarios}
            )
            return ResponseDTO("Comentário criado", postagem_atualizada, 200)
        except Exception as erro:
            return ResponseDTO("Erro interno no servidor", str(erro), 500)

    async def deletar_postagem(self, postagem_id, usuario_id):
        try:

            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)

            if not postagem_encontrada:
                return ResponseDTO("Postagem não encontrada", "", 404)

            if not postagem_encontrada.usuario_id == usuario_id:
                return ResponseDTO("Não é possível realizar essa requisição", "", 401)

            await postagemRepository.deletar_postagem(postagem_id)
            return ResponseDTO("Postagem deletada com sucesso", "", 200)

        except Exception as erro:
            return ResponseDTO("Erro interno no servidor", str(erro), 500)

    async def deletar_comentario(self, postagem_id, usuario_id, comentario_id):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)
            for comentario in postagem_encontrada.comentarios:
                if comentario["comentario_id"] == comentario_id:
                    if not (comentario["usuario_id"] == usuario_id or postagem_encontrada.usuario_id == usuario_id):
                        return ResponseDTO("Requisição Inválida", "", 401)

                    postagem_encontrada.comentarios.remove(comentario)



            postagem_atualizada = await postagemRepository.atualizar_postagem(
                postagem_encontrada.id,
                {"comentarios": postagem_encontrada.comentarios}
            )
            return ResponseDTO("Comentário deletado com sucesso!", postagem_atualizada, 200)

        except Exception as erro:
            print(erro)
            return ResponseDTO("Erro interno no servidor", str(erro), 500)

    async def atualizar_comentario(self, postagem_id, usuario_id, comentario_id, comentario_atualizado):
        try:
            postagem_encontrada = await postagemRepository.buscar_postagem(postagem_id)

            for comentario in postagem_encontrada.comentarios:
                if comentario["comentario_id"] == comentario_id:
                    if not comentario["usuario_id"] == usuario_id:
                        return ResponseDTO("Requisição Inválida", "", 401)

                    comentario = comentario_atualizado

            postagem_atualizada = await postagemRepository.atualizar_postagem(
                postagem_encontrada.id,
                {"comentarios": postagem_encontrada.comentarios}
            )
            return ResponseDTO("comentário deletado com sucesso!", postagem_atualizada, 200)

        except Exception as erro:
            print(erro)
            return ResponseDTO("Erro interno no servidor", str(erro), 500)
