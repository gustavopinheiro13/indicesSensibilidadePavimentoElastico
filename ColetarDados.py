from abaqus import *
from abaqusConstants import *
import numpy as np
import json

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

# Definindo uma classe para representar os objetos de saida para checagem de modelos depois
class saidaModelos:
    def __init__(self, nomeJob, nomeStep, nomeSensibilidade, valorSensibilidade, modeloAviao, nosInteresse):
        self.nomeJob = nomeJob
        self.nomeStep = nomeStep
        self.nomeSensibilidade = nomeSensibilidade
        self.valorSensibilidade = valorSensibilidade
        self.modeloAviao = modeloAviao
        self.nosInteresse = nosInteresse


def obter_dados_deslocamento(nomeJob, nomeStep, nome_campo, modeloAviao, nomeSensibilidade, nosInteresse, valorSensibilidade):
    # Caminho para o arquivo .odb
    caminho_modelo = nomeJob + '.odb'
    # Carregando o arquivo .odb
    odb = session.openOdb(caminho_modelo)
    # Obtendo o passo desejado
    passo = odb.steps[nomeStep]
    # Obtendo o campo de saída desejado
    campo_saida = passo.frames[-1].fieldOutputs[nome_campo]
    # Lista de objetos para armazenar os dados dos deslocamentos
    dados_deslocamentos = []
    # Iterando sobre os nós de interesse
    for noInteresse in nosInteresse:
        # Obtendo o valor do campo de saída para o nó específico
        try:
            valor_campo = campo_saida.values[noInteresse].dataDouble
        except:
            valor_campo = campo_saida.values[noInteresse - 1].data
        # Criando objeto de dados de deslocamento
        dados = DadosDeslocamento(nomeJob = nomeJob, nomeStep = nomeStep, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = valorSensibilidade, modeloAviao = modeloAviao, noInteresse = noInteresse, u1= valor_campo[0], u2= valor_campo[1], u3 = valor_campo[2])
        # Adicionando o objeto à lista
        dados_deslocamentos.append(dados)
    # Fechando o arquivo .odb
    odb.close()
    return dados_deslocamentos

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
        modelo_saida = saidaModelos(nomeJob = str(dado['nomeJob']), nomeStep = str(dado['nomeStep']),nomeSensibilidade = str(dado['nomeSensibilidade']), valorSensibilidade = str(dado['valorSensibilidade']), modeloAviao = str(dado['modeloAviao']), nosInteresse = dado['nosInteresse'])
        # Adiciona o objeto à lista
        lista_jobs.append(modelo_saida)
    return lista_jobs

def gravarDadosModelo(nome_arquivo):
    # Exemplo de uso
    lista_jobs = reimportarDadosDeModelos(nome_arquivo)
    nome_arquivo_saida = 'Deslocamento' + nome_arquivo
    dados_deslocamento = []
    for job in lista_jobs:
        dados = obter_dados_deslocamento(
            nomeJob=job.nomeJob,
            nomeStep=job.nomeStep,
            nome_campo='U',
            modeloAviao=job.modeloAviao,
            nomeSensibilidade=job.nomeSensibilidade,
            nosInteresse=job.nosInteresse,
            valorSensibilidade=job.valorSensibilidade
        )
        for modeloPonto in dados:
            dados_job = {
                'nomeJob': modeloPonto.nomeJob,
                'nomeStep': modeloPonto.nomeStep,
                'nomeSensibilidade': modeloPonto.nomeSensibilidade,
                'valorSensibilidade': modeloPonto.valorSensibilidade,
                'modeloAviao': modeloPonto.modeloAviao,
                'no':  int(modeloPonto.no),
                'u1':  np.float64(modeloPonto.u1),
                'u2':  np.float64(modeloPonto.u2),
                'u3':  np.float64(modeloPonto.u3)
            }
            dados_deslocamento.append(dados_job)
    # Salva os dados em um arquivo JSON
    with open(nome_arquivo_saida, 'w') as arquivo_saida:
        json.dump(dados_deslocamento, arquivo_saida, indent=4)

#gravarDadosModelo('dadosModelosSaida.json')
gravarDadosModelo('dadosPavimentoCritico.json')
#gravarDadosModelo('dadosModelosSaidaCalibracaoMesh.json')
#gravarDadosModelo('dadosModelosSaidaCalibracaoSubleito.json')

#Arrumar tamanho da mesh
#Arrumar
#tirar tudo de linear do documento
#pegar os intervalos superior e inferior de cada indice de sensibilidade
#Correcoes do Heber
