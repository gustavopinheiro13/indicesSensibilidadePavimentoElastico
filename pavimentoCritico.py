import os
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
# Funcao para importar os dados do arquivo JSON e criar a lista de objetos
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


def pavimentoCritico(nome_arquivo):
    # Carrega os dados do arquivo JSON
    os.chdir("C:/Users/gusta/")
    with open(nome_arquivo, 'r') as arquivo_json:
        dados_deslocamento = json.load(arquivo_json)

    # Importar os dados do arquivo e criar a lista de objetos DadosDeslocamento
    lista_deslocamentos_calculados = importar_dados_deslocamento(nome_arquivo)
    dados_filtrados = filter(lambda x: x.no == 47, lista_deslocamentos_calculados)
    return max(dados_filtrados, key=lambda x: x.u3)

pavimentoCriticoAdotado = pavimentoCritico('DeslocamentodadosPavimentoCritico.json')
print(pavimentoCriticoAdotado)
