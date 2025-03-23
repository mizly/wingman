import cv2

cap = None

def start_camera():
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)

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
