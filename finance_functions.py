import pandas as pd
import requests as r
import json 
import yfinance as yf


with open ("fin_modeling_key.txt", "r") as fin_key:
    fkey = fin_key.read ().strip ()

qqq_tickers = pd.read_csv ("tickers_qqq.csv", header =None)
snp_tickers = pd.read_csv ("snp500.csv")


def exchange_name (company:str):
    url = f'https://financialmodelingprep.com/stable/search-symbol?query={company}&apikey={fkey}'
    data = pd.DataFrame (r.get (url).json ()) ['exchangeFullName']
    data = data.to_list ()
    return data


def pe_qqq ():
    tick_list = qqq_tickers[0].to_list ()
    tickers_info = yf.Tickers(tick_list)

    dictionary_pe = dict ()

    for tick in tick_list:
        try:
            temp_tick = tickers_info.tickers [tick].info ['trailingPE']
        except:
            temp_tick = None
            print (f"Ticker {tick} doesn't have PE ratio!")

        try:
            temp_tick_div = tickers_info.tickers [tick].info ['dividendYield']
        except:
            temp_tick_div = None
            print (f"Ticker {tick} doesn't have Dividends!")
        
        dictionary_pe[tick] = [temp_tick, temp_tick_div]
    
    df_pe = pd.DataFrame (data = dictionary_pe.values (), columns = ["PE", "DIV"],index = dictionary_pe.keys ())
    df_pe = df_pe.dropna(subset = 'PE', axis=0)
    df_pe_sorted_head = df_pe.sort_values (by = "PE", ascending = True).head ()
    return df_pe_sorted_head


def pe_snp ():
    tick_list = snp_tickers['Symbol'].to_list ()
    tickers_info = yf.Tickers(tick_list)

    dictionary_pe = dict ()

    for tick in tick_list:
        try:
            temp_tick = tickers_info.tickers [tick].info ['trailingPE']
        except:
            temp_tick = None
            print (f"Ticker {tick} doesn't have PE ratio!")

        try:
            temp_tick_div = tickers_info.tickers [tick].info ['dividendYield']
        except:
            temp_tick_div = None
            print (f"Ticker {tick} doesn't have Dividends!")
        
        dictionary_pe[tick] = [temp_tick, temp_tick_div]
    
    df_pe = pd.DataFrame (data = dictionary_pe.values (), columns = ["PE", "DIV"],index = dictionary_pe.keys ())
    df_pe = df_pe.dropna(subset = 'PE', axis=0)
    df_pe_sorted_head = df_pe.sort_values (by = "PE", ascending = True).head ()
    return df_pe_sorted_head
