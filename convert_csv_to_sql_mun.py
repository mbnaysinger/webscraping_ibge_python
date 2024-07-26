import csv
import os

# Caminho do arquivo CSV
csv_file_path = os.path.join(os.path.dirname(__file__), 'mun_siafi.csv')

# Caminho do arquivo SQL de saída
sql_file_path = os.path.join(os.path.dirname(__file__), 'municipios.sql')

# Nome da tabela
table_name = 'siafi'

# Função para substituir espaços e quebras de linha por backspaces
def replace_spaces_and_line_feeds(text):
    return text.replace('\n', '\b').replace("'", "''")

# Função para remover BOM de uma string
def remove_bom(text):
    return text.lstrip('\ufeff')

# Função para gerar comandos SQL a partir do CSV
def generate_sql_from_csv(csv_path, sql_path, table_name):
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            # Ler a primeira linha para verificar e remover o BOM, se presente
            first_line = csv_file.readline()
            if first_line.startswith('\ufeff'):
                first_line = remove_bom(first_line)
            
            # Reposicionar o ponteiro do arquivo para o início
            csv_file.seek(0)
            csv_reader = csv.DictReader(csv_file)
            
            # Substituir o cabeçalho 'uf' removendo o BOM
            csv_reader.fieldnames = [remove_bom(field) for field in csv_reader.fieldnames]
            
            # Verificar e exibir cabeçalhos
            headers = csv_reader.fieldnames
            print(f"Cabeçalhos encontrados: {headers}")
            
            # Verificar se os cabeçalhos esperados estão presentes
            expected_headers = ['cod_ibge', 'cod_siafi', 'nome', 'uf', 'microrregiao', 'mesorregiao']
            for header in expected_headers:
                if header not in headers:
                    raise ValueError(f"Cabeçalho esperado '{header}' não encontrado no arquivo CSV.")
            
            with open(sql_path, mode='w', encoding='utf-8') as sql_file:
                sql_file.write("INSERT INTO municipios (cod_ibge, cod_siafi, nome, uf, microrregiao, mesorregiao) VALUES\n")
                for row in csv_reader:
                    cod_ibge = replace_spaces_and_line_feeds(row['cod_ibge'])
                    cod_siafi = replace_spaces_and_line_feeds(row['cod_siafi'])
                    nome = replace_spaces_and_line_feeds(row['nome'])
                    uf = replace_spaces_and_line_feeds(row['uf'])
                    microrregiao = replace_spaces_and_line_feeds(row['microrregiao'])
                    mesorregiao = replace_spaces_and_line_feeds(row['mesorregiao'])

                    sql_command = f"('{cod_ibge}', '{cod_siafi}', '{nome}', '{uf}', '{microrregiao}', '{mesorregiao}'),\n"
                    sql_file.write(sql_command)

        print(f"Arquivo SQL gerado com sucesso em: {sql_path}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Executar a função
generate_sql_from_csv(csv_file_path, sql_file_path, table_name)