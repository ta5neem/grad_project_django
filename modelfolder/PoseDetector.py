import math
import cv2
import mediapipe as mp
import numpy as np



class PoseDetector:
    
    mp_hands = None
    mp_drawing = None
    mpPose = None 
    R_sholder = None
    R_hip = None
    R_elbow= None
    L_sholder= None
    L_hip= None
    L_elbow= None
    L_wrist= None
    R_wrist= None
    L_wrist= None
    Nose  = None
    results = None 
    lm =None
    lmPose =None
    
    
    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.detectionCon = detectionCon
        self.trackCon = trackCon
#        
        # تحديد المتغيرات
#         self.R_sholder=0,
#         self.R_hip=self.R_elbow=self.L_sholder=self.L_hip=self.L_elbow=self.L_wrist=self.R_wrist=self.L_wrist=0
    
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose       
#            ////////////////      اعدادات الموديل
#         self.pose = self.mpPose.Pose(min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon,)
        self.hands =self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)        
        self.pose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


#         mp_drawing = mp.solutions.drawing_utils
#         mp_pose = mp.solutions.pose
#         mp_hands = mp.solutions.hands
        
    def find_pose(self, img ,blackie, draw=True):
#         ///// body
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        self.results = self.pose.process(imgRGB)
        self.lm = self.results.pose_landmarks
        self.lmPose  = self.mpPose.PoseLandmark
#         /////// hand
        self.results_hands = self.hands.process(imgRGB)
        

        if self.lm and draw:
            self.draw_landmarks(img ,blackie)
        
        return img,blackie
        
    def draw_landmarks(self, img ,blackie, connections=None):
        self.mp_drawing.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        self.mp_drawing.draw_landmarks(blackie, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        if self.results_hands.multi_hand_landmarks:
            for hand_landmarks in self.results_hands.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                self.mp_drawing.draw_landmarks(blackie, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def Landmark_pos(self ,w ,h ):
        R_sholder_X = int(self.lm.landmark[self.lmPose.RIGHT_SHOULDER ].x*w)
        R_sholder_Y = int(self.lm.landmark[self.lmPose.RIGHT_SHOULDER].y*h)
        self.R_sholder=[R_sholder_X ,R_sholder_Y]

        R_hip_X = int(self.lm.landmark[self.lmPose.RIGHT_HIP ].x*w)
        R_hip_Y = int(self.lm.landmark[self.lmPose.RIGHT_HIP ].y*h)
        self.R_hip=[R_hip_X ,R_hip_Y]

        R_elbow_X = int(self.lm.landmark[self.lmPose.RIGHT_ELBOW ].x*w)
        R_elbow_Y = int(self.lm.landmark[self.lmPose.RIGHT_ELBOW].y*h)
        self.R_elbow=[R_elbow_X ,R_elbow_Y]

        L_sholder_X = int(self.lm.landmark[self.lmPose.LEFT_SHOULDER ].x*w)
        L_sholder_Y = int(self.lm.landmark[self.lmPose.LEFT_SHOULDER].y*h)
        self.L_sholder=[L_sholder_X ,L_sholder_Y]

        L_hip_X = int(self.lm.landmark[self.lmPose.LEFT_HIP ].x*w)
        L_hip_Y = int(self.lm.landmark[self.lmPose.LEFT_HIP ].y*h)
        self.L_hip=[L_hip_X ,L_hip_Y]

        L_elbow_X = int(self.lm.landmark[self.lmPose.LEFT_ELBOW ].x*w)
        L_elbow_Y = int(self.lm.landmark[self.lmPose.LEFT_ELBOW].y*h)
        self.L_elbow=[L_elbow_X ,L_elbow_Y]

        L_wrist_X = int(self.lm.landmark[self.lmPose.LEFT_WRIST ].x*w)
        L_wrist_Y = int(self.lm.landmark[self.lmPose.LEFT_WRIST].y*h)
        self.L_wrist=[L_wrist_X ,L_wrist_Y]

        R_wrist_X = int(self.lm.landmark[self.lmPose.RIGHT_WRIST ].x*w)
        R_wrist_Y = int(self.lm.landmark[self.lmPose.RIGHT_WRIST].y*h)
        self.R_wrist=[R_wrist_X ,R_wrist_Y]

        Nose_X = int(self.lm.landmark[self.lmPose.NOSE ].x*w)
        Nose_Y = int(self.lm.landmark[self.lmPose.NOSE].y*h)
        self.Nose=[Nose_X ,Nose_Y]

    #     L_wrist_X = int(lm.landmark[lmPose.LEFT_WRIST ].x*w)
    #     L_wrist_Y = int(lm.landmark[lmPose.LEFT_WRIST].y*h)
    #     L_wrist=[L_wrist_X ,L_wrist_Y]

#         return R_sholder,R_hip,R_elbow,L_sholder,L_hip,L_elbow,L_wrist,R_wrist,L_wrist,Nose                



#     def Landmark_pos(self,w=480 ,h=640 ):
#         R_sholder_X = int(self.lm.landmark[self.lmPose.RIGHT_SHOULDER ].x*w)
#         R_sholder_Y = int(self.lm.landmark[self.lmPose.RIGHT_SHOULDER].y*h)
#         if  R_sholder_X>h or  R_sholder_Y>w :
#             R_sholder_X=0
#             R_sholder_Y=0
#         self.R_sholder=[R_sholder_X ,R_sholder_Y]

#         R_hip_X = int(self.lm.landmark[self.lmPose.RIGHT_HIP ].x*w) 
#         R_hip_Y = int(self.lm.landmark[self.lmPose.RIGHT_HIP ].y*h)
#         if  R_hip_X>h or  R_hip_Y>w :
#             R_hip_X=0
#             R_hip_Y=0
#         self.R_hip=[R_hip_X ,R_hip_Y]

#         R_elbow_X = int(self.lm.landmark[self.lmPose.RIGHT_ELBOW ].x*w)
#         R_elbow_Y = int(self.lm.landmark[self.lmPose.RIGHT_ELBOW].y*h)
#         if  R_elbow_X>h or  R_elbow_Y>w :
#             R_elbow_X=0
#             R_elbow_Y=0
#         self.R_elbow=[R_elbow_X ,R_elbow_Y]

#         L_sholder_X = int(self.lm.landmark[self.lmPose.LEFT_SHOULDER ].x*w)
#         L_sholder_Y = int(self.lm.landmark[self.lmPose.LEFT_SHOULDER].y*h)
#         if  L_sholder_X>h or  L_sholder_Y>w :
#             L_sholder_X=0
#             L_sholder_Y=0
#         self.L_sholder=[L_sholder_X ,L_sholder_Y]

#         L_hip_X = int(self.lm.landmark[self.lmPose.LEFT_HIP ].x*w)
#         L_hip_Y = int(self.lm.landmark[self.lmPose.LEFT_HIP ].y*h)
#         if  L_hip_X>h or  L_hip_Y>w :
#             L_hip_X=0
#             L_hip_Y=0
#         self.L_hip=[L_hip_X ,L_hip_Y]

#         L_elbow_X = int(self.lm.landmark[self.lmPose.LEFT_ELBOW ].x*w)
#         L_elbow_Y = int(self.lm.landmark[self.lmPose.LEFT_ELBOW].y*h)
#         if  L_elbow_X>h or  L_elbow_Y>w :
#             L_elbow_X=0
#             L_elbow_Y=0
#         self.L_elbow=[L_elbow_X ,L_elbow_Y]

#         L_wrist_X = int(self.lm.landmark[self.lmPose.LEFT_WRIST ].x*w)
#         L_wrist_Y = int(self.lm.landmark[self.lmPose.LEFT_WRIST].y*h)
#         if  L_wrist_X>h or  L_wrist_Y>w :
#             L_wrist_X=0
#             L_wrist_Y=0
#         self.L_wrist=[L_wrist_X ,L_wrist_Y]

#         R_wrist_X = int(self.lm.landmark[self.lmPose.RIGHT_WRIST ].x*w)
#         R_wrist_Y = int(self.lm.landmark[self.lmPose.RIGHT_WRIST].y*h)
#         if  R_wrist_X>h or  R_wrist_Y>w :
#             R_wrist_X=0
#             R_wrist_Y=0
#         self.R_wrist=[R_wrist_X ,R_wrist_Y]
# #         return R_sholder,R_hip,R_elbow,L_sholder,L_hip,L_elbow,L_wrist,R_wrist,L_wrist
    