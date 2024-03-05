# Importando bibliotecas necessarias
import json
import pandas as pd
import os
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
import math

# Funcao para importar os dados do arquivo JSON e criar um DataFrame
def importarJson(nome_arquivo):
    # Alterando o diretorio de trabalho para a pasta de resultados
    os.chdir("C:/Users/gusta/resultados_abaqus/")
    with open(nome_arquivo, 'r') as arquivo_json:
        dados = json.load(arquivo_json)
    # Importando os dados do arquivo e criando um DataFrame
    dataframe_calculado = pd.DataFrame(dados)
    return dataframe_calculado

# Funcao para calcular a variacao percentual em um grupo de dados
def calcular_variacao_percentual(group, nome_csv, variavel_avaliada):
    if pd.api.types.is_numeric_dtype(group[variavel_avaliada]):
        group[nome_csv] = ((group[variavel_avaliada] - group[variavel_avaliada].shift(1)) / group[variavel_avaliada].shift(1)) * 100
    return group

# Nome do arquivo JSON
nome_arquivo = 'dadosModelosSaidaPrincipais.json'

def analise_quantitativa(vetor, nome_Propriedade, nome_aeronave):
    # Cria um dicionário com os resultados
    resultados = {
        'Media': np.mean(vetor),
        'Desvio Padrao': np.std(vetor),
        'Minimo': np.min(vetor),
        'Maximo': np.max(vetor),
        'quartil_25%': np.percentile(vetor, 25),
        'Mediana': np.median(vetor),
        'quartil_75%': np.percentile(vetor, 75),
        'nome_Propriedade': nome_Propriedade,
        'nome_aeronave': nome_aeronave
    }
    # Cria um DataFrame a partir do dicionário
    df_resultados = pd.DataFrame(resultados, index=[0])
    return df_resultados

# Funcao para criar um DataFrame de variacao percentual
def dataframeVariacaoPercentual(dataframe_calculado, nome_csv, variavel_avaliada):
    # Agrupa os dados pelo modelo do aviao, nome de Propriedade e numero do no
    grupos = dataframe_calculado.groupby(['modeloAviao', 'no'])
    
    dataframesDiscretizadosModeloNomeNo = []
    # Itera sobre cada grupo de dados
    for grupo, dados_grupo in grupos:
        dataframe_separado = dados_grupo.copy()  # Crie uma copia do DataFrame do grupo
        # Adicione o DataFrame separado a lista de DataFrames separados
        dataframesDiscretizadosModeloNomeNo.append(dataframe_separado)
    
    # Calcula a variacao percentual para cada DataFrame na forma de lista
    for deformacao in range(len(dataframesDiscretizadosModeloNomeNo)):
        dataframesDiscretizadosModeloNomeNo[deformacao] = calcular_variacao_percentual(dataframesDiscretizadosModeloNomeNo[deformacao], nome_csv=nome_csv, variavel_avaliada=variavel_avaliada)
    # Concatena os DataFrames individuais de variacao percentual e remove valores NaN
    dfConcatenadoComVariacaoPercentual = pd.concat(dataframesDiscretizadosModeloNomeNo, ignore_index=True).dropna(subset=[nome_csv])
    # Seleciona as colunas relevantes do DataFrame final
    dfConcatenadoComVariacaoPercentual = dfConcatenadoComVariacaoPercentual[['modeloAviao', 'nomePropriedade', 'valorPropriedade', nome_csv]]
    
    return dfConcatenadoComVariacaoPercentual

# Funcao para calcular estatisticas de bootstrap
def bootstrap_test_group(data1, data2, statistic, tamanho_subamostragem=0.75, n_iterations = 100000, alpha=0.05, paired=False):
    # Realiza o bootstrap e calcula a estatistica de interesse para dois grupos
    # inversao_valores_medias = False
    diferencaMedias = []
    medias1 = []
    medias2 = []
    n1, n2 = len(data1), len(data2)
    for _ in range(n_iterations):
        amostra1 = np.random.choice(data1, math.ceil(tamanho_subamostragem * n1), replace=True)
        amostra2 = np.random.choice(data2, math.ceil(tamanho_subamostragem * n2), replace=True)
        statistic1 = statistic(amostra1)  # Estatistica de interesse para o grupo 1
        statistic2 = statistic(amostra2)  # Estatistica de interesse para o grupo 2
        medias1.append(statistic1)
        medias2.append(statistic2)
        diferencaMedias.append(statistic1 - statistic2)  # Diferenca das es tatisticas
    resultado = stats.ttest_ind(medias1, medias2, equal_var=False, alternative="greater")
    intervalos_confianca = resultado.confidence_interval(confidence_level=1-alpha)
    estatistica_t, valor_p = resultado
    lower_bound = intervalos_confianca[0]
    upper_bound = intervalos_confianca[-1]
    rejeitar = estatistica_t < lower_bound
    return np.mean(medias1), np.mean(medias2), estatistica_t, lower_bound, upper_bound, valor_p, rejeitar#, inversao_valores_medias

# Funcao para filtrar outliers em um DataFrame
def filtrar_outliers(dataframe):
    # Calcula o IQR da coluna "variacao_percentual_e3"
    Q1 = dataframe["variacao_percentual_e3"].quantile(0.25)
    Q3 = dataframe["variacao_percentual_e3"].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define os limites para identificar outliers
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    # Filtra os outliers
    outliers = dataframe[(dataframe["variacao_percentual_e3"] < limite_inferior) |
                         (dataframe["variacao_percentual_e3"] > limite_superior)]
    
    # Filtra os valores sem outliers
    sem_outliers = dataframe[(dataframe["variacao_percentual_e3"] >= limite_inferior) &
                            (dataframe["variacao_percentual_e3"] <= limite_superior)]
    
    return sem_outliers, outliers

# Funcao para iniciar o processamento estatistico dos dados
def iniciarProcessamentoEstatistico(nome_arquivo, variavel_avaliada, alpha, quantidadeSimulacoes):
    # Carrega os dados do arquivo JSON
    nome_csv = 'variacao_percentual_'+ variavel_avaliada
    dataframe_calculado = importarJson(nome_arquivo)
    filtro = ((dataframe_calculado['modeloAviao'] == 'B737800')& (dataframe_calculado['no'] == 55)) | ((dataframe_calculado['modeloAviao'] == 'B767300')& (dataframe_calculado['no'] == 0)) | ((dataframe_calculado['modeloAviao'] == 'B777300')& (dataframe_calculado['no'] == 47))
    dataframe_filtrado = dataframe_calculado[filtro]
    dfConcatenadoComVariacaoPercentual = dataframeVariacaoPercentual(dataframe_filtrado, nome_csv, variavel_avaliada = variavel_avaliada)
    dfConcatenadoComVariacaoPercentual_sem_outliers, dfConcatenadoComVariacaoPercentual_outliers = filtrar_outliers(dfConcatenadoComVariacaoPercentual)
    dfConcatenadoComVariacaoPercentual.to_csv(nome_csv + '.csv', index=False, sep=';', decimal=',')
    dfConcatenadoComVariacaoPercentual_sem_outliers.to_csv(nome_csv + '_sem_outliers.csv', index=False, sep=';', decimal=',')
    dfConcatenadoComVariacaoPercentual_outliers.to_csv(nome_csv + '_outliers.csv', index=False, sep=';', decimal=',')
    # Lista de modelos de aviao
    modelos_aviao = dfConcatenadoComVariacaoPercentual['modeloAviao'].unique().tolist()
    nomesPropriedades = dfConcatenadoComVariacaoPercentual['nomePropriedade'].unique().tolist()

    # Inicializa uma lista para armazenar os resultados
    resultadosBootstrapEntrePropriedades = []
    resultadosBootstrapEntreAvioes = []

    # Calcula as estatisticas para cada modelo de aviao
    for aviao in modelos_aviao:
        # Filtra o DataFrame para o modelo de aviao atual
        df_modelo = dfConcatenadoComVariacaoPercentual[dfConcatenadoComVariacaoPercentual['modeloAviao'] == aviao]
        inverter_valores_medias = False
        # Lista de grupos

        # Calcula as estatisticas para cada par de grupos
        for grupo1, grupo2 in combinations(nomesPropriedades, 2):
            #media1, media2, media_diff, lower_bound, upper_bound, p_value, rejeitar, inverter_valores_medias = bootstrap_test_group(
            media1, media2, media_diff, lower_bound, upper_bound, p_value, rejeitar = bootstrap_test_group(
                df_modelo[df_modelo['nomePropriedade'] == grupo1][nome_csv],
                df_modelo[df_modelo['nomePropriedade'] == grupo2][nome_csv],
                statistic=np.mean,  # Estatistica e a media
                alpha=alpha,  # Alpha para o intervalo de confianca de 95%
                n_iterations= quantidadeSimulacoes
            )
            resultadosBootstrapEntrePropriedades.append([grupo1, grupo2, media1, media2, media_diff, lower_bound, upper_bound, p_value, rejeitar, aviao])
            media1, media2, media_diff, lower_bound, upper_bound, p_value, rejeitar = bootstrap_test_group(
                df_modelo[df_modelo['nomePropriedade'] == grupo2][nome_csv],
                df_modelo[df_modelo['nomePropriedade'] == grupo1][nome_csv],
                statistic=np.mean,  # Estatistica e a media
                alpha=alpha,  # Alpha para o intervalo de confianca de 95%
                n_iterations= quantidadeSimulacoes
            )
            resultadosBootstrapEntrePropriedades.append([grupo2, grupo1, media1, media2, media_diff, lower_bound, upper_bound, p_value, rejeitar, aviao])
    
    for propriedade in nomesPropriedades: 
        df_modelo = dfConcatenadoComVariacaoPercentual[dfConcatenadoComVariacaoPercentual['nomePropriedade'] == propriedade]
        # Lista de grupos
        # Calcula as estatisticas para cada par de grupos
        for grupo1, grupo2 in combinations(modelos_aviao, 2):
            media1, media2, media_diff, lower_bound, upper_bound, p_value, rejeitar = bootstrap_test_group(
                df_modelo[df_modelo['modeloAviao'] == grupo1][nome_csv],
                df_modelo[df_modelo['modeloAviao'] == grupo2][nome_csv],
                statistic=np.mean,  # Estatistica e a media
                alpha=alpha,  # Alpha para o intervalo de confianca de 95%
                n_iterations=quantidadeSimulacoes
            )
            # Adiciona os resultados a lista
            resultadosBootstrapEntreAvioes.append([grupo1, grupo2, media1, media2, media_diff, lower_bound, upper_bound, p_value, rejeitar, propriedade])
            media1, media2, media_diff, lower_bound, upper_bound, p_value, rejeitar = bootstrap_test_group(
                df_modelo[df_modelo['modeloAviao'] == grupo2][nome_csv],
                df_modelo[df_modelo['modeloAviao'] == grupo1][nome_csv],
                statistic=np.mean,  # Estatistica e a media
                alpha=alpha,  # Alpha para o intervalo de confianca de 95%
                n_iterations=quantidadeSimulacoes
            )
            resultadosBootstrapEntreAvioes.append([grupo2, grupo1, media1, media2, media_diff, lower_bound, upper_bound, p_value, rejeitar, propriedade])

    # Cria um DataFrame com os resultados
    df_resultadosBootstrapEntrePropriedades = pd.DataFrame(resultadosBootstrapEntrePropriedades, columns=['grupo 1', 'grupo 2', 'media grupo_1', 'media grupo_2', 'estatistica_t', 'media_inferior', 'media_superior', 'valor-p', 'rejeitar', 'modeloAviao'])
    df_resultadosBootstrapEntreAvioes = pd.DataFrame(resultadosBootstrapEntreAvioes, columns=['grupo 1', 'grupo 2', 'media grupo_1', 'media grupo_2', 'estatistica_t', 'media_inferior', 'media_superior', 'valor-p', 'rejeitar', 'propriedade'])
    df_resultadosBootstrapEntreAvioes.to_csv('resultadosBootstrapEntreAvioes.csv', index=False, sep=';', decimal='.')
    resultados_estatistica_bootstrap = []
    for aviao in df_resultadosBootstrapEntrePropriedades['modeloAviao'].unique().tolist():
        df_filtrado = df_resultadosBootstrapEntrePropriedades.loc[df_resultadosBootstrapEntrePropriedades['modeloAviao'] == aviao]
        # Ordenando os resultados por meandiffs em ordem decrescente
        df_filtrado['estatistica_t_absoluta'] = df_filtrado['estatistica_t'].abs()
        df_filtrado = df_filtrado.sort_values(by='estatistica_t_absoluta', ascending=False)
        df_filtrado = df_filtrado.drop(columns=['estatistica_t_absoluta'])
        df_filtrado.to_csv('resultadosBootstrap_' + aviao + '.csv', index=False, sep=';', decimal='.')
        # Concatenar grupos 1 e 2 com hífen
        df_filtrado['grupos_concatenados'] = df_filtrado['grupo 1'] + '-' + df_filtrado['grupo 2']
        # Criar o gráfico de barras
        bars = plt.bar(df_filtrado['grupos_concatenados'], df_filtrado['estatistica_t'], color='skyblue', edgecolor='black')
        plt.xlabel('Grupos')
        plt.ylabel('Estatística T')
        plt.title('Valores de Estatística T por Grupos Concatenados')
        plt.xticks(rotation=45)
        plt.grid(True) 
        # Salvar a figura
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(int(bar.get_height())), 
            ha='center', va='bottom', fontsize=5)
        plt.savefig(f"grafico_bootstrap_{aviao}.png", dpi=300)
        plt.close()
        plt.bar(np.arange(len(df_filtrado)), df_filtrado['media_superior'] - df_filtrado['media_inferior'],
        bottom=df_filtrado['media_inferior'], color='orange', alpha=0.3)
        # Plotando os pontos da estatística_t
        plt.scatter(np.arange(len(df_filtrado)), df_filtrado['estatistica_t'], color='red', s=10, edgecolor='black')
        plt.xlabel('Grupos', fontsize=12)
        plt.ylabel('Valores', fontsize=12)
        plt.title('Valores Estatísticos por Grupos Concatenados', fontsize=14)
        plt.xticks(np.arange(len(df_filtrado)), df_filtrado['grupos_concatenados'], rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.legend()
        plt.tight_layout()
        # Salvar a figura
        nome_figura = f"grafico_bootstrap_comparacao_limite_estatistica_{aviao}.png"
        plt.savefig(nome_figura, dpi=300)
        plt.close()
        df_filtrado.drop('grupos_concatenados', axis=1, inplace=True)
        resultados_estatistica_bootstrap.append(df_filtrado)
    print(resultados_estatistica_bootstrap)
    print(df_resultadosBootstrapEntreAvioes)

# Funcao para descrever e visualizar os dados
def descreverDados(nome_arquivo, variavel_avaliada):
    nome_csv = 'variacao_percentual_' + variavel_avaliada
    sns.set_context('notebook')
    df_analise_descritiva_deformacao = pd.DataFrame()
    df_analise_descritiva_variacao_deformacao = pd.DataFrame()
    # Importar dados e calcular variacao percentual
    dataframe_calculado = importarJson(nome_arquivo)
    
    # Definir um filtro para selecionar dados especificos
    filtro = ((dataframe_calculado['modeloAviao'] == 'B737800') & (dataframe_calculado['no'] == 55)) | ((dataframe_calculado['modeloAviao'] == 'B767300') & (dataframe_calculado['no'] == 0)) | ((dataframe_calculado['modeloAviao'] == 'B777300') & (dataframe_calculado['no'] == 47))
    
    # Aplicar o filtro ao DataFrame
    dataframe_filtrado = dataframe_calculado[filtro]
    dataframe_filtrado['valorPropriedade'] = pd.to_numeric(dataframe_filtrado['valorPropriedade'], errors='raise')
    
    # Iterar sobre os modelos de aviao unicos
    for aviao in dataframe_filtrado['modeloAviao'].unique().tolist():
        dataframe_filtradoo_por_aviao = dataframe_filtrado[(dataframe_filtrado['modeloAviao'] == aviao)]
        
        # Iterar sobre as Propriedades unicas
        for Propriedade in dataframe_filtradoo_por_aviao['nomePropriedade'].unique().tolist():
            if Propriedade != "Base":
                dataframe_filtrado_por_Propriedade = dataframe_filtradoo_por_aviao[(dataframe_filtradoo_por_aviao['nomePropriedade'] == Propriedade)]
                
                # Calcular a variacao percentual
                dfConcatenadoComVariacaoPercentual = dataframeVariacaoPercentual(dataframe_filtrado_por_Propriedade, nome_csv, variavel_avaliada = variavel_avaliada)
                dfConcatenadoComVariacaoPercentual_sem_outliers, outliers_dfConcatenadoComVariacaoPercentual = filtrar_outliers(dfConcatenadoComVariacaoPercentual)
                df_analise_descritiva_deformacao_atual = analise_quantitativa(dataframe_filtrado_por_Propriedade["e3"], Propriedade, aviao)
                df_analise_descritiva_variacao_deformacao_atual = analise_quantitativa(dfConcatenadoComVariacaoPercentual["variacao_percentual_e3"], Propriedade, aviao)
                df_analise_descritiva_deformacao = pd.concat([df_analise_descritiva_deformacao, df_analise_descritiva_deformacao_atual], ignore_index=True)
                df_analise_descritiva_variacao_deformacao = pd.concat([df_analise_descritiva_variacao_deformacao, df_analise_descritiva_variacao_deformacao_atual], ignore_index=True)
                # Nome do arquivo de figura
                nomeFiguraArquivo = f'Grafico de pontos para {Propriedade} no {aviao}'
                
                # Salvar os DataFrames em arquivos CSV
                dfConcatenadoComVariacaoPercentual.to_csv(nomeFiguraArquivo.title().replace(" ", "") + '_dataframe_variacao_percentual.csv', index=False, sep=';', decimal='.')
                outliers_dfConcatenadoComVariacaoPercentual.to_csv(nomeFiguraArquivo.title().replace(" ", "") + '_outliers.csv', index=False, sep=';', decimal='.')
                
                # Grafico de Variacao Percentual
                cores = np.random.rand(1,3)
                dfConcatenadoComVariacaoPercentual.to_csv(nomeFiguraArquivo.title().replace(" ", "") + '_variacao_percentual.csv', index=False, sep=';', decimal=',')
                unidadePropriedade = {'carregamento': 'Pa', 'elasBas': 'Pa', 'elasRev': 'Pa', 'elasSub': 'Pa', 'espBas': 'm', 'espRev': 'm', 'poiBas': '', 'poiRev': '', 'poiSub': '' }
                
                #Grafico variacao percentual
                largura = 720 / 80
                altura = 480 / 80
                plt.figure() #figsize=(largura, altura)
                plt.scatter(dfConcatenadoComVariacaoPercentual['valorPropriedade'], dfConcatenadoComVariacaoPercentual["variacao_percentual_e3"], color=cores, alpha=0.7, s=10)
                if unidadePropriedade[Propriedade] == '':
                    plt.xlabel(Propriedade)
                else:
                    plt.xlabel(Propriedade + ' (' + unidadePropriedade[Propriedade]+ ')' )
                plt.ylabel("Variação percentual (%)")
                plt.grid(True)
                plt.tight_layout()
                plt.ticklabel_format(style='plain', axis='y')
                sns.set_style('whitegrid')
                intervaloPlotado = 1.02
                multiplicador = 0.8
                margem = 0.1
                plt.margins(x = margem, y = margem) 
                # plt.xlim(0, dfConcatenadoComVariacaoPercentual['valorPropriedade'].max()* intervaloPlotado)
                plt.savefig(nomeFiguraArquivo.title().replace(" ", ""), dpi=300)
                plt.close()
                print(aviao + " " + Propriedade + " Variacao Percentual OK")
                # Grafico sem outliers
                plt.figure() #figsize=(largura, altura)
                cores = np.random.rand(1,3)
                plt.scatter(dfConcatenadoComVariacaoPercentual_sem_outliers['valorPropriedade'], dfConcatenadoComVariacaoPercentual_sem_outliers[nome_csv], color=cores, alpha=0.7, s=10)                
                if unidadePropriedade[Propriedade] == '':
                    plt.xlabel(Propriedade)
                else:
                    plt.xlabel(Propriedade + ' (' + unidadePropriedade[Propriedade]+ ')' )
                plt.ylabel("Variação percentual (%)")
                plt.margins(x = margem, y = margem) 
                plt.grid(True)
                plt.tight_layout()
                plt.ticklabel_format(style='plain', axis='y')
                sns.set_style('whitegrid')
                # plt.xlim(0, dfConcatenadoComVariacaoPercentual['valorPropriedade'].max()* intervaloPlotado)
                plt.savefig(nomeFiguraArquivo.title().replace(" ", "")+"_sem_outliers", dpi=300)
                plt.close()
                print(aviao + " " + Propriedade + " Sem outliers OK")
                # Grafico de Deformacoes Absolutas
                plt.figure() #figsize=(largura, altura)
                cores = np.random.rand(1,3) 
                plt.scatter(dataframe_filtrado_por_Propriedade['valorPropriedade'], dataframe_filtrado_por_Propriedade["e3"], color=cores, alpha=0.7, s=10) 
                if unidadePropriedade[Propriedade] == '':
                    plt.xlabel(Propriedade)
                else:
                    plt.xlabel(Propriedade + ' (' + unidadePropriedade[Propriedade]+ ')' )
                plt.ylabel("Deformação absoluta (m/m)")
                plt.margins(x = margem, y = margem) 
                plt.grid(True)
                plt.tight_layout()
                plt.ticklabel_format(style='plain', axis='y')
                sns.set_style('whitegrid')
                # plt.xlim(0, dfConcatenadoComVariacaoPercentual['valorPropriedade'].max()* intervaloPlotado)
                plt.savefig(nomeFiguraArquivo.title().replace(" ", "")+"_deformacoes_absolutas", dpi=300)
                plt.close()
                print(aviao + " " + Propriedade + " Deformacoes absolutas OK")
                # Plotar graficos de dispersao para cada coluna separadamente
    df_analise_descritiva_deformacao.to_csv('analise_descritiva_deformacao.csv', index=False, sep=';', decimal=',')
    df_analise_descritiva_variacao_deformacao.to_csv('analise_descritiva_variacao_deformacao.csv', index=False, sep=';', decimal=',')
    return []


# # # # Chamada das funcoes deslocamento
iniciarProcessamentoEstatistico('DeslocamentodadosModelosSaidaPrincipais.json', variavel_avaliada = 'u3', alpha = 0.05)
descreverDados('DeslocamentodadosModelosSaidaPrincipais.json', variavel_avaliada = 'u3')

# # # Chamada das funcoes deformacao
iniciarProcessamentoEstatistico('DeformacaodadosModelosSaidaPrincipais.json', variavel_avaliada = 'e3', alpha = 0.05, quantidadeSimulacoes = 100000)
descreverDados('DeformacaodadosModelosSaidaPrincipais.json', variavel_avaliada = 'e3')