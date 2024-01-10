import pandas as pd
import numpy as np
from pykrige.ok3d import OrdinaryKriging3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

file_path = 'data/datos-errores.xlsx' 
df = pd.read_excel(file_path)

data = df[['x', 'y', 'z', 'errorTotal', 'errorX', 'errorY', 'errorZ']].values

# Función para crear un modelo de Kriging 3D
def crear_modelo_kriging(coord_x, coord_y, coord_z, error):
    return OrdinaryKriging3D(
        coord_x, coord_y, coord_z,
        error,
        variogram_model='spherical',
        verbose=False
    )

# Crear modelos de Kriging para cada eje
modelo_krigingX = crear_modelo_kriging(data[:, 0], data[:, 1], data[:, 2], data[:, 4])
modelo_krigingY = crear_modelo_kriging(data[:, 0], data[:, 1], data[:, 2], data[:, 5])
modelo_krigingZ = crear_modelo_kriging(data[:, 0], data[:, 1], data[:, 2], data[:, 6])
modelo_krigingTotal = crear_modelo_kriging(data[:, 0], data[:, 1], data[:, 2], data[:, 3])

# new_x = float(input("Ingrese la coordenada x: "))
# new_y = float(input("Ingrese la coordenada y: "))
# new_z = float(input("Ingrese la coordenada z: "))

def calcular_error(new_x,new_y,new_z):
    # Predicciones de errores en cada eje utilizando Kriging
    errorX_interpolado, _ = modelo_krigingX.execute('grid', [new_x], [new_y], [new_z])
    errorY_interpolado, _ = modelo_krigingY.execute('grid', [new_x], [new_y], [new_z])
    errorZ_interpolado, _ = modelo_krigingZ.execute('grid', [new_x], [new_y], [new_z])
    errorTotal_interpolado, _ = modelo_krigingTotal.execute('grid', [new_x], [new_y], [new_z])

    return errorX_interpolado, errorY_interpolado, errorZ_interpolado,errorTotal_interpolado 


'''
data = df[['x', 'y', 'z', 'error']].values

#Crear un modelo de Kriging 3D
ok3d = OrdinaryKriging3D(
    data[:, 0],  # x
    data[:, 1],  # y
    data[:, 2],  # z
    data[:, 3],  # error
    variogram_model='spherical',
    verbose=False
)

# Pedir al usuario que ingrese las coordenadas
new_x = float(input("Ingrese la coordenada x: "))
new_y = float(input("Ingrese la coordenada y: "))
new_z = float(input("Ingrese la coordenada z: "))

#print(data)

prediction, variance = ok3d.execute('grid', [new_x], [new_y], [new_z])

#print(ok3d.variogram_model_parameters)
#print(ok3d.variogram_function)

print(f"Valor de predicción en ({new_x}, {new_y}, {new_z}): {prediction[0][0]}")
print(f"Incertidumbre en la predicción: {variance[0][0]}")
'''