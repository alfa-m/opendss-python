import py_dss_interface
import pandas as pd

dss = py_dss_interface.DSS(r"C:\Program Files\OpenDSS")

dss_file_path = r"C:\Program Files\OpenDSS\IEEETestCases\34Bus\ieee34Mod1.dss"
dss.text("Compile [{}]".format(dss_file_path))
dss.text("Buscoords IEEE34_BusXY.csv")

nomesLinhas = dss.lines.names
nomesNos = dss.circuit.y_node_order

dss.solution.solve()

pd.DataFrame(dss.circuit.system_y).to_csv("D:\\Polar Files\\Documents\\TCC\\Python\\opendss\\Y_freq_teste.csv", sep=',')

dss.text("Spectrum.DefaultLoad.NumHarm=1")

for i in range(len(nomesLinhas)):
    linha = nomesLinhas[i]
    dss.text("New Monitor.MonitorLine{} Line.{} 1 mode=0".format(linha, linha))

nomesMonitores = dss.monitors.names

dss.solution.solve()

dss.text("Set mode=harmonic")

matrizAdmitancia = pd.DataFrame()
tensaoNodal = pd.DataFrame()
correnteNodal = pd.DataFrame()

for harmonic in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]:
        dss.text(f"set harmonics=[{harmonic}]")
        dss.solution.solve()

        matrizAdmitancia[harmonic] = dss.circuit.system_y
        nome_csv_admitancia = "D:\\Polar Files\\Documents\\TCC\\Python\\opendss\\Y_freq_" + str(harmonic) + ".csv"
        pd.DataFrame(dss.circuit.system_y).to_csv(nome_csv_admitancia, sep=',')

        tensaoNodal[harmonic] = dss.circuit.y_node_varray
        nome_csv_tensao = "D:\\Polar Files\\Documents\\TCC\\Python\\opendss\\V_nodal_freq_" + str(harmonic) + ".csv"
        pd.DataFrame(dss.circuit.system_y).to_csv(nome_csv_tensao, sep=',')

        correnteNodal[harmonic] = dss.circuit.y_currents
        nome_csv_corrente = "D:\\Polar Files\\Documents\\TCC\\Python\\opendss\\I_nodal_freq_" + str(harmonic) + ".csv"
        pd.DataFrame(dss.circuit.system_y).to_csv(nome_csv_corrente, sep=',')

        """
        matrizY = pd.DataFrame()
        tamanhoY = len(nomesNos)
        i = 1
        for a in range(tamanhoY):
                linhaY = pd.DataFrame()
                for b in range(tamanhoY):
                        linhaY[a][b] = matrizAdmitancia[i][0] + i * matrizAdmitancia[i + 1][0]
                        i = i + 2
                matrizY[a] = linhaY
        """

matrizAdmitancia.to_csv("D:\\Polar Files\\Documents\\TCC\\Python\\opendss\\Y_freq_total.csv", sep=',')
tensaoNodal.to_csv("D:\\Polar Files\\Documents\\TCC\\Python\\opendss\\V_nodal_total.csv", sep=',')
correnteNodal.to_csv("D:\\Polar Files\\Documents\\TCC\\Python\\opendss\\I_nodal_total.csv", sep=',')
