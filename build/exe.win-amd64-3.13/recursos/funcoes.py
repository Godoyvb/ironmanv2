import os, time
import json
from datetime import datetime

ARQUIVO_LOG = "log.dat"

def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open(ARQUIVO_LOG,"r")
        banco.close()
    except:
        print("Log Inexistente. Criando...")
        banco = open(ARQUIVO_LOG,"w")
        banco.close()
    
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open(ARQUIVO_LOG,"r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    hora_br = datetime.now().strftime("%H:%M:%S")
    dadosDict[nome] = (pontos, data_br, hora_br)
    
    banco = open(ARQUIVO_LOG,"w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo
    
def maior_pontuador():
    banco = open(ARQUIVO_LOG,"r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}

    nome_maior = None
    dataJogada =  None
    maior_pontos = -1

    for nome, info in dadosDict.items():

        pontos = info[0]
        
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior = nome
            if len(info) > 2:
                dataJogada = f"{info[1]} {info[2]}"
            else:
                dataJogada = info[1]

    return nome_maior, maior_pontos, dataJogada
