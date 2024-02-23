[![Badge](https://img.shields.io/badge/DESCRIÇÃO_-0.1.0.B-red)](https://github.com/seu-usuario/seu-repositorio)  [![Badge](https://img.shields.io/badge/PRODUÇÃO_-0.1.0.B-green)](https://github.com/seu-usuario/seu-repositorio) [![Badge](https://img.shields.io/badge/HOMOLOGAÇÃO-0.1.0.B-yellow)](https://github.com/seu-usuario/seu-repositorio)

## Scripts Explicados

### Script de Logs
O script de logs consiste em funções e um decorator para facilitar a geração de logs em um programa Python. 

Breve explicação de cada parte do script:

1. **Função `criar_log(source_log: str = __name__)`:**
   - Esta função cria um logger personalizado para registrar mensagens de log.
   - Ela utiliza o fuso horário de Brasília para registrar a data e hora das mensagens.
   - Retorna o logger criado.

2. **Função `criar_mensagem_error(message: str) -> None`:**
   - Esta função cria uma mensagem de erro no log usando o logger criado pela função `criar_log()`.

3. **Decorator `logs(func)`:**
   - Este decorator é usado para monitorar a execução de funções específicas, registrando mensagens de log no início e no final da execução.
   - Ele cria um logger com o nome da função decorada, registra uma mensagem de início e fim da execução da função e retorna o resultado da função original.

### Script Selenium_Init
O script Selenium_Init é responsável por configurar e iniciar um driver do Selenium para automação de navegação web. 

Breve explicação do que o script faz:

1. **Classe `SeleniumDriver`:**
   - Esta classe é responsável por inicializar e fornecer um objeto driver do Selenium para automação.
   - No método `__init__`, ele configura as opções do Chrome, define as preferências e configurações do navegador, e inicializa o driver do Chrome.
   - O método `run()` retorna o objeto driver configurado.

2. **Utilização:**
   - Para utilizar essa classe em outro arquivo, você pode instanciá-la e chamar o método `run()` para obter o driver do navegador.
   - Exemplo de uso:
     ```python
     selenium_driver = SeleniumDriver()
     driver = selenium_driver.run()
     ```
### Informação relevante:
Os arquivos:
   1. **[Pipfile](Pipfile):**
      Declara as dependências para criação do ambiente de desenvolvimento ou deploy usando o gerenciador de dependências [pipenv](https://pipenv.pypa.io/en/latest/)
   - **[Pipfile.lock](Pipfile.lock):**
      Arquivo gerado após as dependências terem sido instaladas, contendo as referências de acordo com a versão do python utilizada.
   - **[requirements.txt](requirements.txt):**
      Arquivo de dependências compatível com qualquer gerenciador de dependência python bastando usar a flag `-r` e o caminho do arquivo `-r ./requirements.txt`
      Exemplos:
      ```bash
      # pipy
      pip install -r ./requirements.txt
      # pipenv
      pipenv install -r ./requirements.txt
      # E por aí vai!
      ```

## 🧑🏽 Colaboradores
Este projeto foi criado por:

- Gustavo H Martins ([GitHub](https://github.com/Gustavo-H-Martins) | [LinkedIn](https://www.linkedin.com/in/gustavo-henrique-lopes-martins-361789192/))

[![Gustavo-H-Martins](https://github-readme-stats.vercel.app/api?username=Gustavo-H-Martins&show_icons=true&theme=radical)](https://github.com/Gustavo-H-Martins)

Essas explicações ajudam a compreender como os scripts funcionam e como podem ser integrados em outros projetos.