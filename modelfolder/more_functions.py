import PoseDetector 
import motion
import math
import cv2
import mediapipe as mp
import numpy as np
from experta import *
from enum import Enum
import mysql.connector
import pymssql
from sqlalchemy import create_engine

class more_functions : 

    def draw_img(self,image,text,position):
        cv2.putText(image,text,(position[0],position[1]),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
        return image


    # حساب الزوايا
    def angle_between_points(self ,p1, p2, p3):
        # calculate vectors
        v1 = (p1[0] - p2[0] , p1[1] - p2[1])
        v2 = (p3[0] - p2[0] , p3[1] - p2[1] )
        # calculate angle between vectors
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        mag_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
        mag_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)
        try:
            cos_angle = dot_product / (mag_v1 * mag_v2)
            rad_angle = math.acos(cos_angle)
        except:
            rad_angle=0
        # convert to degrees
        deg_angle = math.degrees(rad_angle)
        return deg_angle



    # معرفة اتجاه الدوران 
    # def turnR_L(self ,img,L_sholder,R_sholder,R_hip):
        
    #     direct = None
    #     ang=self.angle_between_points(L_sholder,R_sholder,R_hip)
    #     cv2.putText(img,str(ang),(50,50),cv2.FONT_HERSHEY_PLAIN,2,(204,0,102),2)
    #     if ang < 77 :
    #         direct = motion.direction.right    
    #     elif ang > 91 :
    #         direct = motion.direction.left
    #     else :
    #         direct=motion.direction.straight
    #     return direct
        
        
    # def calculate_hand_strike_zone(self ,img,x_R, y_R,x_L,y_L,strike_zone_x, strike_zone_y):

    #     # Check if the hand movement is within the strike zone
    #     if strike_zone_x[0] <= x_R <= strike_zone_x[1] and \
    #     strike_zone_y[0] <= y_R <= strike_zone_y[1]and \
    #     strike_zone_x[0] <= x_L <= strike_zone_x[1] and \
    #     strike_zone_y[0] <= y_L <= strike_zone_y[1]: 
    #         return cv2.putText(img,"you are in the zone",(400,450),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
    #     else:
    #         return cv2.putText(img,"you are not in the zone",(400,450),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
        

    # def strike_zone(self ,imgRGB,L_sholder,R_sholder,R_wrist,L_wrist):
        
    #     dist = math.sqrt((L_sholder[0] - R_sholder[0]) ** 2 + (L_sholder[1] - R_sholder[1])**  2)
    #     dist1=dist * (1/3)
    #     dist2=dist * (1/4)

    #     p0=int(R_sholder[0]-dist1)
    #     p1=int(R_sholder[1]+dist2)
    #     p2=int(L_sholder[0]+dist1)
    #     p3=int(R_sholder[1]+dist*1.3)
        
    #     cv2.putText(imgRGB,"*",(p0,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
    #     cv2.putText(imgRGB,"*",(p2,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
    #     cv2.putText(imgRGB,"*",(p0,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
    #     cv2.putText(imgRGB,"*",(p2,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
        
    #     return self.calculate_hand_strike_zone(imgRGB,R_wrist[0],R_wrist[1],L_wrist[0],L_wrist[1] ,(p0,p2),(p1,p3))   


    def turnR_L(self,img,L_sholder,R_sholder,R_hip):
        
        ang=self.angle_between_points(L_sholder,R_sholder,R_hip)
        cv2.putText(img,str(ang),(50,50),cv2.FONT_HERSHEY_PLAIN,2,(204,0,102),2)
        if ang < 77 :
            cv2.putText(img,"you turn right",(50,450),cv2.FONT_HERSHEY_PLAIN,2,(204,0,102),2)
            
            return 1
        elif ang > 91 :   
            cv2.putText(img,"you turn left",(50,450),cv2.FONT_HERSHEY_PLAIN,2,(204,0,102),2)
            return 2
        else :
            cv2.putText(img,"you are straight",(50,450),cv2.FONT_HERSHEY_PLAIN,2,(204,0,102),2)
            return 0

   
    def calculate_hand_strike_zone(self,img,x_R, y_R,x_L,y_L,strike_zone_x, strike_zone_y):
        """
        Calculates if hand movements are within the defined strike zone.

        Args:
            x (float): X-coordinate of hand movement.
            y (float): Y-coordinate of hand movement.
            z (float): Z-coordinate of hand movement.
            strike_zone_x (tuple): Tuple of minimum and maximum values for x-coordinate of the strike zone.
            strike_zone_y (tuple): Tuple of minimum and maximum values for y-coordinate of the strike zone.
            strike_zone_z (tuple): Tuple of minimum and maximum values for z-coordinate of the strike zone.

        Returns:
            bool: True if hand movement is within the strike zone, False otherwise.
        """
        # Check if the hand movement is within the strike zone
        if strike_zone_x[0] <= x_R <= strike_zone_x[1] and \
        strike_zone_y[0] <= y_R <= strike_zone_y[1]and \
        strike_zone_x[0] <= x_L <= strike_zone_x[1] and \
        strike_zone_y[0] <= y_L <= strike_zone_y[1]: 
            return cv2.putText(img,"you are in the zone",(400,450),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
        else:
            return cv2.putText(img,"you are not in the zone",(400,450),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
    

    def strike_zone(self,imgRGB,L_sholder,R_sholder,R_wrist,L_wrist,x):
        
        dist = math.sqrt((L_sholder[0] - R_sholder[0]) ** 2 + (L_sholder[1] - R_sholder[1]) ** 2)
        dist1=dist * (1/3)
        dist2=dist * (1/4)

        
        if x==0:

        
            p0=int(R_sholder[0]-dist1)
            p1=int(R_sholder[1]+dist2)
            p2=int(L_sholder[0]+dist1)
            p3=int(R_sholder[1]+dist*1.3)
            
            
            cv2.putText(imgRGB,"*",(p0,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p0,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            
            return self.calculate_hand_strike_zone(imgRGB,R_wrist[0],R_wrist[1],L_wrist[0],L_wrist[1] ,(p0,p2),(p1,p3))


        elif x==1:
            
            p0=int(R_sholder[0])
            p1=int(R_sholder[1]+dist2)
            p2=int(L_sholder[0]+1.5*dist)
            p3=int(R_sholder[1]+dist*1.8)

            
            cv2.putText(imgRGB,"*",(p0,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p0,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            
            return self.calculate_hand_strike_zone(imgRGB,R_wrist[0],R_wrist[1],L_wrist[0],L_wrist[1] ,(p0,p2),(p1,p3))
            
            
        elif x==2:
            
            p0=int(R_sholder[0]-(1.5*dist))
            p1=int(R_sholder[1]+dist2)
            p2=int(L_sholder[0])
            p3=int(R_sholder[1]+dist*1.8)

            
            cv2.putText(imgRGB,"*",(p0,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p1),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p0,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            cv2.putText(imgRGB,"*",(p2,p3),cv2.FONT_HERSHEY_PLAIN,2,(51,255,255),4)
            
            return self.calculate_hand_strike_zone(imgRGB,R_wrist[0],R_wrist[1],L_wrist[0],L_wrist[1] ,(p0,p2),(p1,p3))



    def destances(self , detector) : 
                    diatance_sholders = math.dist(detector.R_sholder, detector.L_sholder)
                    diatance_wrist = math.dist(detector.R_wrist, detector.L_wrist)
                    
                    distance_RSH_LW =math.dist(detector.R_wrist, detector.L_sholder)
                    distance_LSH_RW =math.dist(detector.L_wrist, detector.R_sholder)
                    
                    distance_REL_LW =math.dist(detector.L_wrist, detector.R_elbow)
                    distance_LEL_RW =math.dist(detector.R_wrist, detector.L_elbow)
                    
                    distance_LEL_LW =math.dist(detector.L_wrist, detector.L_elbow)
                    distance_REL_RW =math.dist(detector.R_wrist, detector.R_elbow)

                    distance_RSH_RW =math.dist(detector.R_wrist, detector.R_sholder)
                    distance_LSH_LW =math.dist(detector.L_wrist, detector.L_sholder)

                    distance_nose_RW =math.dist(detector.R_wrist, detector.Nose)
                    distance_nose_LW =math.dist(detector.L_wrist, detector.Nose)
                    
                    distance_RSH_Nose =math.dist(detector.R_sholder, detector.Nose)
                    distance_LSH_Nose =math.dist(detector.L_sholder, detector.Nose)
                    
                    return diatance_sholders,diatance_wrist,distance_RSH_LW,distance_LSH_RW,distance_REL_LW,distance_LEL_RW  
                    return  distance_LEL_LW,distance_REL_RW,distance_RSH_RW,distance_LSH_LW,distance_nose_RW,distance_nose_LW 
                    return distance_RSH_Nose ,distance_LSH_Nose

    def general_motion_in_secound(self,motion_array):
        counts = {}
        for elem in motion_array:
            if elem in counts:
                counts[elem] += 1
            else:
                counts[elem] = 1        
        # for key, value in counts.items():
        #     if value > 1:
        #         print(f"{key} appears {value} times in the array.")
        max_key = max(counts, key=counts.get)
        return max_key



    def motions_evaluations (self , motion_array):
        counts = {}
        log_counts = {}
        for elem in motion_array:
            if elem in counts:
                counts[elem] += 1
            else:
                counts[elem] = 1
        
        for key, value in counts.items():
            # if value > 1:
            #     print(f"{key} appears {value} times in the array.")
            log_counts[key] = math.log(value*10)

        return log_counts   
        
         
         
         
         





