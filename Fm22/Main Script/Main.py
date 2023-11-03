#libraries importeren
from fastapi import FastAPI
import json
import pandas as pd
import numpy as np

#dataframe maken van een csv bestand
df = pd.read_csv('Main script/data.csv')

#Not A Number of geen een waarde geven zodat het gefilterd kan worden
df = df.replace("-", np.nan)

#alles wat geen bruikbare data heeft eruit filteren
df = df.dropna(subset=['Dlp'])
#sorting van Goals en Subsort van xG
df = df.sort_values(['Dlp','xG'], ascending=[False,False])
#Naam,Club,Dlp en xG eruit filteren
df = df[['Naam','Club','Dlp','xG']]
#de gemanipuleerde dataframe omzetten naar een json bestand en opslaan in een export map
df.to_json('Exports/DataFiltered.json', orient='index')
#Bericht dat het filteren en exporteren is gelukt
print("Data gefilterd en geëxporteerd")