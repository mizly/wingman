import cv2
import mediapipe as mp
import time

cap = None

def start_camera(face_detected):
    global cap
    if cap is None or not cap.isOpened():
        print("we are here!")
        cap = cv2.VideoCapture(0)
        while True:
            mp_face_detection = mp.solutions.face_detection
            mp_drawing = mp.solutions.drawing_utils
            face_detection = mp_face_detection.FaceDetection(min_detection_confidence = 0.5)

            face_detected = False
            detected_time = 0
            max_time = 5
            
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    break
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                results = face_detection.process(image_rgb)

                if results.detections:
                    if not face_detected:
                        face_detected = True
                        detected_time = time.time()

                    elif time.time() - detected_time > max_time:
                        detected_time = time.time()
                        #return True
                    
                else:
                    if face_detected:
                        face_detected = False
                    #return False

def get_frame():
    global cap
    if cap is not None and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            return frame
    return None

def close_camera():
    global cap
    if cap is not None and cap.isOpened():
        cap.release()
        cv2.destroyAllWindows()
        cap = None

