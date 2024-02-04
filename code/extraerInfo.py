archivo_bvh = '../files/test3.bvh'  # Reemplaza con la ruta de tu archivo .bvh

with open(archivo_bvh, 'r') as file:
    lineas = file.readlines()

frames_linea = [linea.strip().split() for linea in lineas if 'Frames:' in linea]
frame_time_linea = [linea.strip().split() for linea in lineas if 'Frame Time:' in linea]

if frames_linea and frame_time_linea:
    frames = int(frames_linea[0][1])
    frame_time = float(frame_time_linea[0][2])
    
    print(f'Frames: {frames}')
    print(f'Frame Time: {frame_time}')
    
    info_bvh = {'Frames': frames, 'Frame Time': frame_time}
    print(info_bvh)
else:
    print('No se encontró la información en el archivo.')
