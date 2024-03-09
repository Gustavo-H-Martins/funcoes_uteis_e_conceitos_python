from logs import logs, criar_log
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from navegador import SeleniumDriver
import os
from datetime import datetime
from time import sleep
navegador = SeleniumDriver()
driver = navegador.run()
import json

formatacao_log = f"{__name__}"
log = criar_log(formatacao_log)

# Definindo um parâmetro padrão de busca
parametro_busca_padrao = 'blogs de suplementos alimentares'
# Dando a oportunidade do usuário inserir uma nova busca
parametro_busca = '' # input("Insira um parâmetro de busca, caso oposto vamos pegar um padrão:\n\n")
# se o usuário não inserir pega o padrão
parametro_busca = parametro_busca_padrao if parametro_busca == "" else parametro_busca
# Define a url
url_base =  f"https://www.google.com/search?q={parametro_busca}&hl=pt-BR"

# Abrindo o navegador
driver.get(url=url_base)
# Instancia expressões de manipulação do navegador
actions = ActionChains(driver)
# driver.maximize_window()

botao_mais_resultados = driver.find_element(By.XPATH, "//div[@id='botstuff']/div/div[3]/div[4]/a[1]/h3/div/span[2]")
clicks = range(0, 10)
for click in clicks:
    try:
        actions.move_to_element(botao_mais_resultados).click().perform()
        sleep(0.5)
    except Exception as excessao:
        log.warning(f"Botão mais resultados inacessível, motivo: {excessao}")
        


# define blocos de endereços para extração
titulos_colunas = ["Titulo_01", "Titulo_02", "SubTexto", "http"]
colunas_extracao = {
    'organico': [
        "//div[@id='search']//div[@class='MjjYud']/div/div/div[1]/div/div/span/a/div/div/div/span",
        "//div[@id='search']//div[@class='MjjYud']/div/div/div[1]/div/div/span/a//h3",
        "//div[@id='search']//div[@class='MjjYud']/div/div/div[2]/div/span[last()]",
        "//div[@id='search']//div[@class='MjjYud']/div/div/div[1]/div/div/span/a"
    ],   
    'patrocinado': [
        "//div[@id='tadsb']//div[@class='vdQmEd fP1Qef xpd EtOod pkphOe']/div[1]/a/div[2]/span[1]/span[2]/span[1]/div/span",
        "//div[@id='tadsb']//div[@class='vdQmEd fP1Qef xpd EtOod pkphOe']/div[1]/a/div[1]/span",
        "//div[@id='tadsb']//div[@class='vdQmEd fP1Qef xpd EtOod pkphOe']/div[2]/div/div",
        "//div[@id='tadsb']//div[@class='vdQmEd fP1Qef xpd EtOod pkphOe']/div[1]/a"
    ]
    }
# Definindo os XPATHs dos dados adicionais
adicionais = [
        "//div[@id='botstuff']//div[@class='MjjYud']/div/div/div[1]/div/div/span/a/div/div/div/span",
        "//div[@id='botstuff']//div[@class='MjjYud']/div/div/div[1]/div/div/span/a//h3",
        "//div[@id='botstuff']//div[@class='MjjYud']/div/div/div[2]/div/span[last()]",
        "//div[@id='botstuff']//div[@class='MjjYud']/div/div/div[1]/div/div/span/a"
    ]
colunas_extracao_atributo = [3]

# Verifica se o número de cliks no botão mais resultados é maior ou igual a 10 e inclui os parâmetros adicionais na extração
if clicks[-1] >= 10:
    colunas_extracao["adicionais"] = adicionais
# declara e inicia dicionario de dados
dicionario = {}

# colocando para esperar um pouco para carregar mais resultados na coleta
actions.move_to_element(botao_mais_resultados).perform()
sleep(5)

for bloco in list(colunas_extracao):
    for N_coluna in range(len(titulos_colunas)):
        coluna_extracao = driver.find_elements(By.XPATH, colunas_extracao[bloco][N_coluna])
        for texto_coluna in coluna_extracao:
            if N_coluna not in colunas_extracao_atributo:
                dicionario[titulos_colunas[N_coluna]].append(texto_coluna.text)
            else:
                dicionario[titulos_colunas[N_coluna]].append(texto_coluna.get_attribute("href"))

# Vamos começar a salvar um json aqui
# Vamos abrir um arquivo do tipo json e nomear ele como extracao de dados e passar o nome da coleta como nome do arquivo
with open(file=f"extracao_{parametro_busca.replace('', '_')}_{datetime.strftime(datetime.now(),'%Y_%m_%d')}.json", mode="w") as arquivo_json:
    arquivo_json.write(json.loads(json.dumps(dicionario)))

for titulo in titulos_colunas:
    print(titulo, len(dicionario[titulo]))

# pausando o processo, é interessante para debugar rsrs :D
sleep(10)
driver.quit()
