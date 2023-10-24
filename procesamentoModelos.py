import os
import subprocess
import json
from multiprocessing import Pool
import time
from multiprocessing import freeze_support

# Definicao da classe para representar os objetos de saida para checagem de modelos depois
class saidaModelos:
    def __init__(self, nomeJob, nomeStep, nomeSensibilidade, valorSensibilidade, modeloAviao, nosInteresse):
        self.nomeJob = nomeJob
        self.nomeStep = nomeStep
        self.nomeSensibilidade = nomeSensibilidade
        self.valorSensibilidade = valorSensibilidade
        self.modeloAviao = modeloAviao
        self.nosInteresse = nosInteresse

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
        modelo_saida = saidaModelos(nomeJob=str(dado['nomeJob']), nomeStep=str(dado['nomeStep']), nomeSensibilidade=str(dado['nomeSensibilidade']), valorSensibilidade=str(dado['valorSensibilidade']), modeloAviao=str(dado['modeloAviao']), nosInteresse=dado['nosInteresse'])
        # Adiciona o objeto a lista
        lista_jobs.append(modelo_saida)
    return lista_jobs

# Funcao para executar um modelo usando a GPU
def executar_modelo(job):
    # Definir o nome da plataforma da GPU
    nome_plataforma_gpu = "NVIDIA CUDA"  # Substitua pela plataforma da sua GPU
    # Definir o comando para executar o job com a GPU
    comando = "abaqus job=" + job + " input=" + job + ".inp ask_delete=OFF cpus=3 output_precision=FULL"
    # Executar o comando
    subprocess.run(comando, shell=True)

# Funcao para iniciar a execucao de modelos
def iniciarModelos(arquivo, num_max_execucoes=4):
    # Define o diretorio onde os resultados serao salvos
    os.chdir("C:/Users/gusta/resultados_abaqus/")
    nome_arquivo = arquivo
    lista_objetos_job = reimportarDadosDeModelos(nome_arquivo)
    lista_jobs = []
    # Lista de nomes de jobs a serem executados
    for job in lista_objetos_job:
        lista_jobs.append(job.nomeJob)
    # Numero maximo de modelos em execucao simultaneamente
    # Criacao do pool de processos
    pool = Pool(processes=num_max_execucoes)
    # Mapeamento da funcao de execucao para os jobs
    pool.map(executar_modelo, lista_jobs)
    # Fechamento do pool
    pool.close()
    pool.join()

if __name__ == '__main__':
    tempo_inicial = time.time()
    freeze_support()
    # iniciarModelos("dadosPavimentoCritico.json")
    # iniciarModelos("dadosModelosSaidaCalibracaoSubleito.json")
    # iniciarModelos("dadosModelosSaidaCalibracaoComprimento.json")
    # iniciarModelos("dadosModelosSaidaCalibracaoMesh.json", num_max_execucoes=8)
    iniciarModelos("dadosModelosSaidaPrincipais.json", num_max_execucoes=8)
    tempo_final = time.time()
    print("Tempo de execucao: ", tempo_final - tempo_inicial)