import py_dss_interface
import pandas as pd

dss = py_dss_interface.DSS(r"C:\Program Files\OpenDSS")

dss_file_path = r"C:\Program Files\OpenDSS\IEEETestCases\34Bus\ieee34Mod1.dss"
dss.text("Compile [{}]".format(dss_file_path))
dss.text("Buscoords IEEE34_BusXY.csv")

nomesLinhas = dss.lines.names
#nomesBarras = dss.circuit.buses_names
nomesNos = dss.circuit.nodes_names

dss.solution.solve()

dss.text("Spectrum.DefaultLoad.NumHarm=1")

for i in range(len(nomesLinhas)):
    linha = nomesLinhas[i]
    dss.text("New Monitor.MonitorLine{} Line.{} 1 mode=0".format(linha, linha))

nomesMonitores = dss.monitors.names

dss.text("Set number=1")
dss.solution.solve()

dss.text("Set mode=harmonic")

matrizAdmitancia = pd.DataFrame()
tensaoNodal = pd.DataFrame()
correnteNodal = pd.DataFrame()

for harmonic in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]:
        dss.text(f"set harmonics=[{harmonic}]")
        dss.solution.solve()
        matrizAdmitancia[harmonic] = dss.circuit.system_y
        nome_csv = "D:\\Polar Files\\Documents\\TCC\\Python\\opendss\\Y_freq_" + str(harmonic) + ".csv"
        matrizAdmitancia.to_csv(nome_csv, sep=',')


matrizAdmitancia['total'] = dss.circuit.system_y
matrizAdmitancia.to_csv("D:\\Polar Files\\Documents\\TCC\\Python\\opendss\\Y_freq.csv", sep=',')
