from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from urllib.parse import quote
from db import obter_dados_empresa
from controler import  escrever_lista_raspagem, ler_lista_raspagem
from fastapi import FastAPI
import subprocess
from logs import criar_log, logs
import re
# Criando o logger
formato_mensagem = f'{__name__}:{__name__}'
logger = criar_log(formato_mensagem)

app = FastAPI()



# constante
ROBO_CRAWLER = "./service/crawler.py"
# Comando para executar o arquivo Python
comando = ["python", ROBO_CRAWLER]

# Processo auxiliar global
lista_raspagem = ler_lista_raspagem()
lista_so_nome = []
for item in lista_raspagem:
    item_raspagem = re.sub(r'[^\w\s]', ' ', item)

    # Removendo múltiplos espaços em branco
    lista_so_nome.append(re.sub(r'\s+', ' ', item_raspagem))

# Endpoints API
@app.get("/")
async def read_root():
    subprocess.run(comando)
    return {"home": "Esta api retorna dados extraídos de reviews do GMaps."}


@app.get("/raspagem/")
async def read_item(
    url: str = None, limit: int = 0, start_stars: int = 0, end_stars: int = 5
):  
    if url not in lista_raspagem:
        escrever_lista_raspagem(url)
        logger.warning(f"Link {url} ainda não mapeado!")
        retorno_api = jsonable_encoder(
            {   "return": "alerta!",
                "empresa": url,
                "detalhe": "O parâmetro passado não foi mapeado no banco, vamos mapear e disponibilizar para consulta nos próximos minutos ou hora, tente novamente mais tarde!"
            }
        )
    else:
        retorno_api = obter_dados_empresa(url=url, limit=limit, start_stars=start_stars, end_stars=end_stars)
        logger.info("Retornando dados para requisição com sucesso!")
    return retorno_api
