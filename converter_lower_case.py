import csv
import tempfile
import shutil
import os

def converter_csv_para_minusculas(input_file):
    # Criar um arquivo temporário para escrever as mudanças
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8')
    temp_file_name = temp_file.name

    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile, temp_file:
        reader = csv.reader(csvfile)
        writer = csv.writer(temp_file)

        # Converter cada linha para minúsculas e escrever no arquivo temporário
        for row in reader:
            row = [cell.lower() for cell in row]
            writer.writerow(row)

    # Substituir o arquivo original pelo temporário
    shutil.move(temp_file_name, input_file)

# Exemplo de uso
input_file = './dados/orgaos_prefeitura_fortaleza.csv'  # Nome do seu arquivo CSV de entrada

converter_csv_para_minusculas(input_file)
