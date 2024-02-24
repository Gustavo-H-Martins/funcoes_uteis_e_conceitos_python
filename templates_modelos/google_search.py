from logs import logs, criar_mensagem_error
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from navegador import SeleniumDriver
import os
from time import sleep
navegador = SeleniumDriver()
driver = navegador.run()
# Defindo um parâmetro padrão de busca
parametro_busca_padrao = '"suplementos alimentar";site:blog;inurl:https://*'
# Dando a oportunidade do usuário inserir uma nova busca
parametro_busca = input("Insira um parâmetro de busca, caso oposto vamos pegar um padrão:\n\n")
# se o usuário não inserir pega o padrão
parametro_busca = parametro_busca_padrao if parametro_busca == "" else parametro_busca
# Define a url
url_base =  f"https://www.google.com/search?q={parametro_busca}&hl=pt-BR"

# Abrindo o navegador
driver.get(url=url_base)
# Instancia explessões de manipulação do navegador
actions = ActionChains(driver)
driver.maximize_window()
# Pegando os resultados de pesquisa
resultados = driver.find_elements(By.CLASS_NAME, "ULSxyf")

[print(resultado.text) for resultado in resultados]

# pausando o processo, é interessante para debugar rsrs :D
sleep(5)
driver.quit()