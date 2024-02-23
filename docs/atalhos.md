# Atalhos, Cheats, Comandos comuns

- Git log:
```bash
# Iniciar um repositório git
git init
# Realizar uma adição
git add . `ou` git add * `ou` git add algum_arquivo.py
# Realizar um commit
git commit -a -m "mensagem do coomit"
# Realizar o envio de um commit para o repositório remoto
git push origin branch_qualquer --force # É bom obrigar o sistema a fazer kkkk
# Criar uma nova branch
git checkout -b nova_branch
# Atualizar changelog
git log --pretty=format:"%h - %an, %ar : %s" --graph  > changelog.md
```

- Pipenv
```bash
# Iniciar um ambiente Pipenv
pipenv install -r requirements.txt

# Executar um ambiente pipenv
pipenv shell

# Atualizar um arquivo requirements.txt com pipenv
pipenv requirements > requirements.txt
```