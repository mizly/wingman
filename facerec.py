import mediapipe as mp
#import face_recognition_models
import face_recognition as fr
import cv2
import numpy as np
import pickle
import os
import cvcont

face_database = {}


def faceRecog(img_frame):
    global face_database

    frame = img_frame

    face_locations = fr.face_locations(frame)
    face_encodings = fr.face_encodings(frame, face_locations)
    try:
        with open("face_encodings.pkl", "rb") as f:
            face_database = pickle.load(f)
    except (FileNotFoundError, EOFError):
        return False

    for coding in face_encodings:
        for name, face in face_database.items():
            match = fr.compare_faces([face],coding)[0]
            if(match):
                #print("I know you!")
                return name

    return False


def addFace(name, img_frame):
    frame = img_frame

    face_locations = fr.face_locations(frame)
    face_encodings = fr.face_encodings(frame, face_locations)

    if(face_encodings):
        new_encoding = face_encodings[0]
        try:
            with open("face_encodings.pkl", "rb") as f:
                face_database = pickle.load(f)
        except (FileNotFoundError, EOFError):
            face_database = {}

        if name in face_database:
            return "Sorry, didn't recognize you! Name already in database"
        face_database[name] = new_encoding
        with open("face_encodings.pkl", "wb") as f:
            pickle.dump(face_database, f)
        return True
    
    return False





