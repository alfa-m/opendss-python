import pandas as pd
import numpy as np

frequencia_inicial = 60
frequencia_final = 3000
passo_frequencia = 15

harmonico_pd = pd.DataFrame()
harmonico_pd['harmonico'] = np.arange(frequencia_inicial,(frequencia_final + 1),passo_frequencia).tolist()
harmonico_pd['harmonico'] = harmonico_pd['harmonico'].apply(lambda h : round((h/60), 6))
harmonico_pd['amplitude'] = 100
harmonico_pd['angulo'] = 0

harmonico_pd.to_csv("espectro_harmonico.csv", index=False, header=None)

print("Arquivo .csv de espectro harmônico criado")
