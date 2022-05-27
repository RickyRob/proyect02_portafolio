from modules.utils import *
import scipy.optimize as sco

bienvenida()

n = int(input('Cuantas acciones tendrá tu portafolio: '))

lista = acciones_list(n)
inicio = input('Fecha del periodo inicial (YYYY-MM-DD) : ')
fin = input('Fecha del periodo final (YYYY-MM-DD)  : ')

df = data(lista,inicio,fin)

con_excel(df)

rend, rend_med, desv, medias = returns(df)

print('Varianza Covarianza')
varcov = varcovar(rend_med)
print(varcov)

print('Correlación')
cor = matcor(varcov,desv)
print(cor)

# Esta función solo crea la simulaciones y genera una gráfica
simulaciones(medias, desv, varcov, n)

#Estos son los nuevos pesos aleatorios
pesos = np.random.random(n)
pesos /= np.sum(pesos)
print(pesos)

# Esta función regreso solo el tercer elemento de pstats que el Sharpe 
#op = optimizador(medias, desv, varcov)
print('#################### PSTATS################')
print(pstats(pesos,medias,varcov))

# Creando variables de la funcion optimizadora
cons = ({'type':'eq','fun':lambda x: np.sum(x) - 1})
bnds = tuple((0,1) for x in range(n))

opts = sco.minimize(optimizador(pesos, medias=medias,varcov=varcov), pesos, method = 'SLSQP', bounds = bnds, constraints = cons)

sharpe = pstats(opts['x'])

print(sharpe)

