import pandas as pd
import numpy as np


df = pd.read_csv('Fm22/moneynuts.csv')

df = df.replace("-", pd.np.nan)
df = df.dropna(subset=['Gls'])
#df_sort = df.sort_values('Gls')
print(df)

#df_sorted = df.sort_values('column_name')

for index, row in df.iterrows():
    print("index:", index, "Naam:", row['Name'], " Club:", row['Club'], "Goals:", row['Gls']) 
