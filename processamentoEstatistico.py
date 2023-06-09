import json
from ColetarDados import DadosDeslocamento
import numpy as np
import pandas as pd
# Definir a classe DadosDeslocamento
# Função para importar os dados do arquivo JSON e criar a lista de objetos
def importar_dados_deslocamento(nome_arquivo: str) -> list[DadosDeslocamento]:
    lista_objetos = []
    with open(nome_arquivo, 'r') as arquivo_json:
        dados_json = json.load(arquivo_json)
        for dado in dados_json:
            objeto = DadosDeslocamento(
                dado['nomeJob'],
                dado['nomeStep'],
                dado['nomeSensibilidade'],
                dado['valorSensibilidade'],
                dado['modeloAviao'],
                dado['no'],
                dado['u1'],
                dado['u2'],
                dado['u3']
            )
            lista_objetos.append(objeto)
    return lista_objetos

# Nome do arquivo JSON
nome_arquivo = 'dadosDeslocamento.json'

# Carrega os dados do arquivo JSON
with open(nome_arquivo, 'r') as arquivo_json:
    dados_deslocamento = json.load(arquivo_json)

# Importar os dados do arquivo e criar a lista de objetos DadosDeslocamento
lista_deslocamentos_calculados = importar_dados_deslocamento(nome_arquivo)
dataframe_deslocamentos_calculados = pd.DataFrame(dados_deslocamento)
print(dataframe_deslocamentos_calculados)