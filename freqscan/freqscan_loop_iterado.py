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
s
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
harmonicos = np.arange(1,26,2).tolist()
dss.text("New spectrum.espectroharmonico numharm={} csvfile=espectro_harmonico_reduzido.csv".format(str(len(harmonicos))))

# Cria loop de fonte de corrente harmônica
for j in range(3,len(nomesNos)):
    #  Adiciona a fonte de corrente harmônica de sequência positiva
    node = nomesNos[j]
    barra = node.split(".")
    barra = barra[0]
    scansource = "Isource.scansource{}".format(node)
    dss.text("New {} bus1={} amps=1 spectrum=espectroharmonico".format(scansource,node))

    dss.solution.solve()

    # Seleciona o modo de solução harmonic
    dss.text("Set mode=harmonic")

    #matrixVmag = pd.DataFrame()
    #matrixVmagpu = pd.DataFrame()
    matrixV = pd.DataFrame()

    print("Nó " + node)
    # Realiza a solução harmônica iterada
    for h in range(len(harmonicos)):
        dss.text("Set harmonic={}".format(harmonicos[h]))
        dss.solution.solve()
        indice = "node_" + str(node) + "_harmonico_" + str(harmonicos[h]*60)
        #matrixVmag[indice] = dss.circuit.buses_vmag
        #matrixVmagpu[indice] = dss.circuit.buses_vmag_pu
        matrixV[indice] = dss.circuit.buses_volts
        dss.monitors.reset_all()

        print("Harmonico " + str(harmonicos[h]*60))

    #matrixVmag.to_csv("vmag_node_{}.csv".format(node))
    #matrixVmagpu.to_csv("vmagpu_node_{}.csv".format(node))
    matrixV.to_csv("v_node_{}.csv".format(node))

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
