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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

def inserir_dados(nome_empresa:str, quantidade_reviews:int, media_stars:float, avaliacoes_json:str, url:str):
    # Conecta ao banco
    conn, cursor = abrir_banco()
    # Insere ou substitui os dados na tabela
    cursor.execute("""
        INSERT OR REPLACE INTO avaliacoes (nome_empresa, quantidade_reviews, media_stars, avaliacoes_json, url)
        VALUES (?, ?, ?, ?, ?)
    """, (nome_empresa, quantidade_reviews, media_stars, avaliacoes_json, url))

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


def obter_dados_empresa(url) -> str:
    # Conecta ao banco
    conn, cursor = abrir_banco()

    # Executa a consulta para obter os dados da empresa
    cursor.execute(f"""
        SELECT nome_empresa, quantidade_reviews, media_stars, avaliacoes_json
        FROM avaliacoes
        WHERE url = {url}
    """)

    # Obtém os resultados da consulta
    resultado = cursor.fetchone()

    # Fecha a conexão
    conn.close()

    if resultado:
        # Formata os resultados em um dicionário Python
        dados_empresa = {
            "empresa": {
                "name": resultado[0],
                "stars": resultado[2],
                "reviews": resultado[1]
            },
            "reviews": json.loads(resultado[3])
        }

        return json.dumps(dados_empresa, indent=4)

    return ""
