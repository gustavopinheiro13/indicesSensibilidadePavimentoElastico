import json
import pandas as pd
import os
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 


# Funcao para importar os dados do arquivo JSON e criar um DataFrame
def importarJson(nome_arquivo):
    os.chdir("C:/Users/gusta/resultados_abaqus/")
    with open(nome_arquivo, 'r') as arquivo_json:
        dados = json.load(arquivo_json)
    # Importar os dados do arquivo e criar um DataFrame
    dataframe_calculado = pd.DataFrame(dados)
    return dataframe_calculado

def calcular_variacao_percentual(group, nome_csv, variavel_avaliada):
    if pd.api.types.is_numeric_dtype(group[variavel_avaliada]):
        group[nome_csv] = ((group[variavel_avaliada] - group[variavel_avaliada].shift(1)) / group[variavel_avaliada].shift(1)) * 100
    return group

# Nome do arquivo JSON
nome_arquivo = 'dadosModelosSaidaPrincipais.json'

def dataframeVariacaoPercentual(dataframe_calculado, nome_csv, variavel_avaliada):
    # Agrupa os dados pelo modelo do aviao, nome de sensibilidade e numero do no
    grupos = dataframe_calculado.groupby(['modeloAviao', 'no'])
    
    dataframesDiscretizadosModeloNomeNo = []
    # Itera sobre cada grupo de dados
    for grupo, dados_grupo in grupos:
        dataframe_separado = dados_grupo.copy()  # Crie uma copia do DataFrame do grupo
        # Adicione o DataFrame separado a lista de DataFrames separados
        dataframesDiscretizadosModeloNomeNo.append(dataframe_separado)
    
    # Calcula a variacao percentual para cada DataFrame no formato de lista
    for deformacao in range(len(dataframesDiscretizadosModeloNomeNo)):
        dataframesDiscretizadosModeloNomeNo[deformacao] = calcular_variacao_percentual(dataframesDiscretizadosModeloNomeNo[deformacao], nome_csv=nome_csv, variavel_avaliada = variavel_avaliada)
    # Concatena os DataFrames individuais de variacao percentual e remove valores NaN
    dfConcatenadoComVariacaoPercentual = pd.concat(dataframesDiscretizadosModeloNomeNo, ignore_index=True).dropna(subset=[nome_csv])
    # Seleciona as colunas relevantes do DataFrame final
    dfConcatenadoComVariacaoPercentual = dfConcatenadoComVariacaoPercentual[['modeloAviao', 'nomeSensibilidade', 'valorSensibilidade', nome_csv]]
    
    return dfConcatenadoComVariacaoPercentual

# Função para calcular estatísticas de bootstrap
def bootstrap_test_group(data1, data2, statistic, n_iterations=100000, alpha=0.05):
    # Realiza o bootstrap e calcula a estatística de interesse para dois grupos
    bootstrap_statistics = []
    n1, n2 = len(data1), len(data2)
    for _ in range(n_iterations):
        sample1 = np.random.choice(data1, n1, replace=True)
        sample2 = np.random.choice(data2, n2, replace=True)
        statistic1 = statistic(sample1)  # Estatística de interesse para o grupo 1
        statistic2 = statistic(sample2)  # Estatística de interesse para o grupo 2
        bootstrap_statistics.append(statistic1 - statistic2)  # Diferença das estatísticas

    # Calcula intervalo de confiança (1 - alpha)
    lower_bound = np.percentile(bootstrap_statistics, 100 * alpha / 2)
    upper_bound = np.percentile(bootstrap_statistics, 100 * (1 - alpha / 2))

    return np.mean(bootstrap_statistics), lower_bound, upper_bound


def iniciarProcessamentoEstatistico(nome_arquivo, variavel_avaliada):
    # Carrega os dados do arquivo JSON
    nome_csv = 'variacao_percentual_'+ variavel_avaliada
    dataframe_calculado = importarJson(nome_arquivo)
    filtro = ((dataframe_calculado['modeloAviao'] == 'B737800')& (dataframe_calculado['no'] == 55)) | ((dataframe_calculado['modeloAviao'] == 'B767300')& (dataframe_calculado['no'] == 0)) | ((dataframe_calculado['modeloAviao'] == 'B777300')& (dataframe_calculado['no'] == 47))
    dataframe_filtrado = dataframe_calculado[filtro]
    dfConcatenadoComVariacaoPercentual = dataframeVariacaoPercentual(dataframe_filtrado, nome_csv, variavel_avaliada = variavel_avaliada)
    dfConcatenadoComVariacaoPercentual.to_csv(nome_csv + '.csv', index=False, sep=';', decimal=',')
    # Lista de modelos de avião
    modelos_aviao = dfConcatenadoComVariacaoPercentual['modeloAviao'].unique().tolist()

    # Inicializa uma lista para armazenar os resultados
    resultados = []

    # Calcula as estatísticas para cada modelo de avião
    for aviao in modelos_aviao:
        # Filtra o DataFrame para o modelo de avião atual
        df_modelo = dfConcatenadoComVariacaoPercentual[dfConcatenadoComVariacaoPercentual['modeloAviao'] == aviao]

        # Lista de grupos
        grupos = df_modelo['nomeSensibilidade'].unique().tolist()

        # Calcula as estatísticas para cada par de grupos
        for grupo1, grupo2 in combinations(grupos, 2):
            media_diff, lower_bound, upper_bound = bootstrap_test_group(
                df_modelo[df_modelo['nomeSensibilidade'] == grupo1][nome_csv],
                df_modelo[df_modelo['nomeSensibilidade'] == grupo2][nome_csv],
                statistic=np.mean,  # Estatística é a média
                alpha=0.05  # Alpha para o intervalo de confiança de 95%
            )
            # Decide se rejeita ou não a hipótese nula
            rejeitar = (lower_bound > 0) or (upper_bound < 0)

            # Adiciona os resultados à lista
            resultados.append([grupo1, grupo2, media_diff, lower_bound, upper_bound, rejeitar, aviao])

    # Cria um DataFrame com os resultados
    df_resultadosBootstrap = pd.DataFrame(resultados, columns=['grupo 1', 'grupo 2', 'diferenca_media', 'media_inferior', 'media_superior', 'rejeitar', 'modeloAviao'])
    resultados_estatistica_bootstrap = []
    for aviao in df_resultadosBootstrap['modeloAviao'].unique().tolist():
        df_filtrado = df_resultadosBootstrap.loc[df_resultadosBootstrap['modeloAviao'] == aviao]
        # Ordenando os resultados por meandiffs em ordem decrescente
        df_filtrado['diferenca_media_absoluta'] = df_filtrado['diferenca_media'].abs()
        df_filtrado = df_filtrado.sort_values(by='diferenca_media_absoluta', ascending=False)
        df_filtrado = df_filtrado.drop(columns=['diferenca_media_absoluta'])
        df_filtrado.to_csv('resultadosBootstrap_' + aviao + '.csv', index=False, sep=';', decimal='.')
        resultados_estatistica_bootstrap.append(df_filtrado)
    print(resultados_estatistica_bootstrap)


# Funcao para descrever e visualizar os dados
def descreverDados(nome_arquivo, variavel_avaliada):
    nome_csv = 'variacao_percentual_' + variavel_avaliada
    sns.set_context('notebook')
    # Importar dados e calcular variacao percentual
    dataframe_calculado = importarJson(nome_arquivo)
    filtro = ((dataframe_calculado['modeloAviao'] == 'B737800')& (dataframe_calculado['no'] == 55)) | ((dataframe_calculado['modeloAviao'] == 'B767300')& (dataframe_calculado['no'] == 0)) | ((dataframe_calculado['modeloAviao'] == 'B777300')& (dataframe_calculado['no'] == 47))
    dataframe_filtrado = dataframe_calculado[filtro]
    dataframe_filtrado['valorSensibilidade'] = pd.to_numeric(dataframe_filtrado['valorSensibilidade'], errors='raise')
    for aviao in dataframe_filtrado['modeloAviao'].unique().tolist():
        dataframe_filtradoo_por_aviao = dataframe_filtrado[(dataframe_filtrado['modeloAviao'] == aviao)]
        for sensibilidade in dataframe_filtradoo_por_aviao['nomeSensibilidade'].unique().tolist():
            if sensibilidade != "Base":
                dataframe_filtrado_por_sensibilidade = dataframe_filtradoo_por_aviao[(dataframe_filtradoo_por_aviao['nomeSensibilidade'] == sensibilidade)]
                # dfConcatenadoComVariacaoPercentual = dataframeVariacaoPercentual(pd.concat([caso_base, dataframe_filtrado_por_sensibilidade],ignore_index=True) )
                dfConcatenadoComVariacaoPercentual = dataframeVariacaoPercentual(dataframe_filtrado_por_sensibilidade, nome_csv, variavel_avaliada = variavel_avaliada)
                nomeFigura = f'Gráfico de pontos para {sensibilidade} no {aviao}'
                nomeFiguraArquivo = f'Grafico de pontos para {sensibilidade} no {aviao}'
                #plt.figure()  # Cria uma nova figura para cada coluna
                cores = np.random.rand(1,3)
                plt.scatter(dfConcatenadoComVariacaoPercentual['valorSensibilidade'], dfConcatenadoComVariacaoPercentual[nome_csv], color=cores, alpha=0.7, s=10)
                unidadeSensibilidade = {'carregamento': 'Pa', 'elasBas': 'Pa', 'elasRev': 'Pa', 'elasSub': 'Pa', 'espBas': 'm', 'espRev': 'm', 'poiBas': '', 'poiRev': '', 'poiSub': '' }
                if unidadeSensibilidade[sensibilidade] == '':
                    plt.xlabel(sensibilidade)
                else:
                    plt.xlabel(sensibilidade + ' (' + unidadeSensibilidade[sensibilidade]+ ')' )
                plt.ylabel("Variação percentual (%)")

                plt.title(nomeFigura)
                plt.grid(True)
                plt.tight_layout()  # Melhorar a disposicao dos elementos no grafico
                plt.ticklabel_format(style='plain', axis='y')
                sns.set_style('whitegrid')
                plt.savefig(nomeFiguraArquivo.title().replace(" ", ""), dpi=300)
                plt.close()
                print(aviao + " " + sensibilidade + " OK")
            # Plotar graficos de dispersao para cada coluna separadamente
    #plt.show()        
    return []


# # Chamada das funcoes deslocamento
# iniciarProcessamentoEstatistico('DeslocamentodadosModelosSaidaPrincipais.json', variavel_avaliada = 'u3')
# descreverDados('DeslocamentodadosModelosSaidaPrincipais.json', variavel_avaliada = 'u3')

# Chamada das funcoes deformacao
iniciarProcessamentoEstatistico('DeformacaodadosModelosSaidaPrincipais.json', variavel_avaliada = 'e3')
# descreverDados('DeformacaodadosModelosSaidaPrinc\ipais.json', variavel_avaliada = 'e3')
#Consertar os graficos para mostrarrem tambem o valor da sensibilidade, ficar valor da sensibilidade e variacao percentual