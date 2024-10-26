from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

import numpy as np
import imutils
import cv2
import time

class EmotionDetector:
    def __init__(self, face_model_path, emotion_model_path):
        self.classes = ['enojado', 'asco', 'miedo', 'feliz', 'neutral', 'triste', 'sorprendido']
        prototxtPath, weightsPath = face_model_path
        self.faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
        self.emotionModel = load_model(emotion_model_path)
        self.time_prevframe = 0
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def preprocess_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
        image = cv2.resize(image, (48, 48))  # Redimensionar
        image = img_to_array(image)  # Convertir a array
        image = np.expand_dims(image, axis=0)  # Expandir dimensiones
        image = preprocess_input(image)  # Preprocesar
        return image

    def predict_emotion(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1.0, (400, 400), (104.0, 177.0, 123.0))
        self.faceNet.setInput(blob)
        detections = self.faceNet.forward()

        faces, locs, preds = [], [], []

        for i in range(0, detections.shape[2]):
            if detections[0, 0, i, 2] > 0.4:
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (Xi, Yi, Xf, Yf) = box.astype("int")
                Xi, Yi = max(0, Xi), max(0, Yi)

                face = frame[Yi:Yf, Xi:Xf]
                face = self.preprocess_image(face)  # Preprocesar la imagen

                faces.append(face)
                locs.append((Xi, Yi, Xf, Yf))
                preds.append(self.emotionModel.predict(face)[0])

        return (locs, preds)

    def start_detection(self):
        while True:
            ret, frame = self.cam.read()
            frame = imutils.resize(frame, width=640)
            (locs, preds) = self.predict_emotion(frame)

            for (box, pred) in zip(locs, preds):
                (Xi, Yi, Xf, Yf) = box
                label = "{}: {:.0f}%".format(self.classes[np.argmax(pred)], max(pred) * 100)

                cv2.rectangle(frame, (Xi, Yi-40), (Xf, Yi), (255, 0, 0), -1)
                cv2.putText(frame, label, (Xi + 5, Yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.rectangle(frame, (Xi, Yi), (Xf, Yf), (255, 0, 0), 3)

            time_actualframe = time.time()
            if time_actualframe > self.time_prevframe:
                fps = 1 / (time_actualframe - self.time_prevframe)
            self.time_prevframe = time_actualframe

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        self.cam.release()
