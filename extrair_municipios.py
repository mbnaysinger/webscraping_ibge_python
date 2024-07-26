import requests
import pandas as pd

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
    nome_municipio = municipio['nome']
    nome_microrregiao = municipio['microrregiao']['nome']
    nome_mesorregiao = municipio['microrregiao']['mesorregiao']['nome']
    sigla_uf = municipio['microrregiao']['mesorregiao']['UF']['sigla']

    dados_extraidos.append({
        'ID Município': id_municipio,
        'Nome Município': nome_municipio,
        'Nome Microrregião': nome_microrregiao,
        'Nome Mesorregião': nome_mesorregiao,
        'Sigla UF': sigla_uf
    })

# Criando um DataFrame com os dados extraídos
df = pd.DataFrame(dados_extraidos)

# Exportando para um arquivo Excel
df.to_excel('municipios.xlsx', index=False)

print("Dados exportados com sucesso para 'municipios.xlsx'")