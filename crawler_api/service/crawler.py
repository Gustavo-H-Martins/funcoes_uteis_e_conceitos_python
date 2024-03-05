from playwright.async_api import async_playwright
import re
from time import sleep
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from logs import criar_log, logs

# Criando o logger
formato_mensagem = f'{__name__}:{__name__}'
logger = criar_log(formato_mensagem)

@logs
async def raspardor(
    url:str = ""
) -> dict:
    """Robôzinho que vai raspar os dados solicitados
    Parâmetros:
        - `url`: Url de onde vamos raspar os dados
    Retorno:
        - `retorno_raspagem`: dicionário de dados para populaar base de raspagem de reviews
    """
    async with async_playwright() as p:
        retorno_raspagem = {"empresa": {"name": "", "stars": 0, "reviews": 0}, "reviews": []}
        # Abre o navegador e carrega a página com a url passada
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)


        # Busca o primeiro item da raspagem e dados da empresa
        await page.locator(".hh2c6:nth-child(1)").click()
        retorno_raspagem["empresa"]["name"] = await page.locator(
            ".DUwDvf.lfPIob"
        ).text_content()
        reviews = await page.locator(
            '//*[@class="F7nice "]/span[2]/span'
        ).text_content()
        retorno_raspagem["empresa"]["reviews"] = re.sub(
            r"\((\d+)\)", r"\1", reviews.replace(",", ".")
        )
        media = await page.locator(
            '//*[@class="F7nice "]/span[1]/span[1]'
        ).text_content()
        retorno_raspagem["empresa"]["stars"] = media.replace(",", ".")

        # Busca dados de avaliações
        await page.locator(".hh2c6:nth-child(2)").click()
        await page.get_by_alt_text("Ordenar").click()
        await page.locator('#action-menu > div:nth-child(2)').click()

        for i in range(0, 10):
            await page.mouse.wheel(0, 15000)
            sleep(2)

        # Aguarda o carregamento dos elementos
        await page.wait_for_selector("div.d4r55")

        clientes = await page.query_selector_all("div.d4r55")
        imagens = await page.query_selector_all("img.NBa7we")
        datas = await page.query_selector_all("span.rsqaWe")
        estrelas = await page.query_selector_all("span.kvMYJc")
        comentarios = await page.query_selector_all("span.wiI7pd")
        tamanho_elementos = len(clientes)

        for i in range(0, tamanho_elementos):
            cliente = await clientes[i].text_content()
            imagem = await imagens[i].evaluate("(element) => element.src")
            imagem_aumentada = imagem.replace("w36-h36", "w50-h50")
            data = await datas[i].text_content()
            estrela = await estrelas[i].evaluate(
                '(element) => element.getAttribute("aria-label")'
            )
            try:
                comentario = await comentarios[i].text_content()
            except Exception as e:
                comentario = "Sem comentários"
                logger.warning(f"Não encontrado valor para o comentário erro: {e}")
            retorno_raspagem["reviews"].append(
                {
                    "image": imagem_aumentada,
                    "name": cliente,
                    "stars": estrela,
                    "date": data,
                    "text": comentario,
                }
            )
        await browser.close()
    logger.info("Raspado dados com sucesso!")
    return retorno_raspagem