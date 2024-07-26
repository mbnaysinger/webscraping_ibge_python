import requests

# URL da API
url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

# Fazendo a requisição HTTP para obter os dados
response = requests.get(url)
municipios = response.json()

# Lista para armazenar os dados extraídos
dados_extraidos = []

# Extraindo os dados necessários
for municipio in municipios:
    id_municipio = municipio['id']
    nome_municipio = municipio['nome'].replace("'", "''")
    nome_microrregiao = municipio['microrregiao']['nome'].replace("'", "''")
    nome_mesorregiao = municipio['microrregiao']['mesorregiao']['nome'].replace("'", "''")
    sigla_uf = municipio['microrregiao']['mesorregiao']['UF']['sigla']

    dados_extraidos.append((id_municipio, nome_municipio, nome_microrregiao, nome_mesorregiao, sigla_uf))

# Gerando o script SQL
with open('insert_municipios.sql', 'w') as file:
    file.write("INSERT INTO municipios (cod_mun, nome, microrregiao, mesorregiao, uf) VALUES\n")
    for i, dados in enumerate(dados_extraidos):
        id_municipio, nome_municipio, nome_microrregiao, nome_mesorregiao, sigla_uf = dados
        file.write(f"({id_municipio}, '{nome_municipio}', '{nome_microrregiao}', '{nome_mesorregiao}', '{sigla_uf}')")
        if i < len(dados_extraidos) - 1:
            file.write(",\n")
        else:
            file.write(";\n")

print("Script SQL gerado com sucesso em 'insert_municipios.sql'")