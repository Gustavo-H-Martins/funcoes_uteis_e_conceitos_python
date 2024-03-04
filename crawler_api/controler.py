import os
from service import raspardor
from db import inserir_dados
from logs import criar_log, logs
import re

# Criando o logger
formato_mensagem = f'{__name__}:{__name__}'
logger = criar_log(formato_mensagem)

# CONSTANTE
CRAWLER_LIST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"config", "lista_raspagem.txt"))
@logs
def ler_lista_raspagem() -> list:
    """Realiza a leitura dos dados dentro do arquivo de configurações de lista de raspagem"""
    with open(file=CRAWLER_LIST_PATH, mode="r") as f:
        lista_raspagem = [linha.strip().split("/@-")[0].replace("https://www.google.com/maps/place/", "") for linha in f.readlines()]
        lista_so_nome = []
        for item in lista_raspagem:
            item_raspagem = re.sub(r'[^\w\s]', ' ', item)

            # Removendo múltiplos espaços em branco
            lista_so_nome.append(re.sub(r'\s+', ' ', item_raspagem))


        f.close()

    logger.info(f"Retornando um total de {len(lista_so_nome)} de itens para serem raspados!")
    return lista_so_nome
@logs
def escrever_lista_raspagem(texto:str):
    """Realiza a escrita de dados dentro do arquivo de configurações de lista de raspagem"""

    with open(file=CRAWLER_LIST_PATH, mode="+a") as f:
        f.write(f"{texto.strip()}\n")
        f.close()
    
    logger.info(f"Salvo linha com valor {texto}")

@logs
def deletar_lista_raspasgem(texto:str):
    """Deleta um valor dentro do arquivo de configurações de lista de raspagem"""
    with open(file=CRAWLER_LIST_PATH, mode='r+') as f:
        linhas = f.readlines()
        f.seek(0)  # Volta para o início do arquivo

        # Escreve todas as linhas, exceto a que queremos deletar
        for linha in linhas:
            if linha.strip() != texto.strip():
                f.write(f"{linha}\n")
        # Remove qualquer conteúdo que possa ter sobrado do arquivo original
        f.truncate()
    logger.info(f"Deletada linha com valor {texto}")

@logs
def raspar_chamada_api(url:str):
    lista_raspagem = ler_lista_raspagem()
    if url not in lista_raspagem:
        escrever_lista_raspagem(url)
    retorno_api = raspardor(url=url)
    if retorno_api:
        logger.info("Achamos dados na raspagem!")
        inserir_dados(
            nome_empresa=retorno_api["empresa"]["name"],
            quantidade_reviews=retorno_api["empresa"]["reviews"],
            media_stars=retorno_api["empresa"]["stars"],
            avaliacoes_json=retorno_api["reviews"],
            url=url
        )
    else:
        logger.warning("Sem dados para retornar por agora!")
    