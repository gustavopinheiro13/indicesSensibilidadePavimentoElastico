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
# Classe DadosDeslocamento para armazenar informacoes de deslocamento
class DadosDeslocamento:
    # Construtor para inicializar os atributos da classe
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

# Funcao para importar os dados do arquivo JSON e criar um DataFrame
def importarJson(nome_arquivo):
    os.chdir("C:/Users/gusta/resultados_abaqus/")
    with open(nome_arquivo, 'r') as arquivo_json:
        dados_deslocamento = json.load(arquivo_json)
    # Importar os dados do arquivo e criar um DataFrame
    dataframe_deslocamentos_calculados = pd.DataFrame(dados_deslocamento)
    return dataframe_deslocamentos_calculados

# Funcao para calcular a variacao percentual em relacao ao valor anterior de u3
def calcular_variacao_percentual(group):
    if pd.api.types.is_numeric_dtype(group['u3']):
        group['variacao_percentual_u3'] = (group['u3'] - group['u3'].shift(1)) / group['u3'].shift(1) * 100
    return group

# Nome do arquivo JSON
nome_arquivo = 'dadosModelosSaidaPrincipais.json'

def dataframeVariacaoPercentual(dataframe_deslocamentos_calculados):
    # Agrupa os dados pelo modelo do aviao, nome de sensibilidade e numero do no
    grupos = dataframe_deslocamentos_calculados.groupby(['modeloAviao', 'nomeSensibilidade', 'no'])
    
    dataframesDiscretizadosModeloNomeNo = []
    # Itera sobre cada grupo de dados
    for grupo, dados_grupo in grupos:
        dataframe_separado = dados_grupo.copy()  # Crie uma copia do DataFrame do grupo
        # Adicione o DataFrame separado a lista de DataFrames separados
        dataframesDiscretizadosModeloNomeNo.append(dataframe_separado)
    
    # Calcula a variacao percentual para cada DataFrame no formato de lista
    for deformacao in range(len(dataframesDiscretizadosModeloNomeNo)):
        dataframesDiscretizadosModeloNomeNo[deformacao] = calcular_variacao_percentual(dataframesDiscretizadosModeloNomeNo[deformacao])
    
    # Concatena os DataFrames individuais de variacao percentual e remove valores NaN
    dfConcatenadoComVariacaoPercentual = pd.concat(dataframesDiscretizadosModeloNomeNo, ignore_index=True).dropna(subset=['variacao_percentual_u3'])
    
    # Seleciona as colunas relevantes do DataFrame final
    dfConcatenadoComVariacaoPercentual = dfConcatenadoComVariacaoPercentual[['modeloAviao', 'nomeSensibilidade', 'variacao_percentual_u3']]
    
    return dfConcatenadoComVariacaoPercentual


def iniciarProcessamentoEstatitico(nome_arquivo):
    # Carrega os dados do arquivo JSON
    dataframe_deslocamentos_calculados = importarJson(nome_arquivo)
    filtro = ((dataframe_deslocamentos_calculados['modeloAviao'] == 'B737800')& (dataframe_deslocamentos_calculados['no'] == 55)) | ((dataframe_deslocamentos_calculados['modeloAviao'] == 'B767300')& (dataframe_deslocamentos_calculados['no'] == 0)) | ((dataframe_deslocamentos_calculados['modeloAviao'] == 'B777300')& (dataframe_deslocamentos_calculados['no'] == 47))
    dataframe_deslocamentos_filtrados = dataframe_deslocamentos_calculados[filtro]
    dfConcatenadoComVariacaoPercentual = dataframeVariacaoPercentual(dataframe_deslocamentos_filtrados)
    dfConcatenadoComVariacaoPercentual.to_csv('variacao_percentual_u3.csv', index=False, sep=';', decimal=',')
    #Teste de Shapiro-Wilk para normalidade e teste de Levene para homogeneidade de variancias
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

    # Para cada grupo, criar o DataFrame pivotado e adicionar a lista
    for _, grupo in grupos:
        dataframe_pivotado = grupo.pivot(columns='nomeSensibilidade', values='variacao_percentual_u3')
        dataframes_pivotados.append(dataframe_pivotado.reset_index())

    # Concatenar todos os DataFrames em um unico DataFrame
    dataframe_resultante = pd.concat(dataframes_pivotados, ignore_index=False, axis=1).drop('index', axis=1)

    return dataframe_resultante

# Funcao para descrever e visualizar os dados
def descreverDados(nome_arquivo):
    # Importar dados e calcular variacao percentual
    dataframe_deslocamentos_calculados = importarJson(nome_arquivo)
    filtro = ((dataframe_deslocamentos_calculados['modeloAviao'] == 'B737800')& (dataframe_deslocamentos_calculados['no'] == 55)) | ((dataframe_deslocamentos_calculados['modeloAviao'] == 'B767300')& (dataframe_deslocamentos_calculados['no'] == 0)) | ((dataframe_deslocamentos_calculados['modeloAviao'] == 'B777300')& (dataframe_deslocamentos_calculados['no'] == 47))
    dataframe_deslocamentos_filtrados = dataframe_deslocamentos_calculados[filtro]
    for aviao in dataframe_deslocamentos_filtrados['modeloAviao'].tolist():
        dataframe_deslocamentos_filtrados_por_aviao = dataframe_deslocamentos_filtrados[(dataframe_deslocamentos_filtrados['modeloAviao'] == aviao)]
        dfConcatenadoComVariacaoPercentual = dataframeVariacaoPercentual(dataframe_deslocamentos_filtrados_por_aviao)
        dataframeAmostraTransposto = transformar_para_dataframe_transposto(dfConcatenadoComVariacaoPercentual)
        
        # Plotar graficos de dispersao para cada coluna
        plt.figure(figsize=(10, 6))  # Define o tamanho da figura
        cores = np.random.rand(len(dataframeAmostraTransposto.columns), 3)
        plt.figure(figsize=(10, 6))  # Define o tamanho da figura
        plt.style.use('seaborn-whitegrid')  # Estilo de fundo com grid
        
        # Plotar graficos de dispersao para cada coluna separadamente
        for i, coluna in enumerate(dataframeAmostraTransposto.columns):
            nomeFigura = f'Grafico de Pontos para {coluna} em {aviao}'
            plt.figure()  # Cria uma nova figura para cada coluna
            plt.scatter(dataframeAmostraTransposto.index, dataframeAmostraTransposto[coluna], color=cores[i], alpha=0.7, s=10)
            plt.xlabel('indice')
            plt.ylabel(coluna)
            plt.title(nomeFigura)
            #plt.gcf().canvas.set_window_title(nomeFigura)
            plt.grid(True)
            plt.tight_layout()  # Melhorar a disposicao dos elementos no grafico
            plt.savefig(nomeFigura.title().replace(" ", ""), dpi=300)
    plt.show()

    return []


# Funcao para realizar o teste de Levene
def teste_levene(col1, col2):
    estatistica, p_valor = stats.levene(col1, col2)
    return estatistica, p_valor

# Funcao para realizar o teste de Shapiro-Wilk
def teste_shapiro_wilk(coluna):
    estatistica, p_valor = stats.shapiro(coluna)
    return estatistica, p_valor

# Funcao para aceitar ou rejeitar a hipotese nula
def aceitar_rejeitar(p_valor):
    return p_valor > 0.05

# Funcao para testar as premissas do teste de Tukey
def tukey_premissas_teste(dados):
    # Premissa 1: Amostras independentes e aleatorias
    # Premissa 2: Normalidade das populacoes subjacentes
    # Iterando sobre as colunas e aplicando o teste de Shapiro-Wilk
    resultadosShapiro = []
    for coluna in dados.columns:
        estatistica, p_valor = teste_shapiro_wilk(dados[coluna].dropna())
        resultadosShapiro.append({'Coluna': coluna, 'Estatistica do teste': estatistica, 'Valor-p': p_valor, 'Aceita H0': aceitar_rejeitar(p_valor)})

    # Premissa 3: Homogeneidade das variancias
    resultadosLevine = []
    for col1, col2 in combinations(dados.columns, 2):
        estatistica, p_valor = teste_levene(dados[col1].dropna(), dados[col2].dropna())
        resultado = {
            'Colunas': f"{col1} - {col2}",
            'Estatistica do teste': estatistica,
            'Valor-p': p_valor,
            'Aceita H0': aceitar_rejeitar(p_valor)
        }
        resultadosLevine.append(resultado)
    
    return resultadosShapiro, resultadosLevine

# Chamada das funcoes
iniciarProcessamentoEstatitico('DeslocamentodadosModelosSaidaPrincipais.json')
descreverDados('DeslocamentodadosModelosSaidaPrincipais.json')