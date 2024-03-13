import asyncio
from json import dumps
from service import raspardor
from controler import ler_lista_raspagem
from db import inserir_dados
from logs import logs, criar_log

# Criando o logger
formato_mensagem = f'{__name__}:{__name__}'
logger = criar_log(formato_mensagem)

async def main():
    lista_de_raspagem = ler_lista_raspagem()

    for id, url in lista_de_raspagem.items():
        retorno_raspagem = await raspardor(url)
        if len(retorno_raspagem["reviews"]) < 1:
            logger.warning(f"Não conseguimos retorno de dados para o id: {id}, url: {url}")
        else:
            inserir_dados(
                id=f"{id}",
                nome_empresa=retorno_raspagem["empresa"]["name"],
                quantidade_reviews=retorno_raspagem["empresa"]["reviews"],
                media_stars=retorno_raspagem["empresa"]["stars"],
                avaliacoes_json=dumps(retorno_raspagem["reviews"]),
                url=url
            )

if __name__ == "__main__":
    asyncio.run(main())
