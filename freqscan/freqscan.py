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
harmonicos = np.arange(1,25.25,0.25).tolist()
dss.text("New spectrum.espectroharmonico numharm={} csvfile=espectro_harmonico.csv".format(str(len(harmonicos))))

#  Adiciona a fonte de corrente harmônica de sequência positiva
#barra = nomesBarras[3]
barra = '814'
dss.text("New Isource.scansource bus1={} amps=1 spectrum=espectroharmonico".format(barra))
dss.solution.solve()

# Seleciona o modo de solução harmonic
dss.text("Set mode=harmonic")

matrixV = pd.DataFrame()
matrixVpu = pd.DataFrame()

for h in range(len(harmonicos)):
    dss.text("Set harmonic={}".format(harmonicos[h]))
    dss.solution.solve()
    matrixV[harmonicos[h]] = dss.circuit.buses_vmag
    matrixVpu[harmonicos[h]] = dss.circuit.buses_vmag_pu

# Exporta todos os valores dos monitores
dss.text("Export monitors all")

## Plota todos os monitores
#for k in range(len(nomesMonitores)):
#    monitor = nomesMonitores[k]
#    print("Plot monitor object={} channels=(1 3 5)".format(monitor))
#    dss.text("Plot monitor object={} channels=(1 3 5)".format(monitor))

print("Análise harmônica finalizada")

matrixVrol = matrixVpu.sort_values(by=[1.0])
meio = int(round(len(matrixVrol)/2))
mediana = matrixVrol.iloc[meio]

matrixVpuharmonico = matrixVpu[matrixVpu > 0.01]
print(matrixVpu)


"""
matrixV = pd.DataFrame(dss.circuit.buses_vmag)
matrixVharmonico = matrixV[matrixV[0] > 0.001]
print(matrixVharmonico)

matrixVpu = pd.DataFrame(dss.circuit.buses_vmag_pu)
matrixVpuharmonico = matrixVpu[matrixVpu[0] > 0.001]
print(matrixVpuharmonico)

"""
