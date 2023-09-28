from pickle import TRUE
import string
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import json
import os

# Classe Material
class Material:
    def __init__(self, nomeCamada, nomeMaterial, espessuraCamada, moduloElasticidade, coeficientePoisson):
        """
        Classe que representa um material.

        Atributos:
        - nomeCamada: nome da camada do material.
        - nomeMaterial: nome do material.
        - espessuraCamada: espessura da camada do material.
        - moduloElasticidade: modulo de elasticidade do material.
        - coeficientePoisson: coeficiente de Poisson do material.
        """
        self.nomeCamada = nomeCamada
        self.nomeMaterial = nomeMaterial
        self.espessuraCamada = espessuraCamada
        self.moduloElasticidade = moduloElasticidade
        self.coeficientePoisson = coeficientePoisson

# Classe intervaloSensibilidade
class IntervaloSensibilidade:
    def __init__(self, intervaloEspessuraRevestimento, intervaloEspessuraBase, intervaloPoissonRevestimento, intervaloPoissonBase, intervaloPoissonSubleito, intervaloElasticidadeRevestimento, intervaloElasticidadeBase, intervaloElasticidadeSubleito, intervaloCarga):
        """
        Classe que representa um intervalo de sensibilidade.

        Atributos:
        - intervaloEspessuraRevestimento: intervalo da espessura do revestimento.
        - intervaloEspessuraBase: intervalo da espessura da base.
        - intervaloPoissonRevestimento: intervalo do coeficiente de Poisson do revestimento.
        - intervaloPoissonBase: intervalo do coeficiente de Poisson da base.
        - intervaloPoissonSubleito: intervalo do coeficiente de Poisson do subleito.
        - intervaloElasticidadeRevestimento: intervalo do modulo de elasticidade do revestimento.
        - intervaloElasticidadeBase: intervalo do modulo de elasticidade da base.
        - intervaloElasticidadeSubleito: intervalo do modulo de elasticidade do subleito.
        - intervaloCarga: intervalo da carga.
        """
        self.intervaloEspessuraRevestimento = intervaloEspessuraRevestimento
        self.intervaloEspessuraBase = intervaloEspessuraBase
        self.intervaloPoissonRevestimento = intervaloPoissonRevestimento
        self.intervaloPoissonBase = intervaloPoissonBase
        self.intervaloPoissonSubleito = intervaloPoissonSubleito
        self.intervaloElasticidadeRevestimento = intervaloElasticidadeRevestimento
        self.intervaloElasticidadeBase = intervaloElasticidadeBase
        self.intervaloElasticidadeSubleito = intervaloElasticidadeSubleito
        self.intervaloCarga = intervaloCarga


# Classe aviao
class Aviao:
    def __init__(self, modelo, tipoEixo, roda1DistanciaEixoNuloX, roda1DistanciaEixoNuloY, roda2DistanciaEixoNuloX, roda2DistanciaEixoNuloY, larguraContatoPneu, comprimentoContatoPneu, carregamento,
                mascaraCondicaoContornoFundo, mascaraCondicaoContornoSimetriaX, mascaraCondicaoContornoSimetriaY, mascaraCondicaoContornoTravaY, mascaraSuperficie, nosInteresse):
        """
        Classe que representa um aviao.
        Atributos:
        - modelo: modelo do aviao.
        - tipoEixo: tipo de eixo do aviao.
        - roda1DistanciaEixoNuloX: distancia da roda 1 ao eixo nulo X.
        - roda2DistanciaEixoNuloX: distancia da roda 2 ao eixo nulo X.
        - roda1DistanciaEixoNuloY: distancia da roda 1 ao eixo nulo Y.
        - roda2DistanciaEixoNuloY: distancia da roda 2 ao eixo nulo Y.
        - larguraContatoPneu: largura de contato do pneu.
        - comprimentoContatoPneu: comprimento de contato do pneu.
        - carregamento: carga aplicada.
        - mascaraCondicaoContornoFundo: mascara da condicao de contorno de fundo.
        - mascaraCondicaoContornoSimetriaX: mascara da condicao de contorno de simetria em X.
        - mascaraCondicaoContornoSimetriaY: mascara da condicao de contorno de simetria em Y.
        - mascaraCondicaoContornoTravaY: mascara da condicao de contorno de trava em Y.
        - mascaraSuperficie: mascara da superficie.
        - nosInteresse: nos de interesse.
        """
        self.modelo = modelo
        self.tipoEixo = tipoEixo
        self.roda1DistanciaEixoNuloX = roda1DistanciaEixoNuloX
        self.roda2DistanciaEixoNuloX = roda2DistanciaEixoNuloX
        self.roda1DistanciaEixoNuloY = roda1DistanciaEixoNuloY
        self.roda2DistanciaEixoNuloY = roda2DistanciaEixoNuloY
        self.larguraContatoPneu = larguraContatoPneu
        self.comprimentoContatoPneu = comprimentoContatoPneu
        self.carregamento = carregamento
        self.mascaraCondicaoContornoFundo = mascaraCondicaoContornoFundo
        self.mascaraCondicaoContornoSimetriaX = mascaraCondicaoContornoSimetriaX
        self.mascaraCondicaoContornoSimetriaY = mascaraCondicaoContornoSimetriaY
        self.mascaraCondicaoContornoTravaY = mascaraCondicaoContornoTravaY
        self.mascaraSuperficie = mascaraSuperficie
        self.nosInteresse = nosInteresse
        self.localizacaoRodaMediaX = (roda1DistanciaEixoNuloX + roda2DistanciaEixoNuloX) / 2
        self.rodaInternaX = min(roda1DistanciaEixoNuloX, roda2DistanciaEixoNuloX)
        self.localizacaoRodaMediaY = (roda1DistanciaEixoNuloY + roda2DistanciaEixoNuloY) / 2
        self.rodaInternaY = min(roda1DistanciaEixoNuloY, roda2DistanciaEixoNuloY)
        self.localizacaoDatumRoda1_1 = self.rodaInternaX - (larguraContatoPneu / 2)
        self.planoPrincipalDatumRoda1_1 = YZPLANE
        self.localizacaoDatumRoda1_2 = self.rodaInternaX + (larguraContatoPneu / 2)
        self.planoPrincipalDatumRoda1_2 = YZPLANE
        self.localizacaoDatumRoda1_3 = self.rodaInternaY + (comprimentoContatoPneu / 2)
        self.planoPrincipalDatumRoda1_3 = XZPLANE
        self.localizacaoDatumRoda1_4 = self.rodaInternaY - (comprimentoContatoPneu / 2)
        self.planoPrincipalDatumRoda1_4 = XZPLANE

# Funcao para definir os intervalos de sensibilidade
def intervalosAnalise():
    fatorCrescimento = 1.02
    intervaloEspessuraRevestimento = rangeSensibilidade(indiceInicial=0.075, numeroRepeticoes=86, fatorDeCrescimento=fatorCrescimento)
    intervaloEspessuraBase = rangeSensibilidade(indiceInicial=0.075, numeroRepeticoes=86, fatorDeCrescimento=fatorCrescimento)
    intervaloPoissonRevestimento = rangeSensibilidade(indiceInicial=0.15, numeroRepeticoes=44, fatorDeCrescimento=fatorCrescimento)
    intervaloPoissonBase = rangeSensibilidade(indiceInicial=0.2, numeroRepeticoes=30, fatorDeCrescimento=fatorCrescimento)	
    intervaloPoissonSubleito = rangeSensibilidade(indiceInicial=0.2, numeroRepeticoes=30, fatorDeCrescimento=fatorCrescimento)
    intervaloElasticidadeRevestimento = rangeSensibilidade(indiceInicial=1380E6, numeroRepeticoes=157, fatorDeCrescimento=fatorCrescimento)
    intervaloElasticidadeBase = rangeSensibilidade(indiceInicial=187.5E6, numeroRepeticoes=167, fatorDeCrescimento=fatorCrescimento)
    intervaloElasticidadeSubleito = rangeSensibilidade(indiceInicial=7E6, numeroRepeticoes=199, fatorDeCrescimento=fatorCrescimento)
    intervaloCarga = rangeSensibilidade(indiceInicial=206.84E3, numeroRepeticoes=111, fatorDeCrescimento=fatorCrescimento)
    intervalosDeSensibilidade = IntervaloSensibilidade(
        intervaloEspessuraRevestimento=intervaloEspessuraRevestimento,
        intervaloEspessuraBase=intervaloEspessuraBase,
        intervaloPoissonRevestimento=intervaloPoissonRevestimento,
        intervaloPoissonBase=intervaloPoissonBase,
        intervaloPoissonSubleito=intervaloPoissonSubleito,
        intervaloElasticidadeRevestimento=intervaloElasticidadeRevestimento,
        intervaloElasticidadeBase=intervaloElasticidadeBase,
        intervaloElasticidadeSubleito=intervaloElasticidadeSubleito,
        intervaloCarga=intervaloCarga
    )
    return intervalosDeSensibilidade

# Classe para representar a saida dos modelos
class SaidaModelos:
    def __init__(self, nomeJob, nomeStep, nomeSensibilidade, valorSensibilidade, modeloAviao, nosInteresse):
        """
        Classe que representa a saida de modelos.
        Atributos:
        - nomeJob: nome do job associado a saida do modelo.
        - nomeStep: nome do step associado a saida do modelo.
        - nomeSensibilidade: nome da sensibilidade associada a saida do modelo.
        - valorSensibilidade: valor da sensibilidade do modelo.
        - modeloAviao: modelo de aviao associado a saida do modelo.
        - nosInteresse: nos de interesse na saida do modelo.
        """
        self.nomeJob = nomeJob
        self.nomeStep = nomeStep
        self.nomeSensibilidade = nomeSensibilidade
        self.valorSensibilidade = valorSensibilidade
        self.modeloAviao = modeloAviao
        self.nosInteresse = nosInteresse

# Classe para representar o tamanho da malha
class TamanhoMesh:
    def __init__(self, camadaRevestimento, camadaBase, camadaSubleito):
        self.camadaRevestimento = camadaRevestimento
        self.camadaBase = camadaBase
        self.camadaSubleito = camadaSubleito

def substituir_tipo_elemento(caminho_arquivo, texto_antigo, texto_novo):
    # Ler o conteúdo do arquivo
    with open(caminho_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
    # Substituir o texto antigo pelo texto novo
    conteudo_atualizado = conteudo.replace(texto_antigo, texto_novo)
    # Escrever o conteúdo atualizado de volta no arquivo
    with open(caminho_arquivo, 'w') as arquivo:
        arquivo.write(conteudo_atualizado)


# Funcao modelarPart
def modelarPart(nomeModelo, nomePart, localizacaoRodaMediaX, comprimentoSimulado, materialRevestimento, materialBase, materialSubleito):
    """
    Funcao para modelar uma parte.
    Parametros:
    - nomeModelo: nome do modelo.
    - nomePart: nome da parte.
    - localizacaoRodaMediaX: localizacao media entre as rodas no eixo X.
    """
    # Criacao do perfil retangular para extrusao
    mdb.models[nomeModelo].ConstrainedSketch(name='__perfil__', sheetSize=2*localizacaoRodaMediaX)
    mdb.models[nomeModelo].sketches['__perfil__'].rectangle(point1=(0.0, 0.0), point2=(localizacaoRodaMediaX, comprimentoSimulado))
    
    # Criacao da parte atraves de extrusao
    mdb.models[nomeModelo].Part(dimensionality=THREE_D, name=nomePart, type=DEFORMABLE_BODY)
    mdb.models[nomeModelo].parts[nomePart].BaseSolidExtrude(depth=materialRevestimento.espessuraCamada + materialBase.espessuraCamada + materialSubleito.espessuraCamada, sketch=mdb.models[nomeModelo].sketches['__perfil__'])
    
    # Deleta o esboco apos a extrusao
    del mdb.models[nomeModelo].sketches['__perfil__']


# Funcao criarDatum 
def criarDatum(nomeModelo, nomePart, offsetDatum, planoPrincipalDatum):
    """
    Funcao para criar um datum.
    Parametros:
    - nomeModelo: nome do modelo.
    - nomePart: nome da parte.
    - offsetDatum: offset do datum.
    - planoPrincipalDatum: plano principal do datum.
    Retorna:
    - datumSaida: datum criado.
    """
    # Criacao de um datum usando um plano principal
    datumSaida = mdb.models[nomeModelo].parts[nomePart].DatumPlaneByPrincipalPlane(
        offset=offsetDatum, principalPlane=planoPrincipalDatum)
    return datumSaida


# Funcao criarMaterialAbaqus
def criarMaterialAbaqus(nomeModelo, nomeMaterial, moduloElasticidade, coeficientePoisson):
    """
    Funcao para criar um material no Abaqus.
    Parametros:
    - nomeModelo: nome do modelo.
    - nomeMaterial: nome do material.
    - moduloElasticidade: modulo de elasticidade do material.
    - coeficientePoisson: coeficiente de Poisson do material.
    """
    # Criacao de um material com propriedades elasticas
    mdb.models[nomeModelo].Material(name=nomeMaterial)
    mdb.models[nomeModelo].materials[nomeMaterial].Elastic(table=((moduloElasticidade, coeficientePoisson),))


# Funcao recortarPartPorDatum
def recortarPartPorDatum(nomeModelo, nomePart, objetoDatum):
    """
    Funcao para recortar uma parte por um plano de datum no Abaqus.
    Parametros:
    - nomeModelo: nome do modelo.
    - nomePart: nome da parte.
    - objetoDatum: objeto do plano de datum a ser usado para recortar a parte.
    """
    # Recortar a parte usando um plano de datum
    mdb.models[nomeModelo].parts[nomePart].PartitionCellByDatumPlane(cells=mdb.models[nomeModelo].parts[nomePart].cells, datumPlane=objetoDatum)


# Funcao definicaoSet
def definicaoSet(nomeModelo, nomeMaterial, nomeCamada):
    """
    Funcao para definir uma secao solida homogenea no Abaqus.
    Parametros:
    - nomeModelo: nome do modelo.
    - nomeMaterial: nome do material a ser atribuido a secao.
    - nomeCamada: nome da camada para a qual a secao sera definida.
    """
    # Definir uma secao solida homogenea
    mdb.models[nomeModelo].HomogeneousSolidSection(material=nomeMaterial, name='secao' + nomeCamada, thickness=None)


# Funcao definirSecao
def definirSecao(nomeModelo, nomePart, nomeCamada, mascara):
    """
    Funcao para definir uma secao em uma parte no Abaqus.
    Parametros:
    - nomeModelo: nome do modelo.
    - nomePart: nome da parte.
    - nomeCamada: nome da camada para a qual a secao sera definida.
    - mascara: mascara para identificar as celulas da parte que serao incluidas na secao.
    """
    # Criar um conjunto de celulas e atribuir uma secao a ele
    mdb.models[nomeModelo].parts[nomePart].Set(cells=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask((mascara, ), ), name='set' + nomeCamada)
    mdb.models[nomeModelo].parts[nomePart].SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models[nomeModelo].parts[nomePart].sets['set' + nomeCamada], sectionName='secao' + nomeCamada, thicknessAssignment=FROM_SECTION)

## chamada principal para a criacao do modelo
def criarModelo(aviaoSelecionado, comprimentoSimulado, materialRevestimento, materialBase, materialSubleito, nomeSensibilidade, valorSensibilidade, tamanhoDaMesh):
    # validacao se mesh esta em ordem descrescente
    tamanhoDaMesh.camadaRevestimento, tamanhoDaMesh.camadaBase, tamanhoDaMesh.camadaSubleito = sorted([tamanhoDaMesh.camadaRevestimento, tamanhoDaMesh.camadaBase, tamanhoDaMesh.camadaSubleito], reverse=False)
    # Criacao do nome do modelo
    if nomeSensibilidade[:4] == "Mesh":
        nomeModelo = 'Md' + aviaoSelecionado.modelo + nomeSensibilidade
        print(nomeModelo)
    else:
        nomeModelo = 'Md' + aviaoSelecionado.modelo + nomeSensibilidade + str(round(valorSensibilidade, 4)).replace(".", ",")
        print(nomeModelo)
    mdb.Model(modelType=STANDARD_EXPLICIT, name=nomeModelo)
    #
    # Criacao do nome da part
    nomePart = 'Pt' + nomeModelo
    #
    modelarPart(nomeModelo = nomeModelo, nomePart = nomePart, localizacaoRodaMediaX = aviaoSelecionado.localizacaoRodaMediaX, comprimentoSimulado=comprimentoSimulado materialRevestimento = materialRevestimento, materialBase = materialBase, materialSubleito = materialSubleito)
    #
    #Datums de camadas
    # Datums de camadas
    # Criacao do material de revestimento no Abaqus 
    criarMaterialAbaqus(nomeModelo = nomeModelo, nomeMaterial = materialRevestimento.nomeMaterial, moduloElasticidade = materialRevestimento.moduloElasticidade, coeficientePoisson = materialRevestimento.coeficientePoisson)  
    # Criacao do datum para a camada de revestimento
    criarDatum(nomeModelo = nomeModelo, nomePart = nomePart, offsetDatum = materialBase.espessuraCamada + materialSubleito.espessuraCamada, planoPrincipalDatum = XYPLANE)
    datumCamadaRevestimento = mdb.models[nomeModelo].parts[nomePart].datums[2]
    # Criacao do material de base no Abaqus
    criarMaterialAbaqus(nomeModelo = nomeModelo, nomeMaterial = materialBase.nomeMaterial, moduloElasticidade = materialBase.moduloElasticidade, coeficientePoisson = materialBase.coeficientePoisson)    
    criarDatum(nomeModelo=nomeModelo, nomePart=nomePart, offsetDatum= materialSubleito.espessuraCamada, planoPrincipalDatum=XYPLANE)
    datumCamadaBase = mdb.models[nomeModelo].parts[nomePart].datums[3]
    criarMaterialAbaqus(nomeModelo = nomeModelo, nomeMaterial = materialSubleito.nomeMaterial, moduloElasticidade = materialSubleito.moduloElasticidade, coeficientePoisson = materialSubleito.coeficientePoisson)
    criarDatum(nomeModelo=nomeModelo, nomePart=nomePart, offsetDatum= 0, planoPrincipalDatum=XYPLANE)
    datumCamadaSubleito = mdb.models[nomeModelo].parts[nomePart].datums[4]
    criarDatum(nomeModelo=nomeModelo, nomePart=nomePart, offsetDatum=  materialRevestimento.espessuraCamada + materialBase.espessuraCamada + materialSubleito.espessuraCamada, planoPrincipalDatum=XYPLANE)
    datumCamadaSuperficie = mdb.models[nomeModelo].parts[nomePart].datums[5]
    #
    #Recortar as parts Revestimento, Base e Subleito
    recortarPartPorDatum(nomeModelo = nomeModelo, nomePart = nomePart, objetoDatum = datumCamadaRevestimento)
    recortarPartPorDatum(nomeModelo = nomeModelo, nomePart = nomePart, objetoDatum = datumCamadaBase)
    #
    #Definicao de secoes
    definicaoSet(nomeModelo = nomeModelo, nomeMaterial = materialRevestimento.nomeMaterial, nomeCamada = materialRevestimento.nomeCamada)
    definicaoSet(nomeModelo = nomeModelo, nomeMaterial = materialBase.nomeMaterial, nomeCamada = materialBase.nomeCamada)
    definicaoSet(nomeModelo = nomeModelo, nomeMaterial = materialSubleito.nomeMaterial, nomeCamada = materialSubleito.nomeCamada)
    #
    #atribuicao de secoes
    definirSecao(nomeModelo = nomeModelo, nomePart = nomePart, nomeCamada = materialRevestimento.nomeCamada, mascara = '[#2 ]')
    definirSecao(nomeModelo = nomeModelo, nomePart = nomePart, nomeCamada = materialBase.nomeCamada, mascara = '[#4 ]')
    definirSecao(nomeModelo = nomeModelo, nomePart = nomePart, nomeCamada = materialSubleito.nomeCamada, mascara = '[#1 ]')
    #
    criarDatum(nomeModelo = nomeModelo, nomePart = nomePart, offsetDatum = aviaoSelecionado.localizacaoDatumRoda1_1, planoPrincipalDatum = aviaoSelecionado.planoPrincipalDatumRoda1_1)
    datumRoda1_1 = mdb.models[nomeModelo].parts[nomePart].datums[11]
    criarDatum(nomeModelo = nomeModelo, nomePart = nomePart, offsetDatum = aviaoSelecionado.localizacaoDatumRoda1_2, planoPrincipalDatum = aviaoSelecionado.planoPrincipalDatumRoda1_2)
    datumRoda1_2 = mdb.models[nomeModelo].parts[nomePart].datums[12]
    criarDatum(nomeModelo = nomeModelo, nomePart = nomePart, offsetDatum = aviaoSelecionado.rodaInternaX , planoPrincipalDatum = aviaoSelecionado.planoPrincipalDatumRoda1_2)
    datumRoda1_3 = mdb.models[nomeModelo].parts[nomePart].datums[13]
    criarDatum(nomeModelo = nomeModelo, nomePart = nomePart, offsetDatum = aviaoSelecionado.localizacaoDatumRoda1_3, planoPrincipalDatum = aviaoSelecionado.planoPrincipalDatumRoda1_3)
    datumRoda2_1 = mdb.models[nomeModelo].parts[nomePart].datums[14]
    criarDatum(nomeModelo = nomeModelo, nomePart = nomePart, offsetDatum = aviaoSelecionado.localizacaoDatumRoda1_4, planoPrincipalDatum = aviaoSelecionado.planoPrincipalDatumRoda1_4)
    datumRoda2_2 = mdb.models[nomeModelo].parts[nomePart].datums[15]
    criarDatum(nomeModelo = nomeModelo, nomePart = nomePart, offsetDatum = aviaoSelecionado.rodaInternaY, planoPrincipalDatum = aviaoSelecionado.planoPrincipalDatumRoda1_4)
    datumRoda2_3 = mdb.models[nomeModelo].parts[nomePart].datums[16]
    #
    #Recortar datums das rodas
    recortarPartPorDatum(nomeModelo = nomeModelo, nomePart = nomePart, objetoDatum = datumRoda1_1)
    recortarPartPorDatum(nomeModelo = nomeModelo, nomePart = nomePart, objetoDatum = datumRoda1_2)
    recortarPartPorDatum(nomeModelo = nomeModelo, nomePart = nomePart, objetoDatum = datumRoda1_3)
    recortarPartPorDatum(nomeModelo = nomeModelo, nomePart = nomePart, objetoDatum = datumRoda2_1)
    if aviaoSelecionado.tipoEixo != 'simples':
        recortarPartPorDatum(nomeModelo = nomeModelo, nomePart = nomePart, objetoDatum = datumRoda2_2)
        recortarPartPorDatum(nomeModelo = nomeModelo, nomePart = nomePart, objetoDatum = datumRoda2_3)
    #
    mdb.models[nomeModelo].HomogeneousSolidSection(material='Camada asfaltica', name='secaoRevestimento', thickness=None)
    #
    # Definicao de Assembly
    nomeAssembly = 'asb' + nomePart
    mdb.models[nomeModelo].rootAssembly.Instance(dependent=ON, name=nomeAssembly, part=mdb.models[nomeModelo].parts[nomePart])
    #
    # Definicao de Step
    nomeStep = 'stp' + nomePart
    mdb.models[nomeModelo].StaticStep(initialInc=0.01, maxInc=0.1, maxNumInc=1000, name=nomeStep, previous='Initial')
    #Superficie de carga
    nomeSuperficie = 'sp' + nomePart
    #
    mdb.models[nomeModelo].rootAssembly.Surface(name=nomeSuperficie, side1Faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask((aviaoSelecionado.mascaraSuperficie, ), ))
    #
    # Definicao de carga
    nomeCarga = 'crg' + nomePart
    #Alterar carga do aviao e objeto corrrespondente
    mdb.models[nomeModelo].Pressure(amplitude=UNSET, createStepName=nomeStep, distributionType=UNIFORM, field='', magnitude=aviaoSelecionado.carregamento, name=nomeCarga, region=mdb.models[nomeModelo].rootAssembly.surfaces[nomeSuperficie])
    #
    # Fundo
    bcNomeFundo = 'fnd' + nomePart
    mdb.models[nomeModelo].rootAssembly.Set(faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoFundo, ), ), name=bcNomeFundo)
    mdb.models[nomeModelo].DisplacementBC(amplitude=UNSET, createStepName='Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=bcNomeFundo, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeFundo], u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET)
    # Simetria
    bcNomeSimetriaY = 'smty' + nomePart
    mdb.models[nomeModelo].rootAssembly.Set(faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoSimetriaY , ), ), name=bcNomeSimetriaY)
    mdb.models[nomeModelo].YsymmBC(createStepName='Initial', localCsys=None, name=bcNomeSimetriaY, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeSimetriaY])
    bcNomeSimetriaX = 'smtx' + nomePart
    mdb.models[nomeModelo].rootAssembly.Set(faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoSimetriaX, ), ), name=bcNomeSimetriaX)
    mdb.models[nomeModelo].XsymmBC(createStepName='Initial', localCsys=None, name=bcNomeSimetriaX, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeSimetriaX])
    #
    #
    # Trava Y
    bcNomeTravaY = 'tvY' + nomePart
#    mdb.models[nomeModelo].rootAssembly.Set(name=bcNomeTravaY, vertices=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].vertices.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoTravaY, ), ))
    mdb.models[nomeModelo].rootAssembly.Set(faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoTravaY, ), ), name=bcNomeTravaY)
    mdb.models[nomeModelo].DisplacementBC(amplitude=UNSET, createStepName='Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=bcNomeTravaY, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeTravaY], u1=UNSET, u2=SET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
    # Field Output
    mdb.models[nomeModelo].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'E', 'U'))
    ## e tandem triplo?
    if aviaoSelecionado.tipoEixo == 'tandemTriplo':
        criarDatum(nomeModelo = nomeModelo, nomePart = nomePart, offsetDatum = aviaoSelecionado.comprimentoContatoPneu/2, planoPrincipalDatum = aviaoSelecionado.planoPrincipalDatumRoda1_3)
        datumRoda3_1 = mdb.models[nomeModelo].parts[nomePart].datums[23]
        recortarPartPorDatum(nomeModelo = nomeModelo, nomePart = nomePart, objetoDatum = datumRoda3_1)
        mdb.models[nomeModelo].rootAssembly.Surface(name=nomeSuperficie, side1Faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask(('[#0:2 #240 #11000000 #0 #400000 #200 ]', ), ))
    # Mesh
    if aviaoSelecionado.tipoEixo == 'simples':
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#7d640008 #0 #8000700e #403f403 ]', ), ), minSizeFactor=0.1, size=tamanhoDaMesh.camadaRevestimento)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#2800227 #0 #30100000 #40440a2c ]', ), ), minSizeFactor=0.1, size=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0 #40000000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#80000000 #280420 #11 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaRevestimento)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:4 #10 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#110000 #0:3 #1 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaRevestimento)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:2 #400 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0 #10008000 #20000 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:3 #20000000 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#950 #0 #40000000 #50 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:2 #200000 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#ad480 #afd77bdf #fcd8be0 #83a80180 #e ]', ), ), minSizeFactor=0.1, size=tamanhoDaMesh.camadaSubleito)
        #
        mdb.models[nomeModelo].parts[nomePart].setMeshControls(regions=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#ff0fe1 ]', ), ), technique=STRUCTURED)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[6], region=mdb.models[nomeModelo].parts[nomePart].cells[12], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[46], region=mdb.models[nomeModelo].parts[nomePart].cells[4], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[80], region=mdb.models[nomeModelo].parts[nomePart].cells[13], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[59], region=mdb.models[nomeModelo].parts[nomePart].cells[14], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[129], region=mdb.models[nomeModelo].parts[nomePart].cells[15], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#8000 #8004000 #210000 #80000100 #2 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#950 #0 #40000000 #50 ]', ), ), maxSize=3.0, minSize=0.1)
        mdb.models[nomeModelo].parts[nomePart].setElementType(elemTypes=(ElemType(elemCode=AC3D8R, elemLibrary=STANDARD), ElemType(elemCode=AC3D8R, elemLibrary=STANDARD), ElemType(elemCode=UNKNOWN_TET, elemLibrary=STANDARD)), regions=(mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#f01e ]', ), ), ))
        mdb.models[nomeModelo].parts[nomePart].assignStackDirection(cells=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#ffffff ]', ), ), referenceRegion=mdb.models[nomeModelo].parts[nomePart].faces[12])
        mdb.models[nomeModelo].parts[nomePart].setMeshControls(algorithm=ADVANCING_FRONT, regions=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#ffffff ]', ), ), technique=SWEEP)
        #'[#f3c0780 #1e0 ]'
        #'[#c00f01e0 #1e1e03 ]'
    elif aviaoSelecionado.tipoEixo == 'tandemDuplo':
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#fe422 #80002200 #16789fff #4000fe0 #1ffa389 #10 #1e000020 ]', ), ), minSizeFactor=0.1, size=tamanhoDaMesh.camadaRevestimento)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#30005d #22240080 #49876000 #48410000 #6005c36 #c #600000', ' #10 ]'), ), minSizeFactor=0.1, size=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#ac00000 #44480000 #0 #80820000 #b8000000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:4 #40 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#100 #0 #80000000 #0:4 #8 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:6 #800 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:5 #100000 #8001 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:7 #400 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#1080 #4400 #0 #14 #0:3 #40 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaRevestimento)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:6 #4 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:5 #5010820 #50 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaRevestimento)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#f5000a00 #1993987f #20000000 #333cf00b #40000000 #faeef7c3 #e19f778a', ' #3a7 ]'), ), minSizeFactor=0.1, size=tamanhoDaMesh.camadaSubleito)
        mdb.models[nomeModelo].parts[nomePart].setMeshControls(regions=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#f0c3f87f #fe1f ]', ), ), technique=STRUCTURED)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[229], region=mdb.models[nomeModelo].parts[nomePart].cells[37], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[179], region=mdb.models[nomeModelo].parts[nomePart].cells[27], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[62], region=mdb.models[nomeModelo].parts[nomePart].cells[8], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[27], region=mdb.models[nomeModelo].parts[nomePart].cells[9], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[155], region=mdb.models[nomeModelo].parts[nomePart].cells[38], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[159], region=mdb.models[nomeModelo].parts[nomePart].cells[39], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[231], region=mdb.models[nomeModelo].parts[nomePart].cells[40], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[113], region=mdb.models[nomeModelo].parts[nomePart].cells[26], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[127], region=mdb.models[nomeModelo].parts[nomePart].cells[25], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setElementType(elemTypes=(ElemType(elemCode=AC3D8R, elemLibrary=STANDARD), ElemType(elemCode=AC3D8R, elemLibrary=STANDARD), ElemType(elemCode=UNKNOWN_TET, elemLibrary=STANDARD)), regions=(mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#f3c0780 #1e0 ]', ), ), ))
        mdb.models[nomeModelo].parts[nomePart].assignStackDirection(cells=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#ffffffff #ffff ]', ), ), referenceRegion=mdb.models[nomeModelo].parts[nomePart].faces[98])        
        mdb.models[nomeModelo].parts[nomePart].setMeshControls(algorithm=ADVANCING_FRONT, regions=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#ffffffff #ffff ]', ), ), technique=SWEEP)           
    elif aviaoSelecionado.tipoEixo == 'tandemTriplo':
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#80007f92 #fec1c20 #44000074 #1fc8 #fff00044 #122001f3 #2003ff47', ' #1000000 #f000 ]'), ), minSizeFactor=0.1, size=tamanhoDaMesh.camadaRevestimento)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#1806d #c0102000 #ba01c988 #6000 #92801 #6cc8800c #180c00b8', ' #0 #800300 ]'), ), minSizeFactor=0.1, size=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:8 #20000000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#48000000 #41 #0 #21 #88 #0:3 #2000000 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaRevestimento)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:7 #200000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:6 #40000000 #2802a12 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaRevestimento)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#1000000 #4000 #0 #2:2 #0:3 #400000 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:7 #40000000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:7 #80080 #4 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#560000 #0 #442002 #158000 #0 #1110000 #1700000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:5 #80000000 ]', ), ), maxSize=tamanhoDaMesh.camadaSubleito, minSize=tamanhoDaMesh.camadaBase)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#36a80000 #3003839e #1ba1601 #ffea0014 #6d730 #67e00 #86800000', ' #bc57d76d #1d3f0cfb ]'), ), minSizeFactor=0.1, size=tamanhoDaMesh.camadaSubleito)
        mdb.models[nomeModelo].parts[nomePart].setMeshControls(regions=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#3ff0fe1f #fe1e1fc ]', ), ), technique=STRUCTURED)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[49], region=mdb.models[nomeModelo].parts[nomePart].cells[8], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[20], region=mdb.models[nomeModelo].parts[nomePart].cells[18], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[17], region=mdb.models[nomeModelo].parts[nomePart].cells[17], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[18], region=mdb.models[nomeModelo].parts[nomePart].cells[16], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[26], region=mdb.models[nomeModelo].parts[nomePart].cells[19], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[118], region=mdb.models[nomeModelo].parts[nomePart].cells[44], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[213], region=mdb.models[nomeModelo].parts[nomePart].cells[49], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[212], region=mdb.models[nomeModelo].parts[nomePart].cells[50], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[214], region=mdb.models[nomeModelo].parts[nomePart].cells[51], sense=FORWARD)
        mdb.models[nomeModelo].parts[nomePart].setSweepPath(edge=mdb.models[nomeModelo].parts[nomePart].edges[282], region=mdb.models[nomeModelo].parts[nomePart].cells[52], sense=REVERSE)
        mdb.models[nomeModelo].parts[nomePart].setElementType(elemTypes=(ElemType(elemCode=AC3D8R, elemLibrary=STANDARD), ElemType(elemCode=AC3D8R, elemLibrary=STANDARD), ElemType(elemCode=UNKNOWN_TET, elemLibrary=STANDARD)), regions=(mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#c00f01e0 #1e1e03 ]', ), ), ))
        mdb.models[nomeModelo].parts[nomePart].assignStackDirection(cells=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#ffffffff #fffffff ]', ), ), referenceRegion=mdb.models[nomeModelo].parts[nomePart].faces[141])
        mdb.models[nomeModelo].parts[nomePart].setMeshControls(algorithm=ADVANCING_FRONT, regions=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask(('[#ffffffff #fffffff ]', ), ), technique=SWEEP)        
    mdb.models[nomeModelo].parts[nomePart].generateMesh()
    ####################################################################################################
    #Criacao de reference points
    ## 0, roda ###
    # Ponto de simetria do eixo - Geometrico
    # Ponto deembaixo do pneu
    # Ponto de simetria do pneu
    # Para cada aeronave
    # for noInteresse in aviaoSelecionado.nosInteresse:
    #     mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].vertices[noInteresse])
    #Datums de rodas
    ####################################################################################################
    #regerar assembly
    mdb.models[nomeModelo].rootAssembly.regenerate()
    # Job
    nomeJob = 'job' + nomePart
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model=nomeModelo, modelPrint=OFF, 
    multiprocessingMode=THREADS, name=nomeJob, nodalOutputPrecision=FULL, numCpus=24, numDomains=24, numGPUs=1, queue=None, resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
    mdb.jobs[nomeJob].writeInput(consistencyChecking=OFF)
    del mdb.jobs[nomeJob]
    substituir_tipo_elemento(nomeJob + '.inp','type=AC3D8R','type=CIN3D8')
    mdb.ModelFromInputFile(inputFileName=nomeJob + '.inp', name=nomeJob)
    mdb.JobFromInputFile(atTime=None, explicitPrecision=SINGLE,
    getMemoryFromAnalysis=True, inputFileName=nomeJob + '.inp', memory=97, memoryUnits=PERCENTAGE, multiprocessingMode=DEFAULT, name=
    nomeJob, nodalOutputPrecision=FULL, numCpus=24, numDomains=24, numGPUs=1, queue=None, resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
    return SaidaModelos(nomeJob = nomeJob, nomeStep = nomeStep, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = valorSensibilidade, modeloAviao = aviaoSelecionado.modelo, nosInteresse = aviaoSelecionado.nosInteresse)


def rangeSensibilidade(indiceInicial, numeroRepeticoes, fatorDeCrescimento):
    # Funcao para gerar uma lista de valores sensibilidade com base no fator de crescimento
    return [round(indiceInicial * (fatorDeCrescimento ** i), 4) for i in range(numeroRepeticoes)]



def avioesBase():
    # Funcao para criar objetos aviao com parametros especificos
    # Criacao de objetos para os modelos de aviao (B737800, B767300, B777300) com parametros especificos
    # Adiciona os objetos a lista listaAvioes e retorna a lis
    listaAvioes = []
    # Funcao para inicializar o codigo com base em parametros de entrada
    # Cria um objeto aviao do modelo Boeing 737-800 com parametros especificos
    boeing737800 = Aviao(modelo='B737800', tipoEixo = 'simples',roda1DistanciaEixoNuloX=3.2893,roda1DistanciaEixoNuloY=0, roda2DistanciaEixoNuloX=2.4257, roda2DistanciaEixoNuloY = 0, larguraContatoPneu=0.323, comprimentoContatoPneu=0.517, 
                        carregamento=1406.53E3,  mascaraCondicaoContornoFundo = '[#1000000 #8181 #2010 #2 ]' ,mascaraCondicaoContornoSimetriaX = '[#0 #20144000 #8140c409 ]', mascaraCondicaoContornoSimetriaY = '[#804a000 #42 #5a280000 ]', 
                        mascaraCondicaoContornoTravaY = '[#0 #48890000 #24110a02 ]', mascaraSuperficie = '[#0 #200000 #100 ]', nosInteresse=[23, 22, 26, 53, 54, 55, 39, 44, 47])
    # Cria um objeto aviao do modelo Boeing 767-300 com parametros especificos
    boeing767300 = Aviao(modelo='B767300', tipoEixo = 'tandemDuplo', roda1DistanciaEixoNuloX=5.2197, roda1DistanciaEixoNuloY=0.7112, roda2DistanciaEixoNuloX=4.0767,  roda2DistanciaEixoNuloY = 0.7112, larguraContatoPneu=0.332, comprimentoContatoPneu=0.531, 
                        carregamento=1344.48E3, mascaraCondicaoContornoFundo = '[#1481000 #4800000 #9 #60404000 #4000020 #800008 ]' ,mascaraCondicaoContornoSimetriaX = '[#0:4 #2480510 #205031 ]', mascaraCondicaoContornoSimetriaY = '[#80126000 #51000001 #44100 #10820128 #0 #168a00 ]', 
                        mascaraCondicaoContornoTravaY = '[#0:4 #80922240 #90442 ]', mascaraSuperficie = '[#48000000 #0 #22000 ]', nosInteresse=[9, 6, 7, 10, 1, 0, 13, 12, 14, 80, 79, 83, 72, 66, 60, 73, 71, 67])
    # Cria um objeto aviao do modelo Boeing 777-300 com parametros especificos
    boeing777300 = Aviao(modelo='B777300', tipoEixo = 'tandemTriplo', roda1DistanciaEixoNuloX=6.1849, roda1DistanciaEixoNuloY=1.4478, roda2DistanciaEixoNuloX=4.7879, roda2DistanciaEixoNuloY = 1.4478, larguraContatoPneu=0.354, comprimentoContatoPneu=0.566, 
                        carregamento=1482.37E3, mascaraCondicaoContornoFundo = '[#1481000 #4800000 #9 #60404000 #4000020 #800008 ]',mascaraCondicaoContornoSimetriaX = '[#0:4 #2480510 #205031 ]', mascaraCondicaoContornoSimetriaY = '[#80126000 #51000001 #44100 #10820128 #0 #168a00 ]', 
                        mascaraCondicaoContornoTravaY = '[#0:4 #80922240 #90442 ]', mascaraSuperficie = '[#48000000 #0 #22000 ]', nosInteresse=[56 ,53 ,54 ,57 ,48 ,47 ,60 ,59 ,61 ,23 ,22 ,26 ,95 ,89 ,85 ,96 ,94 ,90])
    listaAvioes.append(boeing737800)
    listaAvioes.append(boeing767300)
    listaAvioes.append(boeing777300)
    return listaAvioes

def materiaisBase():
    # Funcao para criar objetos material com parametros especificos
    # Criacao de objetos para os materiais (Revestimento, Base, Subleito) com parametros especificos
    # Adiciona os objetos a lista listaMateriais e retorna a lista
    listaMateriais = []
    materialRevestimento = Material(nomeCamada='Revestimento', nomeMaterial='Camada asfaltica', espessuraCamada=0.1, moduloElasticidade=1500E6, coeficientePoisson=0.30)
    materialBase = Material(nomeCamada='Base', nomeMaterial='BGS', espessuraCamada=0.3, moduloElasticidade=250E6, coeficientePoisson=0.35)
    materialSubleito = Material(nomeCamada='Subleito', nomeMaterial='Material do Subleito', espessuraCamada=3, moduloElasticidade=200E6, coeficientePoisson=0.35)
    listaMateriais.append(materialRevestimento)
    listaMateriais.append(materialBase)
    listaMateriais.append(materialSubleito)
    return listaMateriais

def processarModelos(listaJobs, rodarJobs, nomeJson):
    # Funcao para processar os modelos e gerar um arquivo JSON de saida
    # Converte a lista de objetos em uma lista de dicionarios para a saida em JSON
    # Itera sobre a lista de objetos e cria dicionarios com informacoes relevantes
    # Escreve a lista de dicionarios em um arquivo JSON
    # Convertendo a lista de objetos em uma lista de dicionarios para saida em JSON
    os.chdir("C:/Users/gusta/resultados_abaqus/")
    nomesJob = []
    modelos_Saida = []
    for objeto in listaJobs:
        if any(objeto.nomeJob == nomeJobExistente for nomeJobExistente in nomesJob):
            pass
        else:
            nomesJob.append(objeto.nomeJob)
            dicionario = {
                "nomeJob": objeto.nomeJob,
                "nomeStep": objeto.nomeStep,
                "nomeSensibilidade": objeto.nomeSensibilidade,
                "valorSensibilidade": objeto.valorSensibilidade,
                "modeloAviao": objeto.modeloAviao,
                "nosInteresse": objeto.nosInteresse
            }
            modelos_Saida.append(dicionario)
    # Escrevendo a lista de dicionarios em um arquivo JSON
    with open(nomeJson, "w") as arquivo_json:
        json.dump(modelos_Saida, arquivo_json, indent=4)
        if rodarJobs == True:
            # Se a variavel rodarJobs for True, executa os jobs
            for job in listaJobs:
                mdb.jobs[job.nomeJob].submit(consistencyChecking=OFF)
                #job.submit(consistencyChecking=OFF)
                #mdb.jobs[job.nomeJob].waitForCompletion()
                print([job.nomeJob, mdb.jobs[job.nomeJob].status])
                # Submete cada job para execucao

def inicializarCodigoModelosPrincipais(rodarJobs, intervalos):
    # Funcao para inicializar a criacao dos modelos principais com diferentes parametros
    # Cria objetos aviao e material base
    # Cria um objeto tamanhoDaMesh com base nas espessuras das camadas
    # Cria uma lista de jobs vazia
    # Cria um modelo para cada aviao com os parametros especificados
    # Para cada aviao, varia diferentes parametros (espessura, elasticidade, Poisson, carregamento)
    # Cria os modelos e adiciona os jobs a lista de jobs
    # Processa os modelos e gera o arquivo JSON de saida
    boeing737800, boeing767300, boeing777300 = avioesBase()[0], avioesBase()[1], avioesBase()[2]
    materialRevestimento, materialBase, materialSubleito = materiaisBase()[0], materiaisBase()[1], materiaisBase()[2]
    #
    # Cria um objeto material para o subleito com parametros especificos
    nomeSensibilidade= 'Base'    
    tamanhoDaMesh = TamanhoMesh(camadaRevestimento = 0.1, camadaBase = 0.1, camadaSubleito = 3)
    listaJobs = []
    comprimentoSimulado = 20
    listaJobs.append(criarModelo(aviaoSelecionado=boeing737800, materialRevestimento=materialRevestimento, comprimentoSimulado=comprimentoSimulado, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = 0))
    listaJobs.append(criarModelo(aviaoSelecionado=boeing767300, materialRevestimento=materialRevestimento, comprimentoSimulado=comprimentoSimulado, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = 0))
    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, materialRevestimento=materialRevestimento, comprimentoSimulado=comprimentoSimulado, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = 0))
    # Cria um modelo utilizando o aviao selecionado e os materiais definidos, e adiciona o job a lista de jobs
    ######
    ###### Variacoes
    #Investigacao espessura camada revestimento
    # listaAvioes = [boeing737800, boeing767300, boeing777300]
    # fatorCrescimento = 1.02
    # for aviaoSelecionado in listaAvioes:
    #     nomeSensibilidade= 'espRev'
    #     for espessuraRevestimento in intervalos.intervaloEspessuraRevestimento:
    #         materialRevestimento.espessuraCamada = espessuraRevestimento
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = espessuraRevestimento))
    #     materialRevestimento = materiaisBase()[0]
    #     nomeSensibilidade= 'espBas'
    #     for espessuraBase in intervalos.intervaloEspessuraBase:
    #         materialBase.espessuraCamada = espessuraBase
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = espessuraBase))
    #     materialBase = materiaisBase()[1]
    #     nomeSensibilidade= 'elasRev'
    #     for elasticidadeRevestimento in intervalos.intervaloElasticidadeRevestimento:
    #         materialRevestimento.moduloElasticidade = elasticidadeRevestimento
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = elasticidadeRevestimento))
    #     materialRevestimento = materiaisBase()[0]
    #     nomeSensibilidade= 'elasBas'
    #     for elasticidadeBase in intervalos.intervaloElasticidadeBase:
    #         materialBase.moduloElasticidade = elasticidadeBase
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = elasticidadeBase))
    #     materialBase = materiaisBase()[1]
    #     nomeSensibilidade= 'elasSub'
    #     for elasticidadeSubleito in intervalos.intervaloElasticidadeSubleito:
    #         materialSubleito.moduloElasticidade = elasticidadeSubleito
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = elasticidadeSubleito))
    #     materialSubleito = materiaisBase()[2]
    #     nomeSensibilidade= 'poiRev'
    #     for poissonRevestimento in intervalos.intervaloPoissonRevestimento:
    #         materialRevestimento.coeficientePoisson = poissonRevestimento
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = poissonRevestimento))
    #     materialRevestimento = materiaisBase()[0]
    #     nomeSensibilidade= 'poiBas'
    #     for poissonBase in intervalos.intervaloPoissonBase:
    #         materialBase.coeficientePoisson = poissonBase
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = poissonBase))
    #     materialBase = materiaisBase()[1]
    #     nomeSensibilidade= 'poiSub'
    #     for poissonSubleito in intervalos.intervaloPoissonSubleito:
    #         materialSubleito.coeficientePoisson = poissonSubleito
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = poissonSubleito))
    #     materialSubleito = materiaisBase()[2]
    #     nomeSensibilidade= 'carregamento'
    #     for carregamento in intervalos.intervaloCarga:
    #         aviaoSelecionado.carregamento = carregamento
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito,tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = carregamento))
    processarModelos(listaJobs, rodarJobs, nomeJson = 'dadosModelosSaidaPrincipais.json')

def iniciarCodigoCalibracaoMesh(rodarJobs):
    boeing737800, boeing767300, boeing777300 = avioesBase()[0], avioesBase()[1], avioesBase()[2]
    materialRevestimento, materialBase, materialSubleito = pavimentoCritico()[0], pavimentoCritico()[1], pavimentoCritico()[2]
    tamanhoDaMesh = TamanhoMesh(camadaRevestimento = 0.05, camadaBase = 0.20, camadaSubleito = 0.75)
    listaJobs = []
    meshRevestimento = [0.05, 0.1, 0.15, 0.2, 0.25, 0.30, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
    meshBase = [0.1, 0.2, 0.30, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2]
    meshSubleito = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3]
    nomesJob = []
    comprimentoSimulado = 20
    for revestimento in meshRevestimento:
        tamanhoDaMesh.camadaRevestimento = revestimento
        for base in meshBase:
            tamanhoDaMesh.camadaBase = base
            for subleito in meshSubleito:
                aviaoSelecionado = boeing777300
                nomeModelo = "Mesh" + str(round(revestimento, 4)).replace(".", ",") + "-" + str(round(base, 4)).replace(".", ",")  + "-"+ str(round(subleito, 4)).replace(".", ",")
                tamanhoDaMesh.camadaSubleito = subleito
                if any(nomeModelo == nomeJobExistente for nomeJobExistente in nomesJob):
                    pass
                else:
                    nomesJob.append(nomeModelo)
                    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, comprimentoSimulado=comprimentoSimulado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = nomeModelo, valorSensibilidade = subleito))
    processarModelos(listaJobs, rodarJobs, nomeJson = 'dadosModelosSaidaCalibracaoMesh.json')

def iniciarCodigoPavimentocritico(rodarJobs, intervalos):
    boeing777300 = avioesBase()[2]
    materialRevestimento, materialBase, materialSubleito = materiaisBase()[0], materiaisBase()[1], materiaisBase()[2]
    tamanhoDaMesh = TamanhoMesh(camadaRevestimento = 0.05, camadaBase = 0.20, camadaSubleito = 0.75)
    listaJobs = []
    materialRevestimento.espessuraCamada = intervalos.intervaloEspessuraRevestimento[0]
    materialSubleito.espessuraCamada = 5
    comprimentoSimulado = 20
    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, comprimentoSimulado=comprimentoSimulado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = "ESEspRev" , valorSensibilidade = materialRevestimento.espessuraCamada))
    materialRevestimento = materiaisBase()[0]
    #
    materialBase.espessuraCamada = intervalos.intervaloEspessuraBase[0]
    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, comprimentoSimulado=comprimentoSimulado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = "ESEspBase", valorSensibilidade = materialBase.espessuraCamada))
    materialBase = materiaisBase()[1]
    #
    materialRevestimento.coeficientePoisson = intervalos.intervaloPoissonRevestimento[-1]
    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, comprimentoSimulado=comprimentoSimulado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = "ESPoiRev", valorSensibilidade = materialRevestimento.coeficientePoisson))
    materialRevestimento = materiaisBase()[0]
    #
    materialBase.coeficientePoisson = intervalos.intervaloPoissonBase[-1]
    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, comprimentoSimulado=comprimentoSimulado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = "ESPoiBas", valorSensibilidade = materialBase.coeficientePoisson))
    materialBase = materiaisBase()[1]
    #
    materialSubleito.coeficientePoisson = intervalos.intervaloPoissonSubleito[-1]
    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, comprimentoSimulado=comprimentoSimulado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = "ESPoiSub", valorSensibilidade = materialSubleito.coeficientePoisson))
    materialSubleito = materiaisBase()[2]
    #
    materialRevestimento.moduloElasticidade = intervalos.intervaloElasticidadeRevestimento[0]
    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, comprimentoSimulado=comprimentoSimulado, comprimentoSimulado=comprimentoSimulado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = "ESElasRev", valorSensibilidade = materialRevestimento.moduloElasticidade))
    materialRevestimento = materiaisBase()[0]
    #
    materialBase.moduloElasticidade = intervalos.intervaloElasticidadeBase[0]
    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, comprimentoSimulado=comprimentoSimulado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh=tamanhoDaMesh, nomeSensibilidade = "ESElasBas", valorSensibilidade = materialBase.moduloElasticidade))
    materialBase = materiaisBase()[1]
    #
    materialSubleito.moduloElasticidade = intervalos.intervaloElasticidadeSubleito[0]
    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, comprimentoSimulado=comprimentoSimulado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito,tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = "ESElasSub", valorSensibilidade = materialSubleito.moduloElasticidade))
    materialSubleito = materiaisBase()[2]
    processarModelos(listaJobs, rodarJobs, nomeJson = 'dadosPavimentoCritico.json')


def iniciarCodigoCalibracaoSubleito(rodarJobs):
    boeing777300 = avioesBase()[2]
    materialRevestimento, materialBase, materialSubleito = pavimentoCritico()[0], pavimentoCritico()[1], pavimentoCritico()[2]
    tamanhoDaMesh = TamanhoMesh(camadaRevestimento = 0.05, camadaBase = 0.20, camadaSubleito = 0.75)
    listaJobs = []
    nomesJob = []
    comprimentoSimulado = 20
    listaAlturas = rangeSensibilidade(indiceInicial=3, numeroRepeticoes=25, fatorDeCrescimento=1.1)
    for alturaSubleito in listaAlturas:
        aviaoSelecionado = boeing777300
        materialSubleito.espessuraCamada = alturaSubleito
        listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, comprimentoSimulado=comprimentoSimulado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, tamanhoDaMesh= tamanhoDaMesh, nomeSensibilidade = "espessuraSubleito", valorSensibilidade = alturaSubleito))
    processarModelos(listaJobs, rodarJobs, nomeJson = 'dadosModelosSaidaCalibracaoSubleito.json')


def pavimentoCritico():
    listaMateriais = []
    materialRevestimento = Material(nomeCamada='Revestimento', nomeMaterial='Camada asfaltica', espessuraCamada=0.1, moduloElasticidade=1500E6, coeficientePoisson=0.30)
    materialBase = Material(nomeCamada='Base', nomeMaterial='BGS', espessuraCamada=0.3, moduloElasticidade=250E6, coeficientePoisson=0.35)
    materialSubleito = Material(nomeCamada='Subleito', nomeMaterial='Material do Subleito', espessuraCamada=5, moduloElasticidade=7E6, coeficientePoisson=0.35)
    listaMateriais.append(materialRevestimento)
    listaMateriais.append(materialBase)
    listaMateriais.append(materialSubleito)
    return listaMateriais


intervalos = intervalosAnalise()
#Executa a funcao que inicializa o  codigo
# iniciarCodigoCalibracaoMesh(rodarJobs = False)
iniciarCodigoCalibracaoSubleito(rodarJobs = False)
# iniciarCodigoPavimentocritico(rodarJobs = False, intervalos = intervalos)
# inicializarCodigoModelosPrincipais(rodarJobs = False, intervalos = intervalos)

# Remove o modelo com nome 'Model-1' do dicionario mdb.models  
del mdb.models['Model-1']

#espessura revestimento
print("espessuras revestimentos " + str(intervalos.intervaloEspessuraRevestimento) + "\n")
#espessura base
print("espessura bases" + str(intervalos.intervaloEspessuraBase) + "\n")
#poisson revestimento
print("poisson revestimento " + str(intervalos.intervaloPoissonRevestimento) + "\n")
#poisson base
print("poisson base " + str(intervalos.intervaloPoissonBase) + "\n")
#poisson subleito
print("poisson subleito " + str(intervalos.intervaloPoissonSubleito) + "\n")
#elasticidade revestimento
print("elasticidade revestimento " + str(intervalos.intervaloElasticidadeRevestimento) + "\n")
#elasticidade base
print("elasticidade base " + str(intervalos.intervaloElasticidadeBase) + "\n")
#elasticidade subleito
print("elasticidade subleito " + str(intervalos.intervaloElasticidadeSubleito) + "\n")
#Carga
print("Carga " + str(intervalos.intervaloCarga) + "\n") 

#Pontos no canto inferior da roda
#B777 - 47
#B767 - 0
#B737 - 55

#testar se a adaptação com comprimento do pavimento funcionou
#Preciso ainda adicionar a reimportação de jobs na espessurasubleito, definicaoMalha, comprimento do pavimento
#preciso criar o modelo para calibração de comprimento de pavimento