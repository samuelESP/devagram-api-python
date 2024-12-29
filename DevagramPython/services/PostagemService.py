import os
from datetime import datetime

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
                    f'fotos-postagem/{nova_postagem["id"]}.jpg',
                    caminho_foto
                )
                nova_postagem = await postagemRepository.atualizar_postagem(nova_postagem["id"], {"foto": url_foto})

                os.remove(caminho_foto)
            except Exception as error:
                return (error)


            return {
                "mensagem": "postagem criada om sucesso",
                "dados": nova_postagem,
                "status": 201
            }

        except Exception as error:
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }


    async def listar_postagens(self):
        try:
            postagens = await postagemRepository.listar_postagem()
            return {
                "mensagem": "Postagens listadas com sucesso!",
                "dados": postagens,
                "status": 200
            }
        except Exception as error:
            print(error)
            return {
                "mensagem": "Erro interno no servidor",
                "dados": str(error),
                "status": 500
            }