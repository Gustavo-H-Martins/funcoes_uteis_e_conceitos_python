import sqlite3
import json
import os

# Constante
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "base_reviews.db"))
def abrir_banco():
    """Estabelece a coneção com o banco"""
    # Conecta ao banco SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def criar_tabela():
    """Cria a tabela do banco que vamos usar por padrão, sem mais que isso por hora"""
    # Conecta ao banco
    conn, cursor = abrir_banco()
    # Criação da tabela para armazenar os dados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY,
            nome_empresa TEXT,
            quantidade_reviews INTEGER,
            media_stars REAL,
            avaliacoes_json TEXT,
            url TEXT
        )
    """)

    # Salva as alterações e fecha a conexão
    conn.commit()
    conn.close()

def inserir_dados(id:str, nome_empresa:str, quantidade_reviews:int, media_stars:float, avaliacoes_json:str, url:str):
    # Conecta ao banco
    conn, cursor = abrir_banco()
    # Insere ou substitui os dados na tabela
    cursor.execute("""
        INSERT OR REPLACE INTO avaliacoes (id, nome_empresa, quantidade_reviews, media_stars, avaliacoes_json, url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id, nome_empresa, quantidade_reviews, media_stars, avaliacoes_json, url))

    # Salva as alterações e fecha a conexão
    conn.commit()
    conn.close()

def otimizar_banco():
    """Realiza uma operação vacuum no banco para otimizar e limpar as transações que possam não ter sido concluídas."""
    # Conecta ao banco
    conn, cursor = abrir_banco()
    # Executa o comando VACUUM para otimizar o banco de dados
    cursor.execute('VACUUM')

    # Salva as alterações e fecha a conexão
    conn.commit()
    conn.close()


def obter_dados_empresa(id:int, limit:int = 0, start_stars:int = 0, end_stars:int= 5) -> dict:
    # Conecta ao banco
    conn, cursor = abrir_banco()
    query_padrao = f"""
        SELECT nome_empresa, quantidade_reviews, media_stars, avaliacoes_json
        FROM avaliacoes
        WHERE id = {id}
    """
    print(end_stars)
    # Executa a consulta para obter os dados da empresa
    cursor.execute(query_padrao)

    # Obtém os resultados da consulta
    resultado = cursor.fetchone()

    # Fecha a conexão
    conn.close()
    
    if resultado:

        reviews = json.loads(resultado[3])
        # Aplica limite na quantidade de reviews com base na variável `limit`
        reviews = reviews[0:limit] if limit else reviews
        # Aplica limite na quantidade de reviews com base na variável `start_stars` e `end_stars`
        if start_stars == True and end_stars == False:
            if start_stars == 2:
                reviews = [review for review in reviews if review["stars"].startswith("2") or review["stars"].startswith("3") or review["stars"].startswith("4") or review["stars"].startswith("5")]
            elif start_stars == 3:
                reviews = [review for review in reviews if review["stars"].startswith("3") or review["stars"].startswith("4") or review["stars"].startswith("5")]
            elif start_stars == 4:
                reviews = [review for review in reviews if review["stars"].startswith("4") or review["stars"].startswith("5")]
            elif start_stars == 5:
                reviews = [review for review in reviews if review["stars"].startswith("5")]
        elif start_stars == False and end_stars == True:
            if end_stars == 5:
                reviews = [review for review in reviews if review["stars"].startswith("1") or review["stars"].startswith("2") or review["stars"].startswith("3") or review["stars"].startswith("4") or review["stars"].startswith("5")]
            elif end_stars == 4:
                reviews = [review for review in reviews if review["stars"].startswith("1") or review["stars"].startswith("2") or review["stars"].startswith("3")]
            elif end_stars == 3:
                reviews = [review for review in reviews if review["stars"].startswith("1") or review["stars"].startswith("2")]
            elif end_stars == 2:
                reviews = [review for review in reviews if review["stars"].startswith("1")]
        else: 
            reviews = [reviews[i] for i in range(0, len(reviews)) if (int(reviews[i]["stars"][0]) >= start_stars and int(reviews[i]["stars"][0]) <= end_stars)]
            
        # Formata os resultados em um dicionário Python
        

        dados_empresa = {
            "empresa": {
                "name": resultado[0],
                "stars": resultado[2],
                "reviews": resultado[1]
            },
            "reviews": reviews
        }

        return dados_empresa

    return {"no_data": "sem dados pra ver aqui."}