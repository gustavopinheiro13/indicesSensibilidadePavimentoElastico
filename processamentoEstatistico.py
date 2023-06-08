import json
from ColetarDados import DadosDeslocamento
import numpy as np
import pandas as pd
nome_arquivo_saida = 'dadosDeslocamento.json'
# Carrega os dados do arquivo JSON
with open(nome_arquivo_saida, 'r') as arquivo_json:
    dados_deslocamento = json.load(arquivo_json)

# Converte os dados para um dataframe
df = pd.DataFrame(dados_deslocamento)

# Exibe o dataframe
print(df)