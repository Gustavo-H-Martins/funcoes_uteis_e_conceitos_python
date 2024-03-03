from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from db import obter_dados_empresa
from controler import  escrever_lista_raspagem, ler_lista_raspagem
from fastapi import FastAPI
import subprocess
from logs import criar_log, logs

# Criando o logger
formato_mensagem = f'{__name__}:{__name__}'
logger = criar_log(formato_mensagem)

app = FastAPI()

# constante
ROBO_CRAWLER = "./src/crawler.py"
# Comando para executar o arquivo Python
comando = ["python", ROBO_CRAWLER]


@app.get("/")
async def read_root():
    subprocess.run(comando)
    return {"home": "Esta api retorna dados extraídos de reviews do GMaps."}


@app.get("/raspagem/")
async def read_item(
    url: str, limit: int = None, start_stars: int = None, end_stars: int = None
):  
    lista_raspagem = ler_lista_raspagem()
    print(lista_raspagem)
    if url not in lista_raspagem:
        escrever_lista_raspagem(url)
        logger.warning(f"url {url} ainda não mapeada!")
        retorno_json = jsonable_encoder(
            {   "return": "alerta!",
                "url": url,
                "detalhe": "O parâmetro passado não foi mapeado no banco, vamos mapear e disponibilizar para consulta nos próximos minutos ou hora, tente novamente mais tarde!"
            }
        )
    else:
        retorno_api = obter_dados_empresa(url=url)
        # Usa jsonable_encoder para serializar corretamente objetos assíncronos
        retorno_json = jsonable_encoder(retorno_api)
        logger.info("Retornando dados para requisição com sucesso!")
    return JSONResponse(content=retorno_json)
