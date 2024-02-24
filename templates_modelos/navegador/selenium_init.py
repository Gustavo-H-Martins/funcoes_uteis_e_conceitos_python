# Bibliotecas necessárias para execução do script
import ctypes
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.chrome import ChromeDriverManager

# Definindo a classe responsável pela automação do navegador
class SeleniumDriver:
    # Método __init__ sempre será executado assim que instanciarmos a classe
    def __init__(self):
        user32 = ctypes.windll.user32
        resolucao = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        chrome_options = Options()
        ##chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f'--window-size={resolucao[0]},{resolucao[1]}')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--log-level=3')


        self.driver = Chrome(service=Service(ChromeDriverManager().install(), options=chrome_options))

    # Método run responsável por retornar o objeto driver (navegador) no script que formos consumir
    def run(self):
        return self.driver

# Para usar essa classe em outro arquivo, você pode instanciá-la e chamar o método run para obter o driver.
    # Exemplo de uso:
        # selenium_driver = SeleniumDriver()
        # driver = selenium_driver.run()
