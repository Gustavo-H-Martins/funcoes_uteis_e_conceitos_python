from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from urllib.parse import quote
from db import obter_dados_empresa, deletar_dados_por_id
from controler import  escrever_lista_raspagem, ler_lista_raspagem
from fastapi import FastAPI, HTTPException, Header
import subprocess
from logs import criar_log
# Criando o logger
formato_mensagem = f'{__name__}:{__name__}'
logger = criar_log(formato_mensagem)

app = FastAPI()
autenticacao = "7beed2ea8ae25d0fd50d8942b938b202"
class Item(BaseModel):
    url_empresa: str
    id_empresa: str
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

# Endpoint DELETE para deletar dados por ID
@app.delete("/deletar-dados")
async def deletar_dados(id: str, token: str = Header(...)):
    if token != autenticacao:
        raise HTTPException(status_code=401, detail="Token de autenticação inválido")
    
    deletar_dados_por_id(id)
    
    return {"message": f"Dados com ID {id} deletados com sucesso!"}

@app.post("/adicionar-url")
async def adicionar_url(item: Item):
    if item.token != autenticacao:
        raise HTTPException(status_code=401, detail="Token de autenticação inválido")
    
    escrever_lista_raspagem(id=item.id_empresa, url=item.url_empresa)
    
    return {"message": f"URL {item.url_empresa} adicionada com id: {item.id_empresa} com sucesso!"}


@app.get("/lista_raspagem")
async def read_item(
    token: str = Header(...)
):  
    if token != autenticacao:
        raise HTTPException(status_code=401, detail="Token de autenticação inválido")

    try:
        lista_raspagem = ler_lista_raspagem()
        lista_raspagem["status"] = "200"
            
    except Exception as E:
        logger.warning(f"Id {id} não encontrado")
        lista_raspagem = jsonable_encoder(
            {   "status": "204",
                "detalhes": "sem conteúdo para mostrar",
                "return": "alerta!",
                "erro": E
            }
        )
    return lista_raspagem

@app.get("/raspagem")
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
            {   "status": "204",
                "detalhes": "sem conteúdo para mostrar",
                "return": "alerta!",
                "erro": E
            }
        )
    return retorno_api
