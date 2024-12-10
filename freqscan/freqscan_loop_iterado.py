import py_dss_interface
import pandas as pd
import numpy as np
import os
import pathlib

# Inicializa o objeto DSS
dss = py_dss_interface.DSS(r"C:\Program Files\OpenDSS")

# Adiciona o path e compila o arquivo .dss
script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("ieee34Mod1.dss")
dss.text("Compile [{}]".format(dss_file))
dss.dssinterface.allow_forms = 0

# Adiciona dados de coordenadas das barras
dss.text("Buscoords BusCoords.dat")

# Cria variaveis contendo o nome das linhas, barras e nós 
nomesLinhas = dss.lines.names
nomesBarras = dss.circuit.buses_names
nomesNos = dss.circuit.nodes_names

# Realiza a solução do fluxo de potência para obter os valores de magnitude e fase das tensões e correntes
dss.solution.solve()

# Remove demais fontes harmonicas
dss.text("Spectrum.DefaultLoad.NumHarm=1")

# Adiciona um monitor em cada linha
for i in range(len(nomesLinhas)):
    linha = nomesLinhas[i]
    dss.text("New Monitor.MonitorLine{} Line.{} 1 mode=0".format(linha, linha))

# Salva nomes dos monitores
nomesMonitores = dss.monitors.names

# Define o espectro de frequências a serem analisadas
#harmonicos = np.arange(1,25.25,0.25).tolist()
harmonicos = np.arange(1,26,2).tolist()
dss.text("New spectrum.espectroharmonico numharm={} csvfile=espectro_harmonico_reduzido.csv".format(str(len(harmonicos))))

# Cria loop de fonte de corrente harmônica
#for j in range(1,len(nomesBarras)):
for j in range(3,len(nomesNos)):
    #  Adiciona a fonte de corrente harmônica de sequência positiva
    #barra = nomesBarras[j]
    no = nomesNos[j]
    barra = no.split(".")
    barra = barra[0]
    scansource = "Isource.scansource{}".format(no)
    dss.text("New {} bus1={} amps=1 spectrum=espectroharmonico".format(scansource,no))

    dss.solution.solve()

    # Seleciona o modo de solução harmonic
    dss.text("Set mode=harmonic")

    matrixV = pd.DataFrame()
    matrixVpu = pd.DataFrame()

    #print("Barra " + barra)
    print("Nó " + no)
    # Realiza a solução harmônica iterada
    for h in range(len(harmonicos)):
        dss.text("Set harmonic={}".format(harmonicos[h]))
        dss.solution.solve()
        #indice = "Barra " + str(barra) + " - harmonico " + str(harmonicos[h]*60)
        indice = "No " + str(no) + " - harmonico " + str(harmonicos[h]*60)
        matrixV[indice] = dss.circuit.buses_vmag
        matrixVpu[indice] = dss.circuit.buses_vmag_pu
        dss.monitors.reset_all()

        print("Harmonico " + str(harmonicos[h]*60))

    #matrixV.to_csv("Vmag - Barra {}.csv".format(barra))
    #matrixVpu.to_csv("Vmagpu - Barra {}.csv".format(barra))
    matrixV.to_csv("Vmag - Nó {}.csv".format(no))
    matrixVpu.to_csv("Vmagpu - Nó {}.csv".format(no))

    # Desabilita a fonte de corrente atual
    fontesCorrente = dss.isources.names
    ultimaFonteCorrente = fontesCorrente[(len(fontesCorrente)-1)]
    dss.text("Disable Isource.{}".format(ultimaFonteCorrente))

nomesBarras_df = pd.DataFrame(nomesBarras)
nomesNos_df = pd.DataFrame(nomesNos)
nomesBarras_df.to_csv("lista_de_barras.csv")
nomesNos_df.to_csv("lista_de_nos.csv")

## Exporta todos os valores dos monitores
#dss.text("Export monitors all")

## Plota todos os monitores
#for k in range(len(nomesMonitores)):
#    monitor = nomesMonitores[k]
#    dss.text("Plot monitor object={} channels=(1 3 5)".format(monitor))

print("Análise harmônica finalizada")
