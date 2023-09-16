# Classe DadosDeslocamento para armazenar informacoes de deslocamento
class DadosDeslocamento:
    # Construtor para inicializar os atributos da classe
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

# Funcao para importar os dados do arquivo JSON e criar a lista de objetos DadosDeslocamento
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

# Funcao para identificar o pavimento critico com base nos dados de deslocamento
def pavimentoCritico(nome_arquivo):
    # Carrega os dados do arquivo JSON
    os.chdir("C:/Users/gusta/")
    with open(nome_arquivo, 'r') as arquivo_json:
        dados_deslocamento = json.load(arquivo_json)

    # Importar os dados do arquivo e criar a lista de objetos DadosDeslocamento
    lista_deslocamentos_calculados = importar_dados_deslocamento(nome_arquivo)
    
    # Filtrar os dados para o no de interesse (no == 47) e encontrar o valor maximo de u3
    dados_filtrados = filter(lambda x: x.no == 47, lista_deslocamentos_calculados)
    return max(dados_filtrados, key=lambda x: x.u3)

# Chamada da funcao para identificar o pavimento critico e imprimir os resultados
pavimentoCriticoAdotado = pavimentoCritico('DeslocamentodadosPavimentoCritico.json')
print(pavimentoCriticoAdotado)