#'../files/testhlt1.bvh'
'''
import bvh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Función para cargar el archivo BVH
def cargar_archivo_bvh(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        mocap = bvh.Bvh(f.read())
    return mocap

# Función para crear un video a partir de los datos de movimiento BVH
def crear_video(mocap, archivo_salida="output_video.mp4"):
    fig, ax = plt.subplots()

    # Variables para el seguimiento del progreso
    progreso = {'frame': 0, 'total_frames': 0}

    # Personaliza esta función según la estructura de tu archivo BVH
    def actualizar(cuadro):
        # Extrae los ángulos de las articulaciones de los datos de movimiento
        angulos_articulaciones = mocap.frames[cuadro]

        # Personaliza esta parte según cómo desees visualizar el movimiento
        # Por ejemplo, podrías aplicar estos ángulos a un modelo de esqueleto 3D
        ax.clear()
        # Dibuja o renderiza el esqueleto basado en angulos_articulaciones

        ax.set_title(f'Cuadro: {cuadro}')

        # Actualiza la variable de progreso
        progreso['frame'] = cuadro + 1
        print(f"Actualizando cuadro {cuadro}...")


    # Establece el número de cuadros según tus datos BVH
    num_cuadros = len(mocap.frames)
    progreso['total_frames'] = num_cuadros

    # Función de actualización de progreso
    def actualizacion_progreso(_):
        porcentaje = (progreso['frame']) / progreso['total_frames'] * 100
        print(f"Progreso: {porcentaje:.2f}% completado", end='\r')

    # Crea la animación
    print("Creando video... Esto puede llevar tiempo.") 
    animacion = FuncAnimation(
        fig, 
        actualizar, 
        frames=range(num_cuadros),  # Utiliza un rango de números como iterador
        repeat=False,
        init_func=lambda: actualizacion_progreso(None),
        interval=100,  # Intervalo de actualización en milisegundos
    )

    # Save animation as a video file
    print(f"Guardando video en '{archivo_salida}'...")
    animacion.save(archivo_salida, writer='pillow', fps=100)

    print("Video creado exitosamente.")

# Ejemplo de uso
ruta_archivo_bvh = '../files/testhlt1.bvh'
datos_movimiento = cargar_archivo_bvh(ruta_archivo_bvh)
crear_video(datos_movimiento)

'''
import bvh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Función para cargar el archivo BVH
def cargar_archivo_bvh(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        mocap = bvh.Bvh(f.read())
    return mocap

# Función para crear un video a partir de los datos de movimiento BVH
def crear_video(mocap, archivo_salida="prueba_video.mp4", limite_cuadros=None):
    fig, ax = plt.subplots()

    # Variables para el seguimiento del progreso
    progreso = {'frame': 0, 'total_frames': 0}

    # Personaliza esta función según la estructura de tu archivo BVH
    def actualizar(cuadro):
        # Extrae los ángulos de las articulaciones de los datos de movimiento
        angulos_articulaciones = mocap.frames[cuadro]

        # Personaliza esta parte según cómo desees visualizar el movimiento
        # Por ejemplo, podrías aplicar estos ángulos a un modelo de esqueleto 3D
        ax.clear()
        # Dibuja o renderiza el esqueleto basado en angulos_articulaciones

        ax.set_title(f'Cuadro: {cuadro}')

        # Actualiza la variable de progreso
        progreso['frame'] = cuadro + 1

    # Establece el número de cuadros según tus datos BVH
    num_cuadros = len(mocap.frames)

    # Limita el número de cuadros si se proporciona un límite
    if limite_cuadros is not None:
        num_cuadros = min(num_cuadros, limite_cuadros)

    progreso['total_frames'] = num_cuadros

    # Función de actualización de progreso
    def actualizacion_progreso(_):
        porcentaje = (progreso['frame']) / progreso['total_frames'] * 100
        print(f"Progreso: {porcentaje:.2f}% completado", end='\r')

    # Crea la animación
    print("Creando video... Esto puede llevar tiempo.") 
    animacion = FuncAnimation(
        fig, 
        actualizar, 
        frames=range(num_cuadros),  # Utiliza un rango de números como iterador
        repeat=False,
        init_func=lambda: actualizacion_progreso(None),
        interval=100,  # Intervalo de actualización en milisegundos
    )

    # Save animation as a video file using FFmpeg writer
    print(f"Guardando video en '{archivo_salida}'...")
    animacion.save(archivo_salida, writer='ffmpeg', fps=100)

    print("Video creado exitosamente.")

# Ejemplo de uso con límite de cuadros (por ejemplo, 100 cuadros)
ruta_archivo_bvh = '../files/testhlt1.bvh'
datos_movimiento = cargar_archivo_bvh(ruta_archivo_bvh)
crear_video(datos_movimiento, limite_cuadros=100)

