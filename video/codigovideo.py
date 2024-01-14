import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import pandas as pd
import os

# Adds Mediapipe posture drawing to an image
def add_frame(img, frame):
    landmarks_from_frame = frame.iloc[1:200]
    landmark_list = landmark_pb2.NormalizedLandmarkList()

    for i in range(0,len(landmarks_from_frame),3):
        landmark = landmark_list.landmark.add()
        landmark.x = landmarks_from_frame[i]
        landmark.y = landmarks_from_frame[i+1]
        landmark.z = landmarks_from_frame[i+2]
        
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    mp_drawing.draw_landmarks(img, landmark_list, mp_pose.POSE_CONNECTIONS)


# data: matriz con todas las coordenadas de todos los videos
# videoId: ID del video que se quiere renderizar
# fps: frames por segundo
# predictions: si se quiere añadir texto en el frame sobre la predicción hecha por el modelo
def render_video(data, filename, fps=5, predictions=None):
    XMAX = 1500
    YMAX = 1000
    frames = data

    out = cv2.VideoWriter(filename+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), fps, (XMAX,YMAX))
    for index, frame in frames.iterrows():
        img = np.zeros((YMAX,XMAX,3), np.uint8)

        font = cv2.FONT_HERSHEY_SIMPLEX

        text = 'video: '+ filename +' numero de frame: '+str(index+1)
        cv2.putText(img, text,(30,100), font, 1,(255,255,255,255),4,cv2.LINE_AA)

        add_frame(img, frame)

        out.write(img)

    return out
    
    
# Ejemplo de como llamamos a esa función

if __name__ == '__main__':

    #files = os.listdir("./Gestos_4_49/Girando")
    import os

    # Obtener la ruta completa al archivo ejemplo.csv en el directorio actual
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "pruebahalterofilia.csv")

    # Leer el archivo CSV
    filt_df = pd.read_csv(file_path)

    video = render_video(filt_df, "prueba", 10)
    video.release()

