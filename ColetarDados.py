from abaqus import *
from abaqusConstants import *
import numpy as np
import json
import os

# Definicao da classe para armazenar os dados de deslocamento
class DadosDeslocamento:
    def __init__(self, nomeJob, nomeStep, nomePropriedade, valorPropriedade, modeloAviao, noInteresse, u1, u2, u3):
        self.nomeJob = nomeJob
        self.nomeStep = nomeStep
        self.nomePropriedade = nomePropriedade
        self.valorPropriedade = valorPropriedade
        self.modeloAviao = modeloAviao
        self.no = noInteresse
        self.u1 = u1
        self.u2 = u2
        self.u3 = u3
#

class DadosDeformacao:
    def __init__(self, nomeJob, nomeStep, nomePropriedade, valorPropriedade, modeloAviao, noInteresse, e1, e2, e3):
        self.nomeJob = nomeJob
        self.nomeStep = nomeStep
        self.nomePropriedade = nomePropriedade
        self.valorPropriedade = valorPropriedade
        self.modeloAviao = modeloAviao
        self.no = noInteresse
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3

class saidaModelos:
    def __init__(self, nomeJob, nomeStep, nomePropriedade, valorPropriedade, modeloAviao, nosInteresse):
        self.nomeJob = nomeJob
        self.nomeStep = nomeStep
        self.nomePropriedade = nomePropriedade
        self.valorPropriedade = valorPropriedade
        self.modeloAviao = modeloAviao
        self.nosInteresse = nosInteresse

# Funcao para obter os dados de deslocamento
def obter_dados_deslocamento(nomeJob, nomeStep, nome_campo, modeloAviao, nomePropriedade, nosInteresse, valorPropriedade):
    # Caminho para o arquivo .odb
    caminho_modelo = nomeJob + '.odb'
    # Carregando o arquivo .odb
    odb = session.openOdb(caminho_modelo)
    # Obtendo o passo desejado
    passo = odb.steps[nomeStep]
    # Obtendo o campo de saida desejado
    campo_saida = passo.frames[-1].fieldOutputs[nome_campo]
    # Lista de objetos para armazenar os dados dos deslocamentos
    dados_deslocamentos = []
    # Iterando sobre os nos de interesse
    for noInteresse in nosInteresse:
        # Obtendo o valor do campo de saida para o no especifico
        try:
            valor_campo = campo_saida.values[noInteresse].dataDouble
        except:
            valor_campo = campo_saida.values[noInteresse - 1].data
        # Criando objeto de dados de deslocamento
        dados = DadosDeslocamento(nomeJob=nomeJob, nomeStep=nomeStep, nomePropriedade=nomePropriedade, valorPropriedade=valorPropriedade, modeloAviao=modeloAviao, noInteresse=noInteresse, u1=valor_campo[0], u2=valor_campo[1], u3=valor_campo[2])
        # Adicionando o objeto a lista
        dados_deslocamentos.append(dados)
    # Fechando o arquivo .odb
    odb.close()
    return dados_deslocamentos

# Funcao para obter os dados de Deformacao
def obter_dados_Deformacao(nomeJob, nomeStep, nome_campo, modeloAviao, nomePropriedade, nosInteresse, valorPropriedade):
    # Caminho para o arquivo .odb
    caminho_modelo = nomeJob + '.odb'
    # Carregando o arquivo .odb
    odb = session.openOdb(caminho_modelo)
    # Obtendo o passo desejado
    passo = odb.steps[nomeStep]
    # Obtendo o campo de saida desejado
    campo_saida = passo.frames[-1].fieldOutputs[nome_campo]
    # Lista de objetos para armazenar os dados dos Deformacaos
    dados_Deformacao = []
    # Iterando sobre os nos de interesse
    for noInteresse in nosInteresse:
        # Obtendo o valor do campo de saida para o no especifico
        try:
            valor_campo = campo_saida.values[noInteresse].dataDouble
        except:
            valor_campo = campo_saida.values[noInteresse - 1].data
        # Criando objeto de dados de Deformacao
        #print(valor_campo)
        dados = DadosDeformacao(nomeJob=nomeJob, nomeStep=nomeStep, nomePropriedade=nomePropriedade, valorPropriedade=valorPropriedade, modeloAviao=modeloAviao, noInteresse=noInteresse, e1=valor_campo[0], e2=valor_campo[1], e3=valor_campo[2])
        # Adicionando o objeto a lista
        dados_Deformacao.append(dados)
    # Fechando o arquivo .odb
    odb.close()
    return dados_Deformacao

# Funcao para reimportar os dados de modelos a partir de um arquivo JSON
def reimportarDadosDeModelos(nome_arquivo):
    # Abre o arquivo JSON no modo de leitura
    with open(nome_arquivo, 'r') as arquivo_json:
        # Carrega os dados do arquivo JSON
        dados_json = json.load(arquivo_json)
    # Cria uma nova lista para armazenar os objetos reimportados
    lista_jobs = []
    # Percorre os dados e cria os objetos correspondentes
    for dado in dados_json:
        # Cria um objeto com os valores do dado
        modelo_saida = saidaModelos(nomeJob=str(dado['nomeJob']), nomeStep=str(dado['nomeStep']), nomePropriedade=str(dado['nomePropriedade']), valorPropriedade=str(dado['valorPropriedade']), modeloAviao=str(dado['modeloAviao']), nosInteresse=dado['nosInteresse'])
        # Adiciona o objeto a lista
        lista_jobs.append(modelo_saida)
    return lista_jobs

# Funcao para gravar os dados de modelos em um arquivo JSON
def gravarDadosModeloDeslocamento(nome_arquivo):
    os.chdir("C:/Users/gusta/resultados_abaqus/")
    # Reimporta os dados de modelos a partir do arquivo JSON
    lista_jobs = reimportarDadosDeModelos(nome_arquivo)
    nome_arquivo_saida = 'Deslocamento' + nome_arquivo
    nomesJob = []
    dados_deslocamento = []
    for job in lista_jobs:
        # Verifica se o nome do job ja foi adicionado a lista de nomes
        if any(job.nomeJob == nomeJobExistente for nomeJobExistente in nomesJob):
            pass
        else:
            nomesJob.append(job.nomeJob)
            # Obtem os dados de deslocamento para o job atual
            dados = obter_dados_deslocamento(
                nomeJob=job.nomeJob,
                nomeStep=job.nomeStep,
                nome_campo='U',
                modeloAviao=job.modeloAviao,
                nomePropriedade=job.nomePropriedade,
                nosInteresse=job.nosInteresse,
                valorPropriedade=job.valorPropriedade
            )
            for modeloPonto in dados:
                dados_job = {
                    'nomeJob': modeloPonto.nomeJob,
                    'nomeStep': modeloPonto.nomeStep,
                    'nomePropriedade': modeloPonto.nomePropriedade,
                    'valorPropriedade': modeloPonto.valorPropriedade,
                    'modeloAviao': modeloPonto.modeloAviao,
                    'no': int(modeloPonto.no),
                    'u1': np.float64(modeloPonto.u1),
                    'u2': np.float64(modeloPonto.u2),
                    'u3': np.float64(modeloPonto.u3)
                }
                dados_deslocamento.append(dados_job)
    # Salva os dados em um arquivo JSON
    with open(nome_arquivo_saida, 'w') as arquivo_saida:
        json.dump(dados_deslocamento, arquivo_saida, indent=4)
    print(nomesJob)
    return dados_deslocamento

# Funcao para gravar os dados de modelos em um arquivo JSON
def gravarDadosModeloDeformacao(nome_arquivo):
    os.chdir("C:/Users/gusta/resultados_abaqus/")
    # Reimporta os dados de modelos a partir do arquivo JSON
    lista_jobs = reimportarDadosDeModelos(nome_arquivo)
    nome_arquivo_saida = 'Deformacao' + nome_arquivo
    nomesJob = []
    dados_Deformacao = []
    for job in lista_jobs:
        print(job.nomeJob)
        # Verifica se o nome do job ja foi adicionado a lista de nomes
        if any(job.nomeJob == nomeJobExistente for nomeJobExistente in nomesJob):
            pass
        else:
            nomesJob.append(job.nomeJob)
            # Obtem os dados de Deformacao para o job atual
            dados = obter_dados_Deformacao(
                nomeJob=job.nomeJob,
                nomeStep=job.nomeStep,
                nome_campo='E',
                modeloAviao=job.modeloAviao,
                nomePropriedade=job.nomePropriedade,
                nosInteresse=job.nosInteresse,
                valorPropriedade=job.valorPropriedade
            )
            for modeloPonto in dados:
                dados_job = {
                    'nomeJob': modeloPonto.nomeJob,
                    'nomeStep': modeloPonto.nomeStep,
                    'nomePropriedade': modeloPonto.nomePropriedade,
                    'valorPropriedade': modeloPonto.valorPropriedade,
                    'modeloAviao': modeloPonto.modeloAviao,
                    'no': int(modeloPonto.no),
                    'e1': np.float64(modeloPonto.e1),
                    'e2': np.float64(modeloPonto.e2),
                    'e3': np.float64(modeloPonto.e3)
                }
                dados_Deformacao.append(dados_job)
    # Salva os dados em um arquivo JSON
    with open(nome_arquivo_saida, 'w') as arquivo_saida:
        json.dump(dados_Deformacao, arquivo_saida, indent=4)
    print(nomesJob)
    return dados_Deformacao

# # # Chamadas das funcoes
gravarDadosModeloDeslocamento('dadosPavimentoCritico.json')
gravarDadosModeloDeslocamento('dadosModelosSaidaCalibracaoSubleito.json')
gravarDadosModeloDeslocamento('dadosModelosSaidaCalibracaoComprimento.json')
gravarDadosModeloDeslocamento('dadosModelosSaidaCalibracaoMesh.json')
gravarDadosModeloDeslocamento('dadosModelosSaidaPrincipais.json')


# # # # Chamadas das funcoes
gravarDadosModeloDeformacao('dadosPavimentoCritico.json')
gravarDadosModeloDeformacao('dadosModelosSaidaCalibracaoSubleito.json')
gravarDadosModeloDeformacao('dadosModelosSaidaCalibracaoComprimento.json')
gravarDadosModeloDeformacao('dadosModelosSaidaCalibracaoMesh.json')
gravarDadosModeloDeformacao('dadosModelosSaidaPrincipais.json')