import json
#from ColetarDados import DadosDeslocamento
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import os
import scipy.stats as stats
import statsmodels.stats.multicomp as mc
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
# Definir a classe DadosDeslocamento
class DadosDeslocamento:
    def __init__(self, nomeJob, nomeStep, nomeSensibilidade, valorSensibilidade, modeloAviao, no, u1, u2, u3):
        self.nomeJob = nomeJob
        self.nomeStep = nomeStep
        self.nomeSensibilidade = nomeSensibilidade
        self.valorSensibilidade = valorSensibilidade
        self.modeloAviao = modeloAviao
        self.no = no
        self.u1 = u1
        self.u2 = u2
        self.u3 = u3
# Funcao para importar os dados do arquivo JSON e criar a lista de objetos
def importarJson(nome_arquivo):
    os.chdir("C:/Users/gusta/resultados_abaqus/")
    with open(nome_arquivo, 'r') as arquivo_json:
        dados_deslocamento = json.load(arquivo_json)
    # Importar os dados do arquivo e criar a lista de objetos DadosDeslocamento
    dataframe_deslocamentos_calculados = pd.DataFrame(dados_deslocamento)
    return dataframe_deslocamentos_calculados

def calcular_variacao_percentual(group):
    if pd.api.types.is_numeric_dtype(group['u3']):
        group['variacao_percentual_u3'] = (group['u3'] - group['u3'].shift(1)) / group['u3'].shift(1) * 100
    return group
# Nome do arquivo JSON

def dataframeVariacaoPercentual(dataframe_deslocamentos_calculados):
    grupos = dataframe_deslocamentos_calculados.groupby(['modeloAviao','nomeSensibilidade', 'no'])
    dataframesDiscretizadosModeloNomeNo = []
    for grupo, dados_grupo in grupos:
        dataframe_separado = dados_grupo.copy()  # Crie uma copia do dataframe do grupo
        # Adicione o dataframe separado a lista de dataframes separados
        dataframesDiscretizadosModeloNomeNo.append(dataframe_separado)
    for deformacao in range(len(dataframesDiscretizadosModeloNomeNo)):
        dataframesDiscretizadosModeloNomeNo[deformacao] = calcular_variacao_percentual(dataframesDiscretizadosModeloNomeNo[deformacao])
    dfConcatenadoComVariacaoPercentual = pd.concat(dataframesDiscretizadosModeloNomeNo, ignore_index=True).dropna(subset=['variacao_percentual_u3'])
    dfConcatenadoComVariacaoPercentual = dfConcatenadoComVariacaoPercentual[['modeloAviao','nomeSensibilidade','variacao_percentual_u3']]
    return dfConcatenadoComVariacaoPercentual

def iniciarProcessamentoEstatitico(nome_arquivo):
    # Carrega os dados do arquivo JSON
    dataframe_deslocamentos_calculados = importarJson(nome_arquivo)
    dfConcatenadoComVariacaoPercentual = dataframeVariacaoPercentual(dataframe_deslocamentos_calculados)
    dfConcatenadoComVariacaoPercentual.to_csv('variacao_percentual_u3.csv', index=False, sep=';', decimal=',')
    #Teste de Shapiro-Wilk para normalidade e teste de Levene para homogeneidade de variâncias
    #dataframeAmostraTransposto = pd.concat([grupo.pivot(columns='nomeSensibilidade', values='variacao_percentual_u3').reset_index() for _, grupo in dfConcatenadoComVariacaoPercentual[['nomeSensibilidade','variacao_percentual_u3']].groupby('nomeSensibilidade', as_index=False)], ignore_index=False, axis=1).drop('index', axis=1)
    dataframeAmostraTransposto = transformar_para_dataframe_transposto(dfConcatenadoComVariacaoPercentual)
    verificacaoPremissasTukey = tukey_premissas_teste(dataframeAmostraTransposto)
    pd.DataFrame(verificacaoPremissasTukey[0]).to_csv('premissasTukeyShapiro.csv', index=False, sep=';', decimal=',')
    pd.DataFrame(verificacaoPremissasTukey[1]).to_csv('premissasTukeyLevine.csv', index=False, sep=';', decimal=',')
    resultadosEstatisticaTukey = []
    for aviao in dfConcatenadoComVariacaoPercentual['modeloAviao'].unique().tolist():
        df_filtrado = dfConcatenadoComVariacaoPercentual.loc[dfConcatenadoComVariacaoPercentual['modeloAviao'] == aviao]
        tukey_resultado = pairwise_tukeyhsd(df_filtrado['variacao_percentual_u3'], df_filtrado['nomeSensibilidade'])
        dataframeResultadosTukey = pd.DataFrame(data=tukey_resultado._results_table.data[1:], columns=tukey_resultado._results_table.data[0])
        # Ordenando os resultados por meandiffs em ordem decrescente
        dataframeResultadosTukey['meandiff_abs'] = dataframeResultadosTukey['meandiff'].abs()
        dataframeResultadosTukey = dataframeResultadosTukey.sort_values(by='meandiff_abs', ascending=False)
        dataframeResultadosTukey = dataframeResultadosTukey.drop(columns=['meandiff_abs'])
        dataframeResultadosTukey.to_csv('resultadosTukey_' + aviao + '.csv', index=False, sep=';', decimal='.')
        resultadosEstatisticaTukey.append(dataframeResultadosTukey)
        # Teste de durbin watson para independencia de amostras     
    print(dfConcatenadoComVariacaoPercentual['modeloAviao'].unique().tolist())



def transformar_para_dataframe_transposto(df):
    # Criar uma lista para armazenar os DataFrames pivotados de cada grupo
    dataframes_pivotados = []

    # Agrupar o DataFrame original pela coluna 'nomeSensibilidade'
    grupos = df.groupby('nomeSensibilidade')

    # Para cada grupo, criar o DataFrame pivotado e adicionar à lista
    for _, grupo in grupos:
        dataframe_pivotado = grupo.pivot(columns='nomeSensibilidade', values='variacao_percentual_u3')
        dataframes_pivotados.append(dataframe_pivotado.reset_index())

    # Concatenar todos os DataFrames em um único DataFrame
    dataframe_resultante = pd.concat(dataframes_pivotados, ignore_index=False, axis=1).drop('index', axis=1)

    return dataframe_resultante


def descreverDados(nome_arquivo):
    dataframe_deslocamentos_calculados = importarJson(nome_arquivo)
    dfConcatenadoComVariacaoPercentual = dataframeVariacaoPercentual(dataframe_deslocamentos_calculados)
    #dataframeAmostraTransposto = pd.concat([grupo.pivot(columns='nomeSensibilidade', values='variacao_percentual_u3').reset_index() for _, grupo in dfConcatenadoComVariacaoPercentual[['nomeSensibilidade','variacao_percentual_u3']].groupby('nomeSensibilidade', as_index=False)], ignore_index=False, axis=1).drop('index', axis=1)
    dataframeAmostraTransposto = transformar_para_dataframe_transposto(dfConcatenadoComVariacaoPercentual)
    # Plotar cada coluna em um gráfico de pontos
    plt.figure(figsize=(10, 6))  # Define o tamanho da figura

    # Plotar cada coluna em um gráfico de pontos com layout aprimorado
    # Gerar cores aleatórias para cada gráfico
    cores = np.random.rand(len(dataframeAmostraTransposto.columns), 3)

    # Plotar cada coluna em um gráfico de pontos separado com cores diferentes
    plt.figure(figsize=(10, 6))  # Define o tamanho da figura
    plt.style.use('seaborn-whitegrid')  # Estilo de fundo com grid

    for i, coluna in enumerate(dataframeAmostraTransposto.columns):
        plt.figure()  # Cria uma nova figura para cada coluna
        plt.scatter(dataframeAmostraTransposto.index, dataframeAmostraTransposto[coluna], color=cores[i], alpha=0.7, s=10)
        plt.xlabel('Índice')
        plt.ylabel(coluna)
        plt.title(f'Gráfico de Pontos para a Coluna {coluna}')
        plt.grid(True)
        plt.tight_layout()  # Melhorar a disposição dos elementos no gráfico
    plt.show()

    return []

def teste_levene(col1, col2):
    estatistica, p_valor = stats.levene(col1, col2)
    return estatistica, p_valor

def teste_shapiro_wilk(coluna):
    estatistica, p_valor = stats.shapiro(coluna)
    return estatistica, p_valor

def aceitar_rejeitar(p_valor):
    return p_valor > 0.05

def tukey_premissas_teste(dados):
    # Premissa 1: Amostras independentes e aleatórias
    # Premissa 2: Normalidade das populações subjacentes`
    # Iterando sobre as colunas e aplicando o teste de Shapiro-Wilk
    # Criar um DataFrame vazio para armazenar os resultados
    resultadosLevine = []
    resultadosShapiro = []#pd.DataFrame(columns=['Coluna', 'Estatística do teste', 'Valor-p'])
    for coluna in dados.columns:
        estatistica, p_valor = teste_shapiro_wilk(dados[coluna].dropna())
        resultadosShapiro.append({'Coluna': coluna, 'Estatística do teste': estatistica, 'Valor-p': p_valor, 'Aceita H0': aceitar_rejeitar(p_valor)})
    print("Hello World")
    # Premissa 3: Homogeneidade das variâncias
    # _, p_levene = stats.levene(dados.columns)
    # if p_levene < 0.05:
    #     print("Premissa 3: As variâncias não são homogêneas.")
    # else:
    #     print("Premissa 3: As variâncias são homogêneas.")
    # Iterando sobre as colunas e aplicando o teste de Levene
    for col1, col2 in combinations(dados.columns, 2):
        estatistica, p_valor = teste_levene(dados[col1].dropna(), dados[col2].dropna())
        resultado = {
            'Colunas': f"{col1} - {col2}",
            'Estatística do teste': estatistica,
            'Valor-p': p_valor,
            'Aceita H0': aceitar_rejeitar(p_valor)
        }
        resultadosLevine.append(resultado)
    return resultadosShapiro, resultadosLevine
iniciarProcessamentoEstatitico('DeslocamentodadosModelosSaidaPrincipais.json')
descreverDados('DeslocamentodadosModelosSaidaPrincipais.json')
