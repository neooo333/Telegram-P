import pandas as pd
import requests as r
import json 


with open ("fin_modeling_key.txt", "r") as fin_key:
    fkey = fin_key.read ().strip ()


def exchange_name (company:str):
    url = f'https://financialmodelingprep.com/stable/search-symbol?query={company}&apikey={fkey}'
    data = pd.DataFrame (r.get (url).json ()) ['exchangeFullName']
    data = data.to_list ()
    return data
