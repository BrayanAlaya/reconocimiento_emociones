# from tensorflow.keras.applications.imagenet_utils import preprocess_input
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model

import tensorflow as tf

import numpy as np
import imutils
import cv2
import time

class EmotionDetector:
    def __init__(self):
        self.classes = ['angry','disgust','fear','happy','neutral','sad','surprise']
        prototxtPath = "services/face_detector/deploy.prototxt"
        weightsPath = "services/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
        emotion_model_path = "services/modelFEC.h5"
        self.time_actualframe = 0
        self.time_prevframe = 0
        self.faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
        self.emotionModel = tf.keras.models.load_model(emotion_model_path)
        self.cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        
        
        
        

    def predict_emotion(self,frame,faceNet,emotionModel):
        # Construye un blob de la imagen
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 177.0, 123.0))

        # Realiza las detecciones de rostros a partir de la imagen
        faceNet.setInput(blob)
        detections = faceNet.forward()

        # Listas para guardar rostros, ubicaciones y predicciones
        faces = []
        locs = []
        preds = []
        
        # Recorre cada una de las detecciones
        for i in range(0, detections.shape[2]):
            
            # Fija un umbral para determinar que la detección es confiable
            # Tomando la probabilidad asociada en la deteccion

            if detections[0, 0, i, 2] > 0.4:
                # Toma el bounding box de la detección escalado
                # de acuerdo a las dimensiones de la imagen
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (Xi, Yi, Xf, Yf) = box.astype("int")

                # Valida las dimensiones del bounding box
                if Xi < 0: Xi = 0
                if Yi < 0: Yi = 0
                
                # Se extrae el rostro y se convierte BGR a GRAY
                # Finalmente se escala a 224x244
                face = frame[Yi:Yf, Xi:Xf]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (48, 48))
                face2 =  tf.keras.utils.img_to_array(face)
                face2 = np.expand_dims(face2,axis=0)

                # Se agrega los rostros y las localizaciones a las listas
                faces.append(face2)
                locs.append((Xi, Yi, Xf, Yf))

                pred = emotionModel.predict(face2)
                preds.append(pred[0])

        return (locs,preds)

    def start_detection(self):
        while True:
            # Se toma un frame de la cámara y se redimensiona
            ret, frame = self.cam.read()
            frame = imutils.resize(frame, width=640)

            if frame is None or frame.size == 0:
                print("Error: frame está vacío o no tiene datos")
                return

            (locs, preds) = self.predict_emotion(frame,self.faceNet,self.emotionModel)
            
            # Para cada hallazgo se dibuja en la imagen el bounding box y la clase
            for (box, pred) in zip(locs, preds):
                
                (Xi, Yi, Xf, Yf) = box
                (angry,disgust,fear,happy,neutral,sad,surprise) = pred


                label = ''
                # Se agrega la probabilidad en el label de la imagen
                label = "{}: {:.0f}%".format(self.classes[np.argmax(pred)], max(angry,disgust,fear,happy,neutral,sad,surprise) * 100)

                cv2.rectangle(frame, (Xi, Yi-40), (Xf, Yi), (255,0,0), -1)
                cv2.putText(frame, label, (Xi+5, Yi-15),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                cv2.rectangle(frame, (Xi, Yi), (Xf, Yf), (255,0,0), 3)


            self.time_actualframe = time.time()

            if self.time_actualframe>self.time_prevframe:
                fps = 1/(self.time_actualframe-self.time_prevframe)
            
            self.time_prevframe = self.time_actualframe

            cv2.putText(frame, str(int(fps))+" FPS", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        self.cam.release()