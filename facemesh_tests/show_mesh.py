import numpy as np 
import cv2 
import mediapipe as mp 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

if __name__ == "__main__": 

    drawing_specs = mp_drawing.DrawingSpec(thickness = 1, circle_radius = 1)
    cap = cv2.VideoCapture(0)

    with mp_face_mesh.FaceMesh(max_num_faces = 1, 
                               refine_landmarks = True, 
                               min_detection_confidence = 0.5, 
                               min_tracking_confidence = 0.5) as face_mesh: 

        while cap.isOpened(): 
            success, image = cap.read()
            if not success: 
                continue 
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image)

            # ===============================================
            # =============== SAVE FACE DATA ================ 
            # recap_landmarks = np.zeros((478,3))
            
            # for i,l in enumerate(results.multi_face_landmarks[0].landmark):
            #     recap_landmarks[i] = [l.x, l.y, l.z]

            # np.savetxt('./face_0.txt', recap_landmarks)

            # ===============================================
            # =============== SAVE CONTOUR DATA =============

            # edges = []
            # for edge_data in mp_face_mesh.FACEMESH_CONTOURS: 
            #     edges.append(list(edge_data))
            
            # np.savetxt('./edges_0.txt', np.array(edges).astype(int))

            # ===============================================
            # =========== SAVE TESSELATION DATA =============            

            # edges_t = []
            # for edge_data in mp_face_mesh.FACEMESH_TESSELATION: 
            #     edges_t.append(list(edge_data))
            
            # np.savetxt('./edges_t_0.txt', np.array(edges_t).astype(int))




            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_face_landmarks: 
                for face_landmarks in results.multi_face_landmarks: 
                    mp_drawing.draw_landmarks(image = image, 
                                              landmark_list = face_landmarks, 
                                              connections = mp_face_mesh.FACEMESH_TESSELATION, 
                                              landmark_drawing_spec = None, 
                                              connection_drawing_spec = mp_drawing_styles.get_default_face_mesh_tesselation_style())

                    mp_drawing.draw_landmarks(
                            image=image,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles
                            .get_default_face_mesh_contours_style())

                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_iris_connections_style())
            cv2.imshow('FaceMesh', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27: 
                break 
        cap.release()
