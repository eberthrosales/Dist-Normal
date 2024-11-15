import numpy as np
import scipy.stats as stats

def calcular_media_y_desviacion(datos):
    """
    Calcula la media y la desviación estándar de un conjunto de datos.
    """
    media = np.mean(datos)
    desviacion_estandar = np.std(datos)
    return media, desviacion_estandar

def generar_datos_normal(media, desviacion_estandar, num_muestras=1000):
    """
    Genera un conjunto de datos con distribución normal.
    """
    return np.random.normal(loc=media, scale=desviacion_estandar, size=num_muestras)

def calcular_funcion_densidad(probabilidades, media, desviacion_estandar):
    """
    Calcula la función de densidad de probabilidad (PDF) de la distribución normal.
    """
    return stats.norm.pdf(probabilidades, loc=media, scale=desviacion_estandar)
