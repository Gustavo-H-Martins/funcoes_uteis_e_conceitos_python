import os
from service import raspardor
from db import inserir_dados
from logs import criar_log, logs
import re
from json import load, dump


# Criando o logger
formato_mensagem = f'{__name__}:{__name__}'
logger = criar_log(formato_mensagem)

# CONSTANTE
CRAWLER_LIST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"config", "lista_raspagem.json"))

@logs
def ler_json(caminho:str) -> dict:
    with open (file=caminho, mode="r") as f:
        conteudo = load(f)
    return conteudo

@logs
def ler_lista_raspagem() -> list:
    """Realiza a leitura dos dados dentro do arquivo de configurações de lista de raspagem"""
    lista_raspagem = ler_json(CRAWLER_LIST_PATH)

    logger.info(f"Retornando um total de {len(lista_raspagem)} de itens para serem raspados!")
    return list(lista_raspagem.values())
@logs
def escrever_lista_raspagem(url:str):
    """Realiza a escrita de dados dentro do arquivo de configurações de lista de raspagem"""

    if not os.path.exists(CRAWLER_LIST_PATH):
        with open(CRAWLER_LIST_PATH, "w") as f:
            posicao = "1"
            dados = {posicao:url}
            dump(dados, f, indent=2, separators=(",", ": "), sort_keys=True)
    else:
        with open(CRAWLER_LIST_PATH, "r+") as f:
            data = load(f)
            posicao = len(data) + 1
            dados = {f"{posicao}":url}
            data.update(dados)
            f.seek(0)
            f.truncate()
            dump(data, f, indent=2, separators=(",", ": "), sort_keys=True)
    return posicao

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
    