import logging
import pytz
import datetime
from functools import wraps

def criar_log(source_log: str = __name__):
    """
    Função para criar um ponto de observação através do uso de logs
    Parâmetro:
        - `source_log`: não da função de entrada
    Retorno: 
        retorna a função de entrada
    """

    # Adicionando configuração para usar o fuso horário de Brasília
    logging.Formatter.converter = logging.Formatter.converter = lambda *args: (
        datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).timetuple()
    )
    
    log_format = '%(levelname)-8s||%(asctime)s||%(name)-12s||%(lineno)d||%(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format)

    
    # Criando o logger
    logger = logging.getLogger(source_log)
    
    return logger

def criar_mensagem_error(message: str) -> None:
    msg_log = criar_log()
    msg_log.error(message)

def logs(func):
    """
    Decorator para monitorar via log qualquer função desejada
    Parâmetro:
        - `func`: não da função de entrada
    Retorno: 
        retorna a função de entrada
    """

    @wraps(func)
    def inner(*args, **kwargs):
        logger = criar_log(func.__name__)
        log_message = "Iniciando...."
        logger.info(log_message)
        result = func(*args, **kwargs)
        log_message = "Finalizando.... "
        logger.info(log_message)
        return result

    return inner


