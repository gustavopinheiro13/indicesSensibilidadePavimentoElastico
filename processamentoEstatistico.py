import json
#from ColetarDados import DadosDeslocamento
import numpy as np
import pandas as pd
from scipy import stats
class DadosDeslocamento:
    def __init__(self, nomeJob, nomeStep, nomeSensibilidade, valorSensibilidade, modeloAviao, noInteresse, u1, u2, u3):
        self.nomeJob = nomeJob
        self.nomeStep = nomeStep
        self.nomeSensibilidade = nomeSensibilidade
        self.valorSensibilidade = valorSensibilidade
        self.modeloAviao = modeloAviao
        self.no = noInteresse
        self.u1 = u1
        self.u2 = u2
        self.u3 = u3
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
def calcular_variacao_percentual(group):
    if pd.api.types.is_numeric_dtype(group['u3']):
        group['variacao_percentual_u3'] = (group['u3'] - group['u3'].shift(1)) / group['u3'].shift(1) * 100
    return group

#df = dataframe_deslocamentos_calculados.groupby(['modeloAviao','nomeSensibilidade', 'no']).apply(calcular_variacao_percentual)
#df.reset_index('modeloAviao', inplace=True)  # Remove 'modeloAviao' do índice

grupos = dataframe_deslocamentos_calculados.groupby(['modeloAviao','nomeSensibilidade', 'no'])

dataframes_separados = []
for grupo, dados_grupo in grupos:
    dataframe_separado = dados_grupo.copy()  # Crie uma cópia do dataframe do grupo
    
    # Faça outras manipulações necessárias no dataframe separado
    
    # Adicione o dataframe separado à lista de dataframes separados
    dataframes_separados.append(dataframe_separado)

for i in range(len(dataframes_separados)):
    dataframes_separados[i] = calcular_variacao_percentual(dataframes_separados[i])

#Teste
#t_statistic, p_value = stats.ttest_ind(np.ma.masked_invalid( pd.Series(df['variacao_percentual_u3'].tolist()).dropna().tolist()), np.ma.masked_invalid( pd.Series(df['variacao_percentual_u3'].tolist()).dropna().tolist()))
#print(np.ma.masked_invalid( pd.Series(df['variacao_percentual_u1'].tolist()).dropna().tolist()))
#print(t_statistic.tolist(), print(p_value.tolist()))
#print(dataframe_deslocamentos_calculados)