from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from urllib.parse import quote
from db import obter_dados_empresa
from controler import  escrever_lista_raspagem, ler_lista_raspagem
from fastapi import FastAPI, HTTPException, Header
import subprocess
from logs import criar_log
# Criando o logger
formato_mensagem = f'{__name__}:{__name__}'
logger = criar_log(formato_mensagem)

app = FastAPI()
autenticacao = "suaReviewInc"
class Item(BaseModel):
    url: str
    token: str
# constante
ROBO_CRAWLER = "./update_base.py"
# Comando para executar o arquivo Python
comando = ["python", ROBO_CRAWLER]

# Endpoints API
@app.get("/")
async def read_root():
    subprocess.run(comando)
    return {"home": "Esta api retorna dados extraídos de reviews do GMaps."}

@app.post("/adicionar-url/")
async def adicionar_url(item: Item):
    if item.token != autenticacao:
        raise HTTPException(status_code=401, detail="Token de autenticação inválido")
    
    id = escrever_lista_raspagem(item.url)
    
    return {"message": f"URL {item.url} adicionada com id: {id} com sucesso!"}

@app.get("/raspagem/")
async def read_item(
    token: str = Header(...),
    id: int = 0, limit: int = 0, start_stars: int = 0, end_stars: int = 5
):  
    
    if token != autenticacao:
        raise HTTPException(status_code=401, detail="Token de autenticação inválido")

    try:
        retorno_api = obter_dados_empresa(id=id, limit=limit, start_stars=start_stars, end_stars=end_stars)
        logger.info("Retornando dados para requisição com sucesso!")
        
    except Exception as E:
        logger.warning(f"Id {id} não encontrado")
        retorno_api = jsonable_encoder(
            {   "return": "alerta!",
                "erro": E
            }
        )
    return retorno_api
