import mediapipe as mp
import face_recognition as fr
import cv2
import numpy as np
import pickle
import os
import cvcont

face_database = {}


def faceRecog():
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence = 0.5)
    


    frame = cvcont.get_frame()

    face_locations = fr.face_locations(frame)
    face_encodings = fr.face_encodings(frame, face_locations)
    try:
        with open("face_encodings.pkl", "rb") as f:
            face_database = pickle.load(f)
    except FileNotFoundError:
        face_database = {}

    for coding in face_encodings:
        for name, face in face_database.items():
            match = fr.compare_faces([face],coding)[0]
            if(match):
                print("I know you!")
                return name

    return False


def addFace(name):
    frame = cvcont.get_frame()

    face_locations = fr.face_locations(frame)
    face_encodings = fr.face_encodings(frame, face_locations)

    if(face_encodings):
        new_encoding = face_encodings[0]
        try:
            with open("face_encodings.pkl", "rb") as f:
                face_database = pickle.load(f)
        except FileNotFoundError:
            face_database = {}

        if name in face_database:
            return "Sorry, didn't recognize you! Name already in database"
        face_database[name] = new_encoding
        with open("face_encodings.pkl", "wb") as f:
            pickle.dump(face_database, f)
        return True
    
    return False





