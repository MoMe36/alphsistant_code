import numpy as np 
import cv2 
import mediapipe as mp 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

def save_face(data, fname = './face_0.txt'): 
    recap_landmarks = np.zeros((478,3))
    print(len(recap_landmarks))
    for i,l in enumerate(data.landmark):
        recap_landmarks[i] = [l.x, l.y, l.z]

    np.savetxt(fname, recap_landmarks)


if __name__ == "__main__": 

    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        
        img = cv2.flip(img, 1)
        cv2.imshow('my webcam', img)

        with mp_face_mesh.FaceMesh(max_num_faces = 1, 
                               refine_landmarks = True, 
                               min_detection_confidence = 0.5, 
                               min_tracking_confidence = 0.5) as face_mesh: 

            results = face_mesh.process(img)

        if results.multi_face_landmarks: 
            save_face(results.multi_face_landmarks[0])        

        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()



    # cap = cv2.VideoCapture(0)

    # with mp_face_mesh.FaceMesh(max_num_faces = 1, 
    #                            refine_landmarks = True, 
    #                            min_detection_confidence = 0.5, 
    #                            min_tracking_confidence = 0.5) as face_mesh: 

    #     while cap.isOpened(): 
    #         success, image = cap.read()
    #         if not success: 
    #             continue 
    #         # image.flags.writeable = False
            
    #         cv2.imshow('FaceMesh', cv2.flip(image, 1))
    #         # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #         # results = face_mesh.process(image)

            # if results.multi_face_landmarks: 
            #     # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #     print(results.multi_face_landmarks)
