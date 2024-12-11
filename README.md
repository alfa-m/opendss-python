# Conteúdo
## [analise_por_frequencia](./analise_por_frequencia)
- Arquivo ["analise_por_frequencia.py"](./analise_por_frequencia/analise_por_frequencia.py): Código errado
- Arquivos csv:
  - Matriz I nodal (por frequência e total)
  - Matriz V nodal (por frequência e total)
  - Matriz Y (por frequência e total)

## [freqscan](./freqscan)
- Arquivos para a simulação em OpenDSS:
  - ["ieee34Mod1.dss"](./freqscan/ieee34Mod1.dss): Arquivo com circuito IEEE 34 barras
  - ["IEEELineCodes.DSS"](./freqscan/IEEELineCodes.DSS): Arquivo com código das linhas do circuito
  - ["BusCoords.dat"](./freqscan/BusCoords.dat): Arquivo com coordenadas das barras do circuito
  - ["espectro_harmonico.csv"](./freqscan/espectro_harmonico.csv): Arquivo com o espectro harmônico de 1 a 25, com passo incremental de 0.25
  - ["espectro_harmonico_reduzido.csv"](./freqscan/espectro_harmonico_reduzido.csv): Arquivo com o espectro harmônico de 1 a 25, com passo incremental de 2
- Arquivo ["freqscan_loop_iterado.py"](./freqscan/freqscan_loop_iterado.py): ARQUIVO CORRETO
- Demais arquivos python: Incorretos ou variações do arquivo acima
- Arquivos csv:
  - "vmag_node_[nome do nó]": Arquivo com medições da magnitude de V por nó no circuito. Existe um para cada nó. Arquivos sendo utilizados nas análises
  - "vmagpu_node_[nome do nó]": Arquivo com medições da magnitude de V em pu por nó no circuito. Existe um para cada nó. Arquivos sendo utilizados nas análises
  - ["lista_de_barras"](./freqscan/lista_de_barras.csv): Arquivo contendo os nomes das barras
  - ["lista_de_nos"](./freqscan/lista_de_nos.csv): Arquivo contendo os nomes dos nós
  - "Vmag - Barra  [nome da barra]": Arquivo com medições da magnitude de V por barra do circuito. Existe um para cada barra
  - "Vmagpu - Barra  [nome da barra]": Arquivo com medições da magnitude de V em pu por barra do circuito. Existe um para cada barra
  - "ieee34-1_Mon_[nome do monitor]_[nome da barra]": Arquivo com capturas dos monitores do circuito. Existe um para cada combinação de monitor e barra
