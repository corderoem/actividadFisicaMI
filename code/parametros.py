import pandas as pd
import numpy as np
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import mplcursors

#El cleaning funciona para un Rigid Body de 36 marcadores, si se usa mas marcadores modificar variable columnas_innecesarias
def cleaning(df):
    df = df[0].str.split(',', expand=True)

    #Eliminar columnas innecesarias 
    columnas_innecesarias = df.columns[185:]  
    # Eliminar las columnas seleccionadas del DataFrame
    df = df.drop(columns=columnas_innecesarias)

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

    return marcadores

def diccionario_pivotes():
    dicc_pivotes = {'Hip-1': ["RShoulder-1", "RThigh-1"],
                     'Hip-2': ["LShoulder-1", "LThigh-1"],
                     'LThigh-2': ["LShin-2", "LThigh-1"],
                     'RThigh-2': ["RShin-2", "RThigh-1"],
                     'LUArm-1': ["LHand-3", "LShoulder-1"],
                     'RUArm-1': ["RHand-3", "RShoulder-1"]}
    return dicc_pivotes


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

def graficar_parametros(df, tiempo_inicial, tiempo_final, marcador, marcador_pivote, marcador_vector1, marcador_vector2):
    tiempo_inicial_dt = datetime.strptime(tiempo_inicial, '%M:%S:%f')
    tiempo_final_dt = datetime.strptime(tiempo_final, '%M:%S:%f')

    # Obtener datos del marcador en el rango de tiempo
    posiciones_tiempo = []
    posiciones_tiempo_angulos = []

    current_time = tiempo_inicial_dt
    while current_time <= tiempo_final_dt:
        tiempo_str = current_time.strftime('%M:%S:%f')[:-4]
        posicion_tiempo = obtener_datos_marcador_tiempo(df, marcador, tiempo_str)
        posicion_tiempo_angulos = {
            'pivote': obtener_datos_marcador_tiempo(df, marcador_pivote, tiempo_str),
            'vector1': obtener_datos_marcador_tiempo(df, marcador_vector1, tiempo_str),
            'vector2': obtener_datos_marcador_tiempo(df, marcador_vector2, tiempo_str)
        }

        if posicion_tiempo and posicion_tiempo_angulos:
            posiciones_tiempo.append(posicion_tiempo)
            posiciones_tiempo_angulos.append(posicion_tiempo_angulos)
            

        current_time += timedelta(milliseconds=40)

    # Crear listas para almacenar los resultados de la función calcular_parametros
    desplazamientos = []
    velocidades = []
    aceleraciones = []
    angulos = []

    # Calcular desplazamiento, velocidad y aceleración para cada instante de tiempo en el rango
    for i in range(1, len(posiciones_tiempo)):

        desplazamiento, velocidad, aceleracion = calcular_parametros(posiciones_tiempo[0], posiciones_tiempo[i], marcador)
        desplazamientos.append(desplazamiento)
        velocidades.append(velocidad)
        aceleraciones.append(aceleracion)

        angulo = calcular_angulo(
            posiciones_tiempo_angulos[i]['pivote'],
            posiciones_tiempo_angulos[i]['vector1'],
            posiciones_tiempo_angulos[i]['vector2']
        )
        angulos.append(angulo)

    # Crear el tiempo correspondiente a cada instante
    tiempos = [posicion[marcador][3] for posicion in posiciones_tiempo[1:]]  # Utilizar todas las posiciones excepto la primera
    # Crear el tiempo correspondiente a cada instante
    tiempos_angulo = [posicion['pivote'][marcador_pivote][3] for posicion in posiciones_tiempo_angulos[1:]]

    # Crear el gráfico con ejes verticales independientes
    fig, ax1 = plt.subplots(figsize=(4, 3))
    # Ajustar los límites del eje x para acortar el lado derecho
    ax1.set_xlabel('Tiempo (s)', fontsize=8)

    # Graficar desplazamiento y configurar el primer eje
    linea_desplazamiento = ax1.plot(tiempos, desplazamientos, color='blue', label='Desplazamiento')[0]
    ax1.tick_params(axis='both', labelcolor='blue', labelsize=7.5)

    # Crear ejes gemelos para velocidad y aceleración
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    ax4 = ax1.twinx()

    # Mover el eje de aceleración hacia la derecha para evitar superposiciones
    #ax3.spines['right'].set_position(('outward', 30))

    # Graficar velocidad y aceleración en los ejes gemelos
    linea_velocidad = ax2.plot(tiempos, velocidades, color='green', label='Velocidad')[0]
    ax2.tick_params(axis='y', labelcolor='green', labelsize=7.5)

    linea_aceleracion = ax3.plot(tiempos, aceleraciones, color='red', label='Aceleración')[0]
    ax3.tick_params(axis='y', labelcolor='red', labelsize=7.5)

    # Calcular ángulos y configurar el eje para el ángulo
    #tiempos_angulo, angulos = calcular_angulos_en_el_tiempo(df, tiempo_inicial, tiempo_final, marcador_pivote, marcador_vector1, marcador_vector2)
    linea_angulo = ax4.plot(tiempos_angulo, angulos, color='orange', label='Ángulo')[0]
    ax4.tick_params(axis='y', labelcolor='orange', labelsize=7.5)
    #ax4.spines['left'].set_position(('outward', 30))

    # Mover los ejes de velocidad y aceleración hacia la izquierda
    # ax2.spines['left'].set_position(('outward', 30))
    ax3.spines['right'].set_position(('outward', 30))
    ax4.spines['right'].set_position(('outward', 60))



    # Unir todas las líneas en una sola leyenda
    lines = [linea_desplazamiento, linea_velocidad, linea_aceleracion, linea_angulo]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, fontsize=7)

    fig.subplots_adjust(right=0.83,left=0.05)
    mplcursors.cursor(hover=True)


    plt.grid(True)
    return fig

