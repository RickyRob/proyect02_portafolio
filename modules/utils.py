import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import xlwings as xw
from datetime import timedelta
from ortools.linear_solver import pywraplp
import scipy.optimize as sco



# Funcion de bienvenida

def bienvenida():
    print('\n')
    print('####################################################')
    print('################# INVESTING ##################')
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
    sheet_estr1[1,l+2].value = df_returns.describe()
    medias = df_returns.mean(axis=0).tolist() # almacenando las medias en esta variable
    desv = pd.DataFrame(df_returns.std(axis=0)) # almacenando las desviaciones estandar en esta variable
    df_ret_med = df_returns - medias
    return df_returns, df_ret_med, desv, medias

    
def varcovar(df):
    wb = xw.books.active # Trabaja sobre el Libro creado
    wb.sheets.add() # Agrega una hoja nueva al Libro creado y activo
    sheet_estr2 = wb.sheets[0] # Se le asigna la hoja por posición
    sheet_estr2.name = 'Matrices' # Se le asigna nombre a la hoja por posición aqui viviran los resultados de rendimientos
    df_t = df.transpose()
    varcov = df_t.dot(df)
    varcov = varcov/(len(df)-1)
    sheet_estr2.range('A1').value = varcov
    return varcov

def matcor(df,desv):
    wb = xw.books.active # Trabaja sobre el Libro creado
    sheet_estr2 = wb.sheets[0] # Se le asigna la hoja por posición
    cor = df/(desv.dot(desv.transpose()))
    l = len(cor)
    sheet_estr2[0,l+2].value = cor
    return cor

def simulaciones(medias, desv, varcov,n):
    ret_p = []
    vol_p = []
    pesos_p = []

    for i in range(6000):
        pesos = np.random.random(n)
        pesos /= np.sum(pesos)
        ret_p.append(np.sum(medias*pesos)*252)
        vol_p.append(np.sqrt(np.dot(pesos.T,np.dot(varcov*252,pesos))))
        pesos_p.append(np.round(pesos,2))
    
    ret_p = np.array(ret_p)
    vol_p = np.array(vol_p)
    concentrado = np.array([ret_p,vol_p,ret_p/vol_p,pesos_p])
    sim = pd.DataFrame(concentrado).T
    sim.columns = ['Retorno','Volatilidad','Sharpe','Pesos']
    print(sim.head())
    print('######### Esta es tu mejor distribución del portafolio ###########')
    optimo = sim[sim['Sharpe']==sim['Sharpe'].max()]
    print(optimo)
    
    
    plt.figure(figsize=(10,7))
    plt.scatter(vol_p,ret_p, c=ret_p/vol_p, marker='o')
    plt.grid(True)
    plt.title(f'Mejor combinación de pesos: {optimo.iloc[:,3]}')
    plt.xlabel('Volatilidad')
    plt.ylabel('Retornos')
    plt.colorbar(cmap='plasma',label='Sharpe Ratio')
    plt.show()

