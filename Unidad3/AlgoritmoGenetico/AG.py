from datetime import datetime
import random
import numpy as np
import pandas as pd
import operator

# Clase que representa un municipio
"""
    Representa un municipio con sus coordenadas geográficas.
    
    Atributos:
        x: Coordenada X latitud del municipio.
        y: Coordenada Y longitud del municipio.
        nombre: Nombre del municipio.
"""
class municipio:
 def __init__(self, x, y, nombre):
  self.x = x
  self.y = y
  self.nombre = nombre
 
 #cálculo de la distancia relativa entre dos municipios 
 def distancia(self, municipio):
  xDis = abs(self.x - municipio.x)
  yDis = abs(self.y - municipio.y)
  distancia = np.sqrt((xDis ** 2) + (yDis ** 2))
  return distancia

 #devuelve un listado con las coordenadas de los lugares 
 """   
        retorna: Una cadena que contiene el nombre del municipio.
"""
 def __repr__(self):
  return "(" + str(self.nombre) + ")"


# Clase que representa la aptitud (fitness) de una ruta
"""
    Calcula la distancia total de una ruta y su valor de aptitud.
    Atributos:
        ruta: Una lista de objetos 'municipio' que define el orden del recorrido.
        distancia: Distancia total calculada de la ruta (se inicializa a 0).
        f_aptitud: Valor de aptitud de la ruta (se inicializa a 0.0).
"""
class Aptitud:
 def __init__(self, ruta):
  self.ruta = ruta
  self.distancia = 0
  self.f_aptitud= 0.0


 # Calcula la distancia total de la ruta
 """
        Calcula la distancia total del recorrido, incluyendo el regreso al inicio.
        Si la distancia ya fue calculada, retorna el valor almacenado.
        retorna: La distancia total de la ruta.
        """
 def distanciaRuta(self):
  if self.distancia ==0:
   distanciaRelativa = 0
   for i in range(0, len(self.ruta)):
    puntoInicial = self.ruta[i]
    puntoFinal = None
    if i + 1 < len(self.ruta):
     puntoFinal = self.ruta[i + 1]
    else:
     puntoFinal = self.ruta[0]
    distanciaRelativa += puntoInicial.distancia(puntoFinal)
   self.distancia = distanciaRelativa
  return self.distancia
 

 # Calcula la aptitud de la ruta
 """
    Calcula el valor de aptitud de la ruta (inverso de la distancia).
    Retorna: El valor de aptitud de la ruta (flotante).
 """
 def rutaApta(self):
  if self.f_aptitud == 0:
   self.f_aptitud = 1 / float(self.distanciaRuta())
  return self.f_aptitud
 

# Crea una ruta aleatoria
"""
    Genera una permutación aleatoria de la lista de municipios.

    Argumentos: listaMunicipios: Lista de todos los municipios disponibles.
    Retorna: Una lista de municipio que representa una ruta aleatoria.
    """
def crearRuta(listaMunicipios):
 route = random.sample(listaMunicipios, len(listaMunicipios))
 print(route)
 return route

# Crea la poblacion inicial con un numero determinado de rutas
"""
    Genera la primera población de rutas de forma aleatoria.  
    Argumentos:
        tamanoPob: Número de rutas que debe contener la población inicial.
        listaMunicipios: Lista de todos los municipios disponibles.
    Retorna: Una lista de rutas (listas de 'municipio') que forman la población inicial.
    """
def poblacionInicial(tamanoPob,listaMunicipios):
 poblacion = []

 for i in range(0, tamanoPob):
  poblacion.append(crearRuta(listaMunicipios))
 return poblacion

#Ordena los resultados de la poblacion con base en la distancia de la ruta

def clasificacionRutas(poblacion):
 fitnessResults = {}
 for i in range(0,len(poblacion)):
  fitnessResults[i] = Aptitud(poblacion[i]).rutaApta()
 return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

#Selecciona las mejores rutas para la siguiente generación
"""
    Selecciona rutas para el apareamiento utilizando el método de ruleta.
    Argumentos:
        popRanked: Resultados de la clasificación de rutas ordenadas por aptitud. 
        indivSelecionados: Número de rutas que se seleccionan directamente para el apareamiento.
    Retorna:
        Una lista de índices de las rutas seleccionadas para el apareamiento.
    """
def seleccionRutas(popRanked, indivSelecionados):
 resultadosSeleccion = []
 df = pd.DataFrame(np.array(popRanked), columns=["Indice","Aptitud"])
 df['cum_sum'] = df.Aptitud.cumsum()
 df['cum_perc'] = 100*df.cum_sum/df.Aptitud.sum()
 
 for i in range(0, indivSelecionados):
  resultadosSeleccion.append(popRanked[i][0])
 for i in range(0, len(popRanked) - indivSelecionados):
  seleccion = 100*random.random()
  for i in range(0, len(popRanked)):
   if seleccion <= df.iat[i,3]:
    resultadosSeleccion.append(popRanked[i][0])
    break
 return resultadosSeleccion

#Crea el grupo de apareamiento con base en los resultados de la selección
"""
    Obtiene las rutas seleccionadas de la población original para formar el grupo de apareamiento.

    Argumentos:
        poblacion: La población actual de rutas.
        resultadosSeleccion: Lista de índices de las rutas seleccionadas.

    Retorna: la lista de rutas (municipios) que serán los progenitores.
    """
def grupoApareamiento(poblacion, resultadosSeleccion):
 grupoApareamiento = []
 for i in range(0, len(resultadosSeleccion)):
  index = resultadosSeleccion[i]
  grupoApareamiento.append(poblacion[index])
 return grupoApareamiento

#de los individuos seleccionados, crea los hijos mediante la reproducción
"""
    la funcion reproduccion crea un hijo a partir de dos progenitores utilizando el cruce de segmentos.
    Argumentos:
        progenitor1: Primer progenitor (ruta).
        progenitor2: Segundo progenitor (ruta).
    Retorna: Una nueva ruta generada a partir de los progenitores.
    """
def reproduccion(progenitor1, progenitor2):
 hijo = []
 hijoP1 = []
 hijoP2 = []
 
 generacionX = int(random.random() * len(progenitor1))
 generacionY = int(random.random() * len(progenitor2))
 
 generacionInicial = min( generacionX,  generacionY)
 generacionFinal = max( generacionX, generacionY)

 for i in range( generacionInicial, generacionFinal):
  hijoP1.append(progenitor1[i])
  
 hijoP2 = [item for item in progenitor2 if item not in hijoP1]

 hijo = hijoP1 + hijoP2
 return hijo



"""
    la funcion reproduccionPoblacion crea una nueva población mediante la reproducción de los mejores individuos seleccionados.
    Argumentos:
        grupoApareamiento: El grupo de rutas seleccionadas para el apareamiento.
        indivSelecionados: El número de individuos seleccionados para la reproducción.
    Retorna: Una nueva población generada a partir de los individuos seleccionados.
"""
def reproduccionPoblacion(grupoApareamiento, indivSelecionados):
 hijos = []
 tamano = len(grupoApareamiento) - indivSelecionados
 espacio = random.sample(grupoApareamiento, len(grupoApareamiento))

 for i in range(0,indivSelecionados):
  hijos.append(grupoApareamiento[i])
 
 for i in range(0, tamano):
  hijo = reproduccion(espacio[i], espacio[len(grupoApareamiento)-i-1])
  hijos.append(hijo)
 return hijos

#cambia los lugares para buscar nuevas rutas que puedan ser mejores

"""
    la funcion mutuacion aplica la mutación a un individuo intercambiando dos municipios con una cierta probabilidad

    Argumentos:
        individuo: El individuo al que se le aplicará la mutación.
        razonMutacion: La probabilidad de que ocurra una mutación en un gen (municipio).

    Retorna: El individuo mutado.
"""

def mutacion(individuo, razonMutacion):
 for swapped in range(len(individuo)):
  if(random.random() < razonMutacion):
   swapWith = int(random.random() * len(individuo))
   
   lugar1 = individuo[swapped]
   lugar2 = individuo[swapWith]
   
   individuo[swapped] = lugar2
   individuo[swapWith] = lugar1
 return individuo


"""
la funcion mutacionPoblacion Aplica la mutación a toda la población de individuos.

    Argumentos:
        poblacion: La población de individuos a mutar.
        razonMutacion: La probabilidad de que ocurra una mutación en un gen (municipio).

    Retorna: La población mutada.
"""
def mutacionPoblacion(poblacion, razonMutacion):
 pobMutada = []
 
 for ind in range(0, len(poblacion)):
  individuoMutar = mutacion(poblacion[ind], razonMutacion)
  pobMutada.append(individuoMutar)
 return pobMutada


# Crea una nueva generación

""" 
   La función nuevaGeneracion genera una nueva generación de rutas a partir de la generación actual.
    Argumentos:
        generacionActual: La población actual de rutas.
        indivSelecionados: Número de rutas seleccionadas para el apareamiento.
        razonMutacion: Probabilidad de mutación para cada gen (municipio).
    Retorna: La nueva generación de rutas.  
"""
def nuevaGeneracion(generacionActual, indivSelecionados, razonMutacion):

 #clasificar rutas 
 popRanked = clasificacionRutas(generacionActual)

 #seleccion de los candidatos
 selectionResults = seleccionRutas(popRanked, indivSelecionados)

 #generar grupo de apareamiento
 grupoApa = grupoApareamiento(generacionActual, selectionResults)

 #generacion de la poblacion cruzada, reproducida
 hijos = reproduccionPoblacion(grupoApa, indivSelecionados)

 #incluir las mutaciones en la nueva generación 
 nuevaGeneracion = mutacionPoblacion(hijos, razonMutacion)

 return nuevaGeneracion


# Función principal del algoritmo genético

"""
    la función algoritmoGenetico ejecuta el algoritmo genético para optimizar la ruta entre municipios.  
    Argumentos: 
        poblacion: Lista de municipios disponibles.
        tamanoPoblacion: Tamaño de la población inicial.  
        indivSelecionados: Número de individuos seleccionados para el apareamiento.
        razonMutacion: Probabilidad de mutación para cada gen (municipio).  
        generaciones: Número de generaciones a evolucionar. 
    Retorna: La mejor ruta encontrada después de todas las generaciones.
"""
def algoritmoGenetico(poblacion, tamanoPoblacion, indivSelecionados, razonMutacion, generaciones):
 pop = poblacionInicial(tamanoPoblacion, poblacion)
 print("Distancia Inicial (promedio): " + str(1 / clasificacionRutas(pop)[0][1]))
 
 for i in range(0, generaciones):
  pop = nuevaGeneracion(pop, indivSelecionados, razonMutacion)
 
 print("Distancia Final: " + str(1 / clasificacionRutas(pop)[0][1]))
 bestRouteIndex = clasificacionRutas (pop)[0][0]
 mejorRuta = pop[bestRouteIndex]
 return mejorRuta


if __name__ == '__main__':
    inicio = datetime.now()
    # Lista de municipios con sus coordenadas y nombre del municipio
    lista_municipios = [
        municipio(x=25.4700301, y=-108.5939634, nombre="Ahome"),
        municipio(x=25.2151696, y=-108.0934159, nombre="Angostura"),
        municipio(x=25.2145546, y=-107.3303666, nombre="Badiraguato"),
        municipio(x=23.1715452, y=-106.0406999, nombre="Concordia"),
        municipio(x=24.2440845, y=-106.4129525, nombre="Cosalá"),
        municipio(x=24.4831709, y=-107.2337522, nombre="Culiacán"),
        municipio(x=26.4225239, y=-108.1920467, nombre="Choix"),
        municipio(x=23.5455454, y=-106.5333762, nombre=" Elota"),
        municipio(x=22.5006185, y=-105.4640353, nombre="Escuinapa"), 
        municipio(x=26.2517756, y=-108.3711879, nombre="El fuerte"), 
        municipio(x=25.3355970, y=-108.2818543, nombre="Guasave"), 
        municipio(x=23.1201137, y=-106.2519997, nombre="Mazatlán"), 
        municipio(x=25.2854757, y=-107.5517622, nombre="Mocorito"), 
        municipio(x=22.5927147, y=-105.5113524, nombre="Rosario"), 
        municipio(x=25.2725200, y=-108.0450520, nombre="Salvador Alvarado"), 
        municipio(x=23.5624993, y=-106.2531789, nombre="San Ignacio"), 
        municipio(x=25.4920540, y=-108.1319365, nombre="Sinaloa"), 
        municipio(x=24.4601988, y=-107.4148337, nombre="Navolato") 
    ]
    # Ejecución del algoritmo genético
    mejor_ruta = algoritmoGenetico(poblacion=lista_municipios, 
        tamanoPoblacion=100, 
        indivSelecionados=20,
        razonMutacion=0.01, 
        generaciones=500)

    print("Mejor ruta encontrada:")
    print(mejor_ruta)
    fin = datetime.now()
    print("Duración del proceso: " + str(fin - inicio))

