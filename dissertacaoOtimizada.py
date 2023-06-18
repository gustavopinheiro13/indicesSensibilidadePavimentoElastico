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

# Classes
#Classe Material
class material:
    def __init__(self, nomeCamada, nomeMaterial, espessuraCamada, moduloElasticidade, coeficientePoisson):
        """
        Classe que representa um material.

        Atributos:
        - nomeCamada: nome da camada do material.
        - nomeMaterial: nome do material.
        - espessuraCamada: espessura da camada do material.
        - moduloElasticidade: módulo de elasticidade do material.
        - coeficientePoisson: coeficiente de Poisson do material.
        """
        self.nomeCamada = nomeCamada
        self.nomeMaterial = nomeMaterial
        self.espessuraCamada = espessuraCamada
        self.moduloElasticidade = moduloElasticidade
        self.coeficientePoisson = coeficientePoisson

    

# Classe aviao
class aviao:
    def __init__(self, modelo, tipoEixo, roda1DistanciaEixoNuloX, roda1DistanciaEixoNuloY, roda2DistanciaEixoNuloX, roda2DistanciaEixoNuloY , larguraContatoPneu, comprimentoContatoPneu, carregamento, 
                mascaraCondicaoContornoFundo, mascaraCondicaoContornoSimetriaX, mascaraCondicaoContornoSimetriaY, mascaraCondicaoContornoTravaY, mascaraSuperficie, nosInteresse):
    # def __init__(self, modelo, tipoEixo, roda1DistanciaEixoNuloX, roda1DistanciaEixoNuloY, roda2DistanciaEixoNuloX, roda2DistanciaEixoNuloY , larguraContatoPneu, comprimentoContatoPneu, carregamento, 
    #             mascaraCondicaoContornoFundo, mascaraCondicaoContornoSimetriaX, mascaraCondicaoContornoSimetriaY, mascaraCondicaoContornoTravaX, mascaraCondicaoContornoTravaY, mascaraCondicaoContornoTravaCanto, mascaraSuperficie, nosInteresse):
        """
        Classe que representa um avião.

        Atributos:
        - modelo: modelo do avião.
        - roda1DistanciaEixoNuloX: distância da roda 1 ao eixo nulo X.
        - roda2DistanciaEixoNuloX: distância da roda 2 ao eixo nulo X.
        - roda1DistanciaEixoNuloY: distância da roda 1 ao eixo nulo Y.
        - roda2DistanciaEixoNuloY: distância da roda 2 ao eixo nulo Y.
        - larguraContatoPneu: largura de contato do pneu.
        - comprimentoContatoPneu: comprimento de contato do pneu.
        - carregamento: carga aplicada.
        - localizacaoRodaMediaX: localização média entre as rodas X.
        - rodaInternaX: roda interna entre as rodas duplas no eixo X.
        - localizacaoRodaMediaY: localização média entre as rodas Y.
        - rodaInternaY: roda interna entre as rodas duplas no eixo Y.
        - localizacaoDatumRoda1_1: localização do Datum Roda 1_1.
        - planoPrincipalDatumRoda1_1: plano principal do Datum Roda 1_1.
        - localizacaoDatumRoda1_2: localização do Datum Roda 1_2.
        - planoPrincipalDatumRoda1_2: plano principal do Datum Roda 1_2.
        - localizacaoDatumRoda1_3: localização do Datum Roda 1_3.
        - planoPrincipalDatumRoda1_3: plano principal do Datum Roda 1_3.
        - localizacaoDatumRoda1_4: localização do Datum Roda 1_4.
        - planoPrincipalDatumRoda1_4: plano principal do Datum Roda 1_4.
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
        #
        self.localizacaoRodaMediaX = (self.roda1DistanciaEixoNuloX + self.roda2DistanciaEixoNuloX) / 2
        self.localizacaoRodaMediaY = (self.roda1DistanciaEixoNuloY + self.roda2DistanciaEixoNuloY) / 2
        #
        self.rodaInternaX = min(self.roda1DistanciaEixoNuloX, roda2DistanciaEixoNuloX)
        self.rodaInternaY = min(self.roda1DistanciaEixoNuloY, roda2DistanciaEixoNuloY)
        #
        # Para ver a simetria na reprodução 3D, comente a linha de baixo e descomente a seguinte
        self.localizacaoDatumRoda1_1 = (self.rodaInternaX - (self.larguraContatoPneu / 2))
        # self.localizacaoDatumRoda1_1 = self.localizacaoRodaMediaX - (self.rodaInterna - (larguraContatoPneu / 2))
        self.planoPrincipalDatumRoda1_1 = YZPLANE
        #
        # Para ver a simetria na reprodução 3D, comente a linha de baixo e descomente a seguinte
        self.localizacaoDatumRoda1_2 = (self.rodaInternaX + (self.larguraContatoPneu / 2))
        # self.localizacaoDatumRoda1_2 = self.localizacaoRodaMediaX - (self.rodaInterna + (larguraContatoPneu / 2))
        self.planoPrincipalDatumRoda1_2 = YZPLANE
        #
        #if self.rodaInternaY == 0:
        #    self.rodaInternaY = self.localizacaoRodaMediaX
        self.localizacaoDatumRoda1_3 = self.rodaInternaY + (self.comprimentoContatoPneu / 2)
        self.planoPrincipalDatumRoda1_3 = XZPLANE
        #
        self.localizacaoDatumRoda1_4 = self.rodaInternaY - (self.comprimentoContatoPneu / 2)
        self.planoPrincipalDatumRoda1_4 = XZPLANE
        #
        self.mascaraCondicaoContornoFundo = mascaraCondicaoContornoFundo
        self.mascaraCondicaoContornoSimetriaX = mascaraCondicaoContornoSimetriaX
        self.mascaraCondicaoContornoSimetriaY = mascaraCondicaoContornoSimetriaY
        self.mascaraCondicaoContornoTravaY = mascaraCondicaoContornoTravaY
        #self.mascaraCondicaoContornoTravaY = mascaraCondicaoContornoTravaY
        #self.mascaraCondicaoContornoTravaCanto = mascaraCondicaoContornoTravaCanto
        self.mascaraSuperficie = mascaraSuperficie
        self.nosInteresse = nosInteresse



# Definindo uma classe para representar os objetos de saida para checagem de modelos depois
class saidaModelos:
    def __init__(self, nomeJob, nomeStep, nomeSensibilidade, valorSensibilidade, modeloAviao, nosInteresse):
        self.nomeJob = nomeJob
        self.nomeStep = nomeStep
        self.nomeSensibilidade = nomeSensibilidade
        self.valorSensibilidade = valorSensibilidade
        self.modeloAviao = modeloAviao
        self.nosInteresse = nosInteresse


# Função modelarPart
def modelarPart(nomeModelo, nomePart, localizacaoRodaMediaX):
    """
    Função para modelar uma parte.

    Parâmetros:
    - nomeModelo: nome do modelo.
    - nomePart: nome da parte.
    - localizacaoRodaMediaX: localização média entre as rodas no eixo X.
    - localizacaoRodaMediaY: localização média entre as rodas no eixo Y.
    """
    mdb.models[nomeModelo].ConstrainedSketch(name='__perfil__', sheetSize=2*localizacaoRodaMediaX)
    mdb.models[nomeModelo].sketches['__perfil__'].rectangle(point1=(0.0, 0.0), point2=(localizacaoRodaMediaX, 2* localizacaoRodaMediaX))
    mdb.models[nomeModelo].Part(dimensionality=THREE_D, name=nomePart, type=DEFORMABLE_BODY)
    mdb.models[nomeModelo].parts[nomePart].BaseSolidExtrude(depth=(2*localizacaoRodaMediaX), sketch=mdb.models[nomeModelo].sketches['__perfil__'])
    del mdb.models[nomeModelo].sketches['__perfil__']

# Função criarDatum 
def criarDatum(nomeModelo, nomePart, offsetDatum, planoPrincipalDatum):
    """
    Função para criar um datum.
    Parâmetros:
    - nomeModelo: nome do modelo.
    - nomePart: nome da parte.
    - offsetDatum: offset do datum.
    - planoPrincipalDatum: plano principal do datum.

    Retorna:
    - datumSaida: datum criado.
    """
    datumSaida = mdb.models[nomeModelo].parts[nomePart].DatumPlaneByPrincipalPlane(
        offset=offsetDatum, principalPlane=planoPrincipalDatum)
    return datumSaida


# Função criarMaterialAbaqus
def criarMaterialAbaqus(nomeModelo, nomeMaterial, moduloElasticidade, coeficientePoisson):
    """
    Função para criar um material no Abaqus.

    Parâmetros:
    - nomeModelo: nome do modelo.
    - nomeMaterial: nome do material.
    - moduloElasticidade: módulo de elasticidade do material.
    - coeficientePoisson: coeficiente de Poisson do material.
    """
    mdb.models[nomeModelo].Material(name=nomeMaterial)
    mdb.models[nomeModelo].materials[nomeMaterial].Elastic(table=((moduloElasticidade, coeficientePoisson),))

# Função recortarPartPorDatum
def recortarPartPorDatum(nomeModelo, nomePart, objetoDatum):
    """
    Função para recortar uma parte por um plano de datum no Abaqus.

    Parâmetros:
    - nomeModelo: nome do modelo.
    - nomePart: nome da parte.
    - objetoDatum: objeto do plano de datum a ser usado para recortar a parte.
    """
    mdb.models[nomeModelo].parts[nomePart].PartitionCellByDatumPlane(cells=mdb.models[nomeModelo].parts[nomePart].cells, datumPlane=objetoDatum)

# Função definicaoSet
def definicaoSet(nomeModelo, nomeMaterial, nomeCamada):
    """
    Função para definir uma seção sólida homogênea no Abaqus.

    Parâmetros:
    - nomeModelo: nome do modelo.
    - nomeMaterial: nome do material a ser atribuído à seção.
    - nomeCamada: nome da camada para a qual a seção será definida.
    """
    mdb.models[nomeModelo].HomogeneousSolidSection(material=nomeMaterial, name='secao' + nomeCamada, thickness=None)


# Função definirSecao
def definirSecao(nomeModelo, nomePart, nomeCamada, mascara):
    """
    Função para definir uma seção em uma parte no Abaqus.

    Parâmetros:
    - nomeModelo: nome do modelo.
    - nomePart: nome da parte.
    - nomeCamada: nome da camada para a qual a seção será definida.
    - mascara: máscara para identificar as células da parte que serão incluídas na seção.
    """
    mdb.models[nomeModelo].parts[nomePart].Set(cells=mdb.models[nomeModelo].parts[nomePart].cells.getSequenceFromMask((mascara, ), ), name='set' + nomeCamada)
    mdb.models[nomeModelo].parts[nomePart].SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models[nomeModelo].parts[nomePart].sets['set' + nomeCamada], sectionName='secao' +  nomeCamada, thicknessAssignment=FROM_SECTION)

#def converterParaTitulo(indiceSensibilidade):
#    return '-'+ str(round(indiceSensibilidade,2))
##Chamadas principais
def criarModelo(aviaoSelecionado, materialRevestimento, materialBase, materialSubleito, nomeSensibilidade, valorSensibilidade):
    #
    # Criação do nome do modelo
    nomeModelo = 'Md' + aviaoSelecionado.modelo + nomeSensibilidade + str(round(valorSensibilidade, 2)).replace(".", "-")
    mdb.Model(modelType=STANDARD_EXPLICIT, name=nomeModelo)
    modelo = mdb.models[nomeModelo]
    #
    # Criação do nome da part
    nomePart = 'Pt' + nomeModelo
    #
    modelarPart(nomeModelo = nomeModelo, nomePart = nomePart, localizacaoRodaMediaX = aviaoSelecionado.localizacaoRodaMediaX)
    #
    #Datums de camadas
    # Datums de camadas
    # Criação do material de revestimento no Abaqus 
    criarMaterialAbaqus(nomeModelo = nomeModelo, nomeMaterial = materialRevestimento.nomeMaterial, moduloElasticidade = materialRevestimento.moduloElasticidade, coeficientePoisson = materialRevestimento.coeficientePoisson)  
    # Criação do datum para a camada de revestimento
    criarDatum(nomeModelo = nomeModelo, nomePart = nomePart, offsetDatum = 2*aviaoSelecionado.localizacaoRodaMediaX -(materialRevestimento.espessuraCamada), planoPrincipalDatum = XYPLANE)
    datumCamadaRevestimento = mdb.models[nomeModelo].parts[nomePart].datums[2]
    # Criação do material de base no Abaqus
    criarMaterialAbaqus(nomeModelo = nomeModelo, nomeMaterial = materialBase.nomeMaterial, moduloElasticidade = materialBase.moduloElasticidade, coeficientePoisson = materialBase.coeficientePoisson)    
    criarDatum(nomeModelo=nomeModelo, nomePart=nomePart, offsetDatum= 2*aviaoSelecionado.localizacaoRodaMediaX -(materialRevestimento.espessuraCamada + materialBase.espessuraCamada), planoPrincipalDatum=XYPLANE)
    datumCamadaBase = mdb.models[nomeModelo].parts[nomePart].datums[3]
    criarMaterialAbaqus(nomeModelo = nomeModelo, nomeMaterial = materialSubleito.nomeMaterial, moduloElasticidade = materialSubleito.moduloElasticidade, coeficientePoisson = materialSubleito.coeficientePoisson)
    criarDatum(nomeModelo=nomeModelo, nomePart=nomePart, offsetDatum= 0, planoPrincipalDatum=XYPLANE)
    datumCamadaSubleito = mdb.models[nomeModelo].parts[nomePart].datums[4]
    criarDatum(nomeModelo=nomeModelo, nomePart=nomePart, offsetDatum= 2*aviaoSelecionado.localizacaoRodaMediaX, planoPrincipalDatum=XYPLANE)
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
    ####################################################################################################
    #Criação de reference points
    ## 0, roda ###
    #Eixo simples
    if aviaoSelecionado.tipoEixo == 'simples':
        #0, topo superficie
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(0.0, aviaoSelecionado.rodaInternaY, 2*aviaoSelecionado.localizacaoRodaMediaX))
        #0, topo da base
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(0.0, aviaoSelecionado.rodaInternaY, 2*aviaoSelecionado.localizacaoRodaMediaX - materialRevestimento.espessuraCamada))
        #0, topo do subleito
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(0.0, aviaoSelecionado.rodaInternaY, 2*aviaoSelecionado.localizacaoRodaMediaX - materialRevestimento.espessuraCamada - materialBase.espessuraCamada))
    else:
        #Outros eixos
        #0, topo superficie
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(0.0, 0, 2*aviaoSelecionado.localizacaoRodaMediaX))
        #0, topo da base
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(0.0, 0, 2*aviaoSelecionado.localizacaoRodaMediaX - materialRevestimento.espessuraCamada))
        #0, topo do subleito
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(0.0, 0, 2*aviaoSelecionado.localizacaoRodaMediaX - materialRevestimento.espessuraCamada - materialBase.espessuraCamada))
    #
    if aviaoSelecionado.tipoEixo == 'simples':
        #0, topo superficie
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(aviaoSelecionado.rodaInternaX, aviaoSelecionado.rodaInternaY, 2*aviaoSelecionado.localizacaoRodaMediaX))
        #0, topo da base
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(aviaoSelecionado.rodaInternaX, aviaoSelecionado.rodaInternaY, 2*aviaoSelecionado.localizacaoRodaMediaX - materialRevestimento.espessuraCamada))
        #0, topo do subleito
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(aviaoSelecionado.rodaInternaX, aviaoSelecionado.rodaInternaY, 2*aviaoSelecionado.localizacaoRodaMediaX - materialRevestimento.espessuraCamada - materialBase.espessuraCamada))
    else:
        #Outros eixos
        #0, topo superficie
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(aviaoSelecionado.rodaInternaX, 0, 2*aviaoSelecionado.localizacaoRodaMediaX))
        #0, topo da base
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(aviaoSelecionado.rodaInternaX, 0, 2*aviaoSelecionado.localizacaoRodaMediaX - materialRevestimento.espessuraCamada))
        #0, topo do subleito
        mdb.models[nomeModelo].rootAssembly.ReferencePoint(point=(aviaoSelecionado.rodaInternaX, 0, 2*aviaoSelecionado.localizacaoRodaMediaX - materialRevestimento.espessuraCamada - materialBase.espessuraCamada))
    ## 0 ###
    # Ponto de simetria do eixo - Geometrico
    # Ponto deembaixo do pneu
    # Ponto de simetria do pneu
    # Para cada aeronave
    #Datums de rodas
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
    #
    # Definicao do Reference Point
    #mdb.models[nomeModelo].parts[nomePart].ReferencePoint(point=mdb.models[nomeModelo].parts[nomePart].vertices[6])
    #
    # Definicao das condicoes de contorno
    # Boeing 737-800
    #
    # Fundo
    bcNomeFundo = 'fnd' + nomePart
    #mdb.models[nomeModelo].rootAssembly.Set(name=bcNomeFundo, vertices=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].vertices.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoFundo, ), ))
    mdb.models[nomeModelo].rootAssembly.Set(faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoFundo, ), ), name=bcNomeFundo)
    mdb.models[nomeModelo].DisplacementBC(amplitude=UNSET, createStepName='Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=bcNomeFundo, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeFundo], u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET)
    # Simetria
    bcNomeSimetriaY = 'smty' + nomePart
    #mdb.models[nomeModelo].rootAssembly.Set(name=bcNomeSimetriaY, vertices=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].vertices.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoSimetriaY, ), ))
    mdb.models[nomeModelo].rootAssembly.Set(faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoSimetriaY , ), ), name=bcNomeSimetriaY)
    mdb.models[nomeModelo].YsymmBC(createStepName='Initial', localCsys=None, name=bcNomeSimetriaY, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeSimetriaY])
    bcNomeSimetriaX = 'smtx' + nomePart
    #mdb.models[nomeModelo].rootAssembly.Set(name=bcNomeSimetriaX, vertices=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].vertices.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoSimetriaX, ), ))
    mdb.models[nomeModelo].rootAssembly.Set(faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoSimetriaX, ), ), name=bcNomeSimetriaX)
    mdb.models[nomeModelo].XsymmBC(createStepName='Initial', localCsys=None, name=bcNomeSimetriaX, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeSimetriaX])
    #
    #
    # Trava X
    # bcNomeTravaX = 'tvX' + nomePart
    # mdb.models[nomeModelo].rootAssembly.Set(name=bcNomeTravaX, vertices=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].vertices.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoTravaX, ), ))
    # mdb.models[nomeModelo].DisplacementBC(amplitude=UNSET, createStepName='Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=bcNomeTravaX, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeTravaX], u1=SET, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
    # Trava Y
    bcNomeTravaY = 'tvY' + nomePart
#    mdb.models[nomeModelo].rootAssembly.Set(name=bcNomeTravaY, vertices=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].vertices.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoTravaY, ), ))
    mdb.models[nomeModelo].rootAssembly.Set(faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoTravaY, ), ), name=bcNomeTravaY)
    mdb.models[nomeModelo].DisplacementBC(amplitude=UNSET, createStepName='Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=bcNomeTravaY, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeTravaY], u1=UNSET, u2=SET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
    # Trava Canto
    # bcNomeTravaCanto = 'tvC' + nomePart
    # mdb.models[nomeModelo].rootAssembly.Set(name=bcNomeTravaCanto, vertices=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].vertices.getSequenceFromMask((aviaoSelecionado.mascaraCondicaoContornoTravaCanto, ), ))
    # mdb.models[nomeModelo].YsymmBC(createStepName='Initial', localCsys=None, name=bcNomeTravaCanto, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeTravaCanto])
    # #mdb.models[nomeModelo].DisplacementBC(amplitude=UNSET, createStepName='Initial', distributionType=UNIFORM, fieldName='', localCsys=None, name=bcNomeTravaCanto, region=mdb.models[nomeModelo].rootAssembly.sets[bcNomeTravaCanto], u1=SET, u2=SET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
    #
    # Field Output
    mdb.models[nomeModelo].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'E', 'U'))
    ## é tandem triplo?
    if aviaoSelecionado.tipoEixo == 'tandemTriplo':
        criarDatum(nomeModelo = nomeModelo, nomePart = nomePart, offsetDatum = aviaoSelecionado.comprimentoContatoPneu/2, planoPrincipalDatum = aviaoSelecionado.planoPrincipalDatumRoda1_3)
        datumRoda3_1 = mdb.models[nomeModelo].parts[nomePart].datums[23]
        recortarPartPorDatum(nomeModelo = nomeModelo, nomePart = nomePart, objetoDatum = datumRoda3_1)
        mdb.models[nomeModelo].rootAssembly.Surface(name=nomeSuperficie, side1Faces=mdb.models[nomeModelo].rootAssembly.instances[nomeAssembly].faces.getSequenceFromMask(('[#0:2 #240 #11000000 #0 #400000 #200 ]', ), ))
    # Mesh
    # mdb.models[nomeModelo].parts[nomePart].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=0.25)
    # mdb.models[nomeModelo].parts[nomePart].generateMesh()
    if aviaoSelecionado.tipoEixo == 'simples':
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#7d640008 #0 #8000700e #403f403 ]', ), ), minSizeFactor=0.1, size=0.05)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#2800227 #0 #30100000 #40440a2c ]', ), ), minSizeFactor=0.1, size=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0 #40000000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#80000000 #280420 #11 ]', ), ), maxSize=0.75, minSize=0.05)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:4 #10 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#110000 #0:3 #1 ]', ), ), maxSize=0.75, minSize=0.05)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:2 #400 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0 #10008000 #20000 ]', ), ), maxSize=0.75, minSize=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:3 #20000000 ]', ), ), maxSize=0.75, minSize=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#950 #0 #40000000 #50 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:2 #200000 ]', ), ), maxSize=0.75, minSize=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#ad480 #afd77bdf #fcd8be0 #83a80180 #e ]', ), ), minSizeFactor=0.1, size=0.75)
    elif aviaoSelecionado.tipoEixo == 'tandemDuplo':
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#fe422 #80002200 #16789fff #4000fe0 #1ffa389 #10 #1e000020 ]', ), ), minSizeFactor=0.1, size=0.05)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#30005d #22240080 #49876000 #48410000 #6005c36 #c #600000', ' #10 ]'), ), minSizeFactor=0.1, size=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#ac00000 #44480000 #0 #80820000 #b8000000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:4 #40 ]', ), ), maxSize=0.75, minSize=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#100 #0 #80000000 #0:4 #8 ]', ), ), maxSize=0.75, minSize=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:6 #800 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:5 #100000 #8001 ]', ), ), maxSize=0.75, minSize=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:7 #400 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#1080 #4400 #0 #14 #0:3 #40 ]', ), ), maxSize=0.75, minSize=0.05)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:6 #4 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:5 #5010820 #50 ]', ), ), maxSize=0.75, minSize=0.05)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#f5000a00 #1993987f #20000000 #333cf00b #40000000 #faeef7c3 #e19f778a', ' #3a7 ]'), ), minSizeFactor=0.1, size=0.75)
    elif aviaoSelecionado.tipoEixo == 'tandemTriplo':
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#80007f92 #fec1c20 #44000074 #1fc8 #fff00044 #122001f3 #2003ff47', ' #1000000 #f000 ]'), ), minSizeFactor=0.1, size=0.05)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#1806d #c0102000 #ba01c988 #6000 #92801 #6cc8800c #180c00b8', ' #0 #800300 ]'), ), minSizeFactor=0.1, size=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:8 #20000000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#48000000 #41 #0 #21 #88 #0:3 #2000000 ]', ), ), maxSize=0.75, minSize=0.05)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:7 #200000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:6 #40000000 #2802a12 ]', ), ), maxSize=0.75, minSize=0.05)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#1000000 #4000 #0 #2:2 #0:3 #400000 ]', ), ), maxSize=0.75, minSize=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:7 #40000000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:7 #80080 #4 ]', ), ), maxSize=0.75, minSize=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#560000 #0 #442002 #158000 #0 #1110000 #1700000 ]', ), ), end2Edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#0:5 #80000000 ]', ), ), maxSize=0.75, minSize=0.25)
        mdb.models[nomeModelo].parts[nomePart].seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=mdb.models[nomeModelo].parts[nomePart].edges.getSequenceFromMask(('[#36a80000 #3003839e #1ba1601 #ffea0014 #6d730 #67e00 #86800000', ' #bc57d76d #1d3f0cfb ]'), ), minSizeFactor=0.1, size=0.75)
    mdb.models[nomeModelo].parts[nomePart].generateMesh()
    #regerar assembly
    mdb.models[nomeModelo].rootAssembly.regenerate()
    # Job
    nomeJob = 'job' + nomePart
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model=nomeModelo, modelPrint=OFF, 
    multiprocessingMode=THREADS, name=nomeJob, nodalOutputPrecision=FULL, numCpus=24, numDomains=24, numGPUs=1, queue=None, resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
    mdb.jobs[nomeJob].writeInput(consistencyChecking=OFF)
    return saidaModelos(nomeJob = nomeJob, nomeStep = nomeStep, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = valorSensibilidade, modeloAviao = aviaoSelecionado.modelo, nosInteresse = aviaoSelecionado.nosInteresse)


def rangeSensibilidade(indiceInicial, numeroRepeticoes, fatorDeCrescimento):
    return [round(indiceInicial * (fatorDeCrescimento ** i), 4) for i in range(numeroRepeticoes)]

def inicializarCodigo(rodarJobs):
    # Função para inicializar o código com base em parâmetros de entrada
    # boeing737800 = aviao(modelo='B737800', tipoEixo = 'simples',roda1DistanciaEixoNuloX=3.2893,roda1DistanciaEixoNuloY=0, roda2DistanciaEixoNuloX=2.4257, roda2DistanciaEixoNuloY = 0, larguraContatoPneu=0.323, comprimentoContatoPneu=0.517, 
    #                     carregamento=1406.53,  mascaraCondicaoContornoFundo = '[#b10 #8022004 ]' ,mascaraCondicaoContornoSimetriaX = '[#14c00000 #7f99ac2 ]', mascaraCondicaoContornoSimetriaY = '[#a00c0 #594b0 ]', 
    #                     mascaraCondicaoContornoTravaX = '[#a9100000 #4109 ]', mascaraCondicaoContornoTravaY = '[#5400]', mascaraCondicaoContornoTravaCanto = '[#42200000 ]', mascaraSuperficie = '[#0 #200000 #100 ]', nosInteresse=[53, 57, 56, 39, 44, 47])
    # # Cria um objeto avião do modelo Boeing 737-800 com parâmetros específicos
    # boeing767300 = aviao(modelo='B767300', tipoEixo = 'tandemDuplo', roda1DistanciaEixoNuloX=5.2197, roda1DistanciaEixoNuloY=0.7112, roda2DistanciaEixoNuloX=4.0767,  roda2DistanciaEixoNuloY = 0.7112, larguraContatoPneu=0.332, comprimentoContatoPneu=0.531, 
    #                     carregamento=1344.48, mascaraCondicaoContornoFundo = '[#20be8000 #14 #82001800 #a ]' ,mascaraCondicaoContornoSimetriaX = '[#0 #ff000000 #987bd ]', mascaraCondicaoContornoSimetriaY = '[#c0017000 #80803201 #580002c8 #4 ]', 
    #                     mascaraCondicaoContornoTravaX = '[#94002c0 #380000 ]', mascaraCondicaoContornoTravaY = '[#0:2 #25b22000 #1 ]', mascaraCondicaoContornoTravaCanto = '[#0:2 #444000 ]',  mascaraSuperficie = '[#48000000 #0 #22000 ]', nosInteresse=[10, 1, 0, 13, 45, 31, 73, 71, 67])
    # # Cria um objeto avião do modelo Boeing 767-300 com parâmetros específicos
    # boeing777300 = aviao(modelo='B777300', tipoEixo = 'tandemTriplo', roda1DistanciaEixoNuloX=6.1849, roda1DistanciaEixoNuloY=1.4478, roda2DistanciaEixoNuloX=4.7879, roda2DistanciaEixoNuloY = 1.4478, larguraContatoPneu=0.354, comprimentoContatoPneu=0.566, 
    #                     carregamento=1482.37, mascaraCondicaoContornoFundo = '[#20be8000 #14 #82001800 #a ]' ,mascaraCondicaoContornoSimetriaX = '[#0 #ff000000 #987bd ]', mascaraCondicaoContornoSimetriaY = '[#c0017000 #80803201 #580002c8 #4 ]', 
    #                     mascaraCondicaoContornoTravaX = '[#94002c0 #380000 ]', mascaraCondicaoContornoTravaY = '[#0:2 #25b22000 #1 ]', mascaraCondicaoContornoTravaCanto = '[#0:2 #444000 ]',  mascaraSuperficie = '[#48000000 #0 #22000 ]', nosInteresse=[57, 71, 47, 95, 89, 85, 60, 59, 61, 96, 94, 90])
    boeing737800 = aviao(modelo='B737800', tipoEixo = 'simples',roda1DistanciaEixoNuloX=3.2893,roda1DistanciaEixoNuloY=0, roda2DistanciaEixoNuloX=2.4257, roda2DistanciaEixoNuloY = 0, larguraContatoPneu=0.323, comprimentoContatoPneu=0.517, 
                        carregamento=1406.53,  mascaraCondicaoContornoFundo = '[#1000000 #8181 #2010 #2 ]' ,mascaraCondicaoContornoSimetriaX = '[#0 #20144000 #8140c409 ]', mascaraCondicaoContornoSimetriaY = '[#804a000 #42 #5a280000 ]', 
                        mascaraCondicaoContornoTravaY = '[#0 #48890000 #24110a02 ]', mascaraSuperficie = '[#0 #200000 #100 ]', nosInteresse=[53, 57, 56, 39, 44, 47])
    # Cria um objeto avião do modelo Boeing 737-800 com parâmetros específicos
    boeing767300 = aviao(modelo='B767300', tipoEixo = 'tandemDuplo', roda1DistanciaEixoNuloX=5.2197, roda1DistanciaEixoNuloY=0.7112, roda2DistanciaEixoNuloX=4.0767,  roda2DistanciaEixoNuloY = 0.7112, larguraContatoPneu=0.332, comprimentoContatoPneu=0.531, 
                        carregamento=1344.48, mascaraCondicaoContornoFundo = '[#1481000 #4800000 #9 #60404000 #4000020 #800008 ]' ,mascaraCondicaoContornoSimetriaX = '[#0:4 #2480510 #205031 ]', mascaraCondicaoContornoSimetriaY = '[#80126000 #51000001 #44100 #10820128 #0 #168a00 ]', 
                        mascaraCondicaoContornoTravaY = '[#0:4 #80922240 #90442 ]', mascaraSuperficie = '[#48000000 #0 #22000 ]', nosInteresse=[10, 1, 0, 13, 45, 31, 73, 71, 67])
    # Cria um objeto avião do modelo Boeing 767-300 com parâmetros específicos
    boeing777300 = aviao(modelo='B777300', tipoEixo = 'tandemTriplo', roda1DistanciaEixoNuloX=6.1849, roda1DistanciaEixoNuloY=1.4478, roda2DistanciaEixoNuloX=4.7879, roda2DistanciaEixoNuloY = 1.4478, larguraContatoPneu=0.354, comprimentoContatoPneu=0.566, 
                        carregamento=1482.37, mascaraCondicaoContornoFundo = '[#1481000 #4800000 #9 #60404000 #4000020 #800008 ]',mascaraCondicaoContornoSimetriaX = '[#0:4 #2480510 #205031 ]', mascaraCondicaoContornoSimetriaY = '[#80126000 #51000001 #44100 #10820128 #0 #168a00 ]', 
                        mascaraCondicaoContornoTravaY = '[#0:4 #80922240 #90442 ]', mascaraSuperficie = '[#48000000 #0 #22000 ]', nosInteresse=[57, 71, 47, 95, 89, 85, 60, 59, 61, 96, 94, 90])
    # Cria um objeto avião do modelo Boeing 777-300 com parâmetros específicos
    #
    #aviaoSelecionado = boeing777300
    # Define o avião selecionado como o Boeing 737-800
    materialRevestimentoOriginal = material(nomeCamada='Revestimento', nomeMaterial='Camada asfaltica', espessuraCamada=0.1, moduloElasticidade=1500000000, coeficientePoisson=0.30)
    materialRevestimento = materialRevestimentoOriginal
    # Cria um objeto material para a camada de revestimento com parâmetros específicos
    materialBaseOriginal = material(nomeCamada='Base', nomeMaterial='BGS', espessuraCamada=0.3, moduloElasticidade=250000000, coeficientePoisson=0.35)
    materialBase = materialBaseOriginal
    # Cria um objeto material para a camada base com parâmetros específicos
    materialSubleitoOriginal = material(nomeCamada='Subleito', nomeMaterial='Material do Subleito', espessuraCamada=5, moduloElasticidade=200000000, coeficientePoisson=0.40)
    materialSubleito = materialSubleitoOriginal
    #
    # Cria um objeto material para o subleito com parâmetros específicos
    nomeSensibilidade= 'Base'
    listaJobs = []
    listaJobs.append(criarModelo(aviaoSelecionado=boeing737800, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = 0))
    listaJobs.append(criarModelo(aviaoSelecionado=boeing767300, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = 0))
    listaJobs.append(criarModelo(aviaoSelecionado=boeing777300, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = 0))
    # Cria um modelo utilizando o avião selecionado e os materiais definidos, e adiciona o job à lista de jobs
    ######
    ###### Variacoes
    #Investigacao espessura camada revestimento
    listaAvioes = [boeing737800, boeing767300, boeing777300]
    # numeroRepeticoes = 1 # Mudar para 50 depois
    # for aviaoSelecionado in listaAvioes:
    #     nomeSensibilidade= 'espRev'
    #     for espessuraRevestimento in rangeSensibilidade(indiceInicial = 0.1, numeroRepeticoes=numeroRepeticoes, fatorDeCrescimento=1.05):
    #         materialRevestimento.espessuraCamada = espessuraRevestimento
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = espessuraRevestimento))
    #     materialRevestimento = materialRevestimentoOriginal
    #     nomeSensibilidade= 'espBas'
    #     for espessuraBase in rangeSensibilidade(indiceInicial = 0.2, numeroRepeticoes=numeroRepeticoes, fatorDeCrescimento=1.05):
    #         materialBase.espessuraCamada = espessuraBase
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = espessuraBase))
    #     materialBase = materialBaseOriginal
    #     nomeSensibilidade= 'elasRev'
    #     for elasticidadeRevestimento in rangeSensibilidade(indiceInicial = 300E6, numeroRepeticoes=numeroRepeticoes, fatorDeCrescimento=1.05):
    #         materialRevestimento.moduloElasticidade = elasticidadeRevestimento
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = elasticidadeRevestimento))
    #     materialRevestimento = materialRevestimentoOriginal
    #     nomeSensibilidade= 'elasBas'
    #     for elasticidadeBase in rangeSensibilidade(indiceInicial = 100E6, numeroRepeticoes=numeroRepeticoes, fatorDeCrescimento=1.05):
    #         materialBase.moduloElasticidade = elasticidadeBase
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = elasticidadeBase))
    #     materialBase = materialBaseOriginal
    #     nomeSensibilidade= 'elasSub'
    #     for elasticidadeSubleito in rangeSensibilidade(indiceInicial = 50E6, numeroRepeticoes=numeroRepeticoes, fatorDeCrescimento=1.05):
    #         materialSubleito.moduloElasticidade = elasticidadeSubleito
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = elasticidadeSubleito))
    #     materialSubleito = materialSubleitoOriginal
    #     nomeSensibilidade= 'poiRev'
    #     for poissonRevestimento in rangeSensibilidade(indiceInicial = 0.08, numeroRepeticoes=numeroRepeticoes, fatorDeCrescimento=1.05):
    #         materialRevestimento.coeficientePoisson = poissonRevestimento
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = poissonRevestimento))
    #     materialRevestimento = materialRevestimentoOriginal
    #     nomeSensibilidade= 'poiBas'
    #     for poissonBase in rangeSensibilidade(indiceInicial = 0.08, numeroRepeticoes=numeroRepeticoes, fatorDeCrescimento=1.05):
    #         materialBase.coeficientePoisson = poissonBase
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = poissonBase))
    #     materialBase = materialBaseOriginal
    #     nomeSensibilidade= 'poiSub'
    #     for poissonSubleito in rangeSensibilidade(indiceInicial = 0.08, numeroRepeticoes=numeroRepeticoes, fatorDeCrescimento=1.05):
    #         materialSubleito.coeficientePoisson = poissonSubleito
    #         listaJobs.append(criarModelo(aviaoSelecionado=aviaoSelecionado, materialRevestimento=materialRevestimento, materialBase=materialBase, materialSubleito=materialSubleito, nomeSensibilidade = nomeSensibilidade, valorSensibilidade = poissonSubleito))
    #     materialSubleito = materialSubleitoOriginal
# Convertendo a lista de objetos em uma lista de dicionários para saida em JSON
    modelos_Saida = []
    for objeto in listaJobs:
        dicionario = {
            "nomeJob": objeto.nomeJob,
            "nomeStep": objeto.nomeStep,
            "nomeSensibilidade": objeto.nomeSensibilidade,
            "valorSensibilidade": objeto.valorSensibilidade,
            "modeloAviao": objeto.modeloAviao,
            "nosInteresse": objeto.nosInteresse
        }
        modelos_Saida.append(dicionario)
    # Escrevendo a lista de dicionários em um arquivo JSON
    with open("dadosModelosSaida.json", "w") as arquivo_json:
        json.dump(modelos_Saida, arquivo_json, indent=4)
        if rodarJobs == True:
            # Se a variável rodarJobs for True, executa os jobs
            for job in listaJobs:
                mdb.jobs[job.nomeJob].submit(consistencyChecking=OFF)
                #job.submit(consistencyChecking=OFF)
                #mdb.jobs[job.nomeJob].waitForCompletion()
                print([job.nomeJob, mdb.jobs[job.nomeJob].status])
                # Submete cada job para execução

#Executa a funcao que inicializa o  codigo
inicializarCodigo(rodarJobs = False)
# Remove o modelo com nome 'Model-1' do dicionário mdb.models  
del mdb.models['Model-1']

