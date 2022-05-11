import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import xlwings as xw
from datetime import timedelta


# Funcion de bienvenida

def bienvenida():
    print('\n')
    print('####################################################')
    print('################# RICKY INVESTING ##################')
    print('####################################################')
    print('\n')

# Esta función tomará las acciones con las que genererará el dataframe
def acciones_list(n:int):
    acciones = []
    for i in np.arange(1,n+1):
        a = input(f'Acción {i} del portafolio: ').upper()
        acciones.append(a)
    return acciones

# Función que crea el dataframe con los precios de cierre ajustado

def data(lista, inicio:str, fin:str):
    df = yf.download(lista[0],start=inicio,end=fin)
    df.drop(['Open','High','Low','Close','Volume'], axis = 1, inplace=True)
    df.dropna(inplace=True)
    df = df.rename(columns={'Adj Close':lista[0]})
    lista.pop(0)
    print(lista)
    for i in lista:
        name = i
        i = yf.download(i,start=inicio,end=fin)
        i.drop(['Open','High','Low','Close','Volume'], axis = 1, inplace=True)
        i.dropna(inplace=True)
        i = i.rename(columns={'Adj Close':name})
        df = df.join(i, how='outer')
    return df

def con_excel(df):
    wb = xw.Book()
    sheet_data = wb.sheets[0]
    sheet_data
    xw.sheets.active
    xw.books.active
    sheet_data.name = 'Data'
    sheet_data.range('A1').value = df
    return wb
    
# Función que genera un dataframe de rendimientos logaritmicos

def returns(df):
    wb = xw.books.active # Trabaja sobre el Libro creado
    wb.sheets.add() # Agrega una hoja nueva al Libro creado y activo
    sheet_estr1 = wb.sheets[0] # Se le asigna la hoja por posición
    sheet_estr1.name = 'Rendimientos' # Se le asigna nombre a la hoja por posición aqui viviran los resultados de rendimientos
    df_returns = np.log(df/df.shift(periods=1))
    df_returns.dropna(inplace=True)
    sheet_estr1.range('A1').value = df_returns

    l = len(df_returns.columns)
    print(l)
    sheet_estr1[1,l+2].value = df_returns.describe()
    medias = pd.DataFrame(df_returns.mean(axis=0)) # almacenando las medias en esta variable
    medias = medias.rename(columns={0:'r_med'})
    desv = pd.DataFrame(df_returns.std(axis=0)) # almacenando las desviaciones estandar en esta variable
    desv = desv.rename(columns={0:'r_desv'})
    estad = medias.join(desv,how='outer') # este es el dataframe de las medias y volatilidades de los rendimientos
    return df_returns, estad

    


