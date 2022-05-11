from modules.utils import *

bienvenida()

n = int(input('Cuantas acciones tendrá tu portafolio: '))

lista = acciones_list(n)
inicio = input('Fecha del periodo inicial (YYYY-MM-DD) : ')
fin = input('Fecha del periodo final (YYYY-MM-DD)  : ')

df = data(lista,inicio,fin)

con_excel(df)

rend, rend_med, desv = returns(df)

print('Varianza Covarianza')
varcov = varcovar(rend_med)
print(varcov)

print('Correlación')
cor = matcor(varcov,desv)
print(cor)


