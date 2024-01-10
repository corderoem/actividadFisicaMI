import pandas as pd
import numpy as np
from tkinter import messagebox


def cleaning(df):
    df = df[0].str.split(',', expand=True)

    #Eliminar columnas innecesarias 
    #LA ULTIMA COLUMNA PENSABA QUE DEBIA SER RFoot-2, LLAMADO "NOMBRE_DEL_TAKE-RFoot-2"
    #Ejemplo en este caso la última columna será la llamada "Skeleton10-RFoot-2", PERO NO, DEPENDE DEL CSV

    columnas_a_eliminar = df.columns[185:215]  
    # Eliminar las columnas seleccionadas del DataFrame
    df = df.drop(columns=columnas_a_eliminar)

    columnas_a_eliminar = [0, 3, 4]

    # drop para eliminar las columnas por índice
    df = df.drop(df.columns[columnas_a_eliminar], axis=1)

    # Para eliminar desde la columna 5 hasta la última, saltando cada 5 columnas
    columnas_a_eliminar = list(range(5, len(df.columns), 5))
    df = df.drop(df.columns[columnas_a_eliminar], axis=1)
    return df


def obtener_encabezados(df):
    encabezados =['Frames']

    # Iterar cada 3 columnas desde la columna 4 hasta la última
    for i in range(5, len(df.columns), 4):
        valor_encabezado = df.iloc[5, i]
        encabezados.append(valor_encabezado)

    return encabezados

def obtener_patron(encabezados):
    # Encontrar el primer elemento que sigue a 'Frames'
    patron = None
    for elemento in encabezados:
        if elemento.startswith('Frames'):
            continue
        if 'Marker' in elemento:
            break
        if '-' in elemento:
            patron = elemento.split('-')[0]  # Tomar la parte antes del primer '-', ese sería el patron
    
    return patron

def obtener_marcadores(patron, encabezados):
    marcadores= []
    for elemento in encabezados:
        if patron in elemento:
            marcadores.append(elemento)
        else:
            print("No se pudo generar lista de marcadores.")
    return marcadores


#lista de pivotes
def lista_pivotes(patron, marcadores):
    lista_pivotes = []
    for marca in marcadores:
        if marca == patron + "-Hip-1" or  marca == patron + "-Hip-2" or  marca == patron + "-Hip-3"or  marca == patron + "-Hip-4":
            lista_pivotes.append(marca)
    return lista_pivotes

#lista de vectores 1 para la cadera
def lista_vector1(patron, marcadores):
    lista_vector1 = []
    for marca in marcadores:
        if marca == patron + "-RShoulder-1" or  marca == patron + "-RShoulder-2" or  marca == patron + "-LShoulder-1"or  marca == patron + "-LShoulder-2":
            lista_vector1.append(marca)
    return lista_vector1

#lista de vectores 2 para la cadera
def lista_vector2(patron, marcadores):
    lista_vector2 = []
    for marca in marcadores:
        if marca == patron + "-RThigh-1" or  marca == patron + "-RThigh-2" or  marca == patron + "-LThigh-1"or  marca == patron + "-LThigh-2":
            lista_vector2.append(marca)
    return lista_vector2


#FUNCIONES DEL CALCULO DE PARAMETROS

def tiempo_a_segundos(tiempo):
    partes_tiempo = tiempo.split(':')
    
    # Si no hay partes suficientes, retornar un error o valor predeterminado
    if len(partes_tiempo) != 3:
        return print("Debe ingresar el tiempo en el formato correcto (mm:ss:ms)")
    
    minutos = int(partes_tiempo[0])
    segundos = int(partes_tiempo[1])
    milisegundos = int(partes_tiempo[2])

    # Convertir todo a segundos y sumar
    tiempo_en_segundos = minutos * 60 + segundos + milisegundos / 100

    return tiempo_en_segundos


def obtener_datos_marcador_tiempo(dataframe, nombre_marcador, tiempo):

    tiempo = tiempo_a_segundos(tiempo)
    
    # número de columnas en el DataFrame
    num_columnas = len(dataframe.columns)
    #Se encuentra el indice de la fila del tiempo pasado como parametro
    indice = dataframe[dataframe[2].astype(float) == tiempo].index.tolist()

    if not indice:
        print("No se encontró el tiempo en el DataFrame")
        messagebox.showwarning("Error","El tiempo proporcionado no se encuentra en el video")
        return  None

    indice_tiempo = indice[0]

    # Iterar desde el 5to puesto sobre las columnas de 4 en 4 para obtener los datos de cada marcador
    for i in range(5, num_columnas, 4):
        
        #Filtrar por tiempo
        fila_especifica = dataframe.iloc[indice_tiempo:indice_tiempo+1, :]
        
        # Filtrar el DataFrame por el nombre del marcador
        filtro_marcador = fila_especifica[fila_especifica.iloc[:, i] == nombre_marcador]  # Filtrar por el nombre del marcador
        
        # Verificar si se encontró la fila
        if not filtro_marcador.empty:

            # Obtener los datos del marcador y tiempo especificados
            tiempo_encontrado = tiempo
            posicion_x = dataframe.iloc[indice_tiempo, i-3]
            posicion_y = dataframe.iloc[indice_tiempo, i-2]
            posicion_z = dataframe.iloc[indice_tiempo, i-1]

            # Guardar los datos en un diccionario
            datos_dict = {
                nombre_marcador: [float(posicion_x), float(posicion_y), float(posicion_z), tiempo_encontrado]
            }
            return  datos_dict



def calcular_parametros(posicion_inicial, posicion_final, marcador):
    
    if marcador == "":
        messagebox.showwarning("Error", "Debe seleccionar un marcador")
        return None
    
    
    if posicion_inicial is not None and posicion_final is not None:    
        if marcador in posicion_inicial and marcador in posicion_final:
            inicial = posicion_inicial[marcador]
            final = posicion_final[marcador]

            xi, yi, zi, ti = inicial
            xf, yf, zf, tf = final

            desplazamiento_x = xf - xi
            desplazamiento_y = yf - yi
            desplazamiento_z = zf - zi

            desplazamiento_total = round(((desplazamiento_x)**2 + (desplazamiento_y)**2 + (desplazamiento_z)**2)**0.5, 3)

            tiempo_transcurrido = round(tf - ti, 3)

            if tiempo_transcurrido != 0:
                velocidad = abs(round(desplazamiento_total / tiempo_transcurrido, 3))

                velocidad_inicial = 0  
                aceleracion = round((velocidad - velocidad_inicial) / tiempo_transcurrido, 3)

                return desplazamiento_total, velocidad, aceleracion
            else:
                return desplazamiento_total, float('inf'), float('inf')  
        else:
            print("No se ha encontrado el marcador")
            return None, None, None
    else:
        print("No se han detectado tiempos iniciales o finales válidos", marcador)
        messagebox.showwarning("Error", "No se han detectado tiempos iniciales o finales")

        return None, None, None

    

def calcular_angulo(diccionario_pivote, diccionario_vector1, diccionario_vector2):
    
    # Obtener los valores de las posiciones
    pivote = np.array(list(diccionario_pivote.values())).flatten()
    vector1 = np.array(list(diccionario_vector1.values())).flatten()
    vector2 = np.array(list(diccionario_vector2.values())).flatten()
    # Calcular los vectores
    vector_a = vector1 - pivote
    vector_b = vector2 - pivote
    # Calcular el ángulo entre los vectores
    producto_punto = np.dot(vector_a, vector_b)
    magnitud_a = np.linalg.norm(vector_a)
    magnitud_b = np.linalg.norm(vector_b)
    
    cos_theta = producto_punto / (magnitud_a * magnitud_b)
    angulo_radianes = np.arccos(cos_theta)
    angulo_grados = np.degrees(angulo_radianes)
    
    return angulo_grados

# #Calculo de errores


def error_desplazamiento(x1, y1, z1, x2, y2, z2, delta_x1, delta_y1, delta_z1, delta_x2, delta_y2, delta_z2):
    
    a = (x2-x1)**2
    b = (y2-y1)**2
    c = (z2-z1)**2
    
    delta_x = delta_x2**2 + delta_x1**2
    delta_y = delta_y2**2 + delta_y1**2
    delta_z = delta_z2**2 + delta_z1**2

    m = a + b + c
    
    expresion = a * delta_x + b * delta_y + c * delta_z
    
    error_desplazamiento = ((1/m) * expresion)**0.5
    
    return error_desplazamiento



def error_velocidad(desplazamiento, tiempo_inicial, tiempo_final, delta_desplazamiento):
    delta_tiempo = 0.01 # error del Motive
    tiempo = tiempo_a_segundos(tiempo_final) - tiempo_a_segundos(tiempo_inicial)
    
    error = ((delta_desplazamiento)**2/(tiempo)**2 + (desplazamiento)**2 * (delta_tiempo)**2/(tiempo)**4 )**0.5
    
    return error



def error_aceleracion(velocidad, tiempo_inicial, tiempo_final, delta_velocidad):
    delta_tiempo = 0.01 # error del Motive
    tiempo = tiempo_a_segundos(tiempo_final) - tiempo_a_segundos(tiempo_inicial)
    
    error = ((delta_velocidad)**2/(tiempo)**2 + (velocidad)**2 * (delta_tiempo)**2/(tiempo)**4 )**0.5
    
    return error
 

def obtener_vector(diccionario):
    # Quitar el último elemento de cada lista del diccionario (eliminar el tiempo)
    dic = diccionario.copy()
    for key, value in dic.items():
        dic[key] = value[:-1]
            
    # Obtener vector
    vector = np.array(list(dic.values())).flatten()

    return vector


def error_vector(delta_x1, delta_x2,delta_y1,delta_y2,delta_z1,delta_z2):
    error = ((delta_x1)**2 + (delta_x2)**2+ (delta_y1)**2+ (delta_y2)**2+ (delta_z1)**2+ (delta_z2)**2)**0.5
    return error



def error_productopunto(x1, y1, z1, x2, y2, z2, delta_x1, delta_y1, delta_z1, delta_x2, delta_y2, delta_z2):
    error = ((x2*delta_x1)**2 + (x1*delta_x2)**2 + (y2*delta_y1)**2 + (y1*delta_y2)**2 + 
             (z2*delta_z1)**2 + (z1*delta_z2)**2)**0.5
    return error



def error_magnitud(vector,delta_vx, delta_vy, delta_vz):
    a = vector[0]
    b = vector[1]
    c = vector[2]
    
    expres1 = (a**2 + b**2 + c**2)
    
    expres2 = a**2 * delta_vx**2 + b**2 * delta_vy**2 + c**2 * delta_vz**2
    
    error_mag = (expres2/expres1)**0.5
    
    return error_mag


def error_angulo(vector1,vector2, delta_punto, delta_mag1, delta_mag2):
    punto = vector1[0] * vector2[0] + vector1[1] * vector2[1] + vector1[2] * vector2[2]
    magnitud_v1 = ( vector1[0]**2 + vector1[1]**2 + vector1[2]**2 )**0.5
    magnitud_v2 = ( vector2[0]**2 + vector2[1]**2 + vector2[2]**2 )**0.5

    
    error_angulo = ((delta_punto**2 + (punto)**2 * (delta_mag1)**2 / magnitud_v1**2 
                     + (punto)**2 * (delta_mag2)**2 / magnitud_v2**2))**0.5
    
    return error_angulo
