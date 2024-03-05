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

    for item in lista_de_raspagem:
        retorno_raspagem = await raspardor(item)
        if len(retorno_raspagem["reviews"]) < 1:
            logger.warning(f"Não conseguimos retorno de dados para o item: {item}")
        else:
            inserir_dados(
                nome_empresa=retorno_raspagem["empresa"]["name"],
                quantidade_reviews=retorno_raspagem["empresa"]["reviews"],
                media_stars=retorno_raspagem["empresa"]["stars"],
                avaliacoes_json=dumps(retorno_raspagem["reviews"]),
                url=item
            )

if __name__ == "__main__":
    asyncio.run(main())
