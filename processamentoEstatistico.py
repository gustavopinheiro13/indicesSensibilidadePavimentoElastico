import json
#from ColetarDados import DadosDeslocamento
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Definir a classe DadosDeslocamento
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

dataframesDiscretizadosModeloNomeNo = []
for grupo, dados_grupo in grupos:
    dataframe_separado = dados_grupo.copy()  # Crie uma cópia do dataframe do grupo
    # Adicione o dataframe separado à lista de dataframes separados
    dataframesDiscretizadosModeloNomeNo.append(dataframe_separado)

for deformacao in range(len(dataframesDiscretizadosModeloNomeNo)):
    dataframesDiscretizadosModeloNomeNo[deformacao] = calcular_variacao_percentual(dataframesDiscretizadosModeloNomeNo[deformacao])


dfConcatenadoComVariacaoPercentual = pd.concat(dataframesDiscretizadosModeloNomeNo, ignore_index=True).dropna(subset=['variacao_percentual_u3'])
dfConcatenadoComVariacaoPercentual = dfConcatenadoComVariacaoPercentual[['modeloAviao','nomeSensibilidade','variacao_percentual_u3']]

resultadosEstatisticaTukey = []
for aviao in dfConcatenadoComVariacaoPercentual['modeloAviao'].unique().tolist():
    df_filtrado = dfConcatenadoComVariacaoPercentual.loc[dfConcatenadoComVariacaoPercentual['modeloAviao'] == aviao]
    tukey_resultado = pairwise_tukeyhsd(df_filtrado['variacao_percentual_u3'], df_filtrado['nomeSensibilidade'])
    dataframeResultadosTukey = pd.DataFrame(data=tukey_resultado._results_table.data[1:], columns=tukey_resultado._results_table.data[0])
    # Ordenando os resultados por meandiffs em ordem decrescente
    dataframeResultadosTukey['meandiff_abs'] = dataframeResultadosTukey['meandiff'].abs()
    dataframeResultadosTukey = dataframeResultadosTukey.sort_values(by='meandiff_abs', ascending=False)
    dataframeResultadosTukey = dataframeResultadosTukey.drop(columns=['meandiff_abs'])
    resultadosEstatisticaTukey.append(dataframeResultadosTukey)
print(dfConcatenadoComVariacaoPercentual['modeloAviao'].unique().tolist())
