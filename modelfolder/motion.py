import math
import cv2
import mediapipe as mp
import numpy as np
from experta import *
from enum import Enum




class motion(Enum):
    
    CLOSED_U_HANDS = 1
    CLOSED_D_HANDS = 2
    STRAIGHT_DOWN = 3 
    HAND_ON_HIP = 4 
    HAND_CROSSED = 5
    HAND_ON_HEAD = 6 
    HAND_CROSSED_LEFT =7 
    HAND_CROSSED_RIGHT = 8
    CLOSSED_HAND_LEFT = 9
    CLOSSED_HAND_RIGHT = 10
    STRAIGHT_DOWN_LEFT = 11
    STRAIGHT_DOWN_RIGHT = 12 
    HAND_ON_HEAD_right = 13 
    HAND_ON_HEAD_left = 14
    HAND_ON_HIP_Left = 15 
    HAND_ON_HIP_Right = 16 
    HANDS_OUT_BOX = 17
        
############################# تعريف  enum خاصة بالاتجاهات  #####################################
class direction(Enum):
    straight = 0 
    right = 1 
    left = 2 
    
##############################        facts  تعريف ال  #######################################        
class destance(Fact):
    pass 

class angle(Fact):
    pass

class BodyPart(Fact):
    pass 

class direction_type (Fact): 
    pass 

####################################      كلاس القواعد     ################################### 
class ReturnValueFact:
    my_variable = None 
    my_direction = None
    my_text = None
    normalize_destance = None
    def set_variable(self, value):
        if isinstance(value, motion):
            self.my_variable = value
   
    def set_direction(self, value):
        if isinstance(value, direction):
            self.my_direction = value
            
        
    def set_text(self, value):
        self.my_text = value     
    
    def set_normalize_destance(self, value):
        self.normalize_destance = value     


class Tree(KnowledgeEngine):

    def __init__(self, instance_of_my_class):
        super().__init__()
        self.instance_of_my_class = instance_of_my_class
        
    def set_value_method(self, value):
        self.instance_of_my_class.set_variable(value)
        
    def set_direction_method(self, value):
        self.instance_of_my_class.set_direction(value)    

    def set_text_method(self, value):
        self.instance_of_my_class.set_text(value)        
        
    def set_normalize_destance(self, value):
        self.instance_of_my_class.set_normalize_destance(value)   
        
        
    @Rule( 
         angle(angle1=P(lambda x: x < 30)), angle(angle2=P(lambda x: 50 < x <100)),
         angle(angle3=P(lambda x: x < 30)), angle(angle4=P(lambda x: 50 < x <100)) ,
         AS.fact5 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2) ,
         AS.fact6 <<  Fact(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 >= dist4) ,
         direction_type(direct = P(lambda x: x == 0)) 
         )
    def check(self):        
        value =motion.CLOSED_U_HANDS
        self.set_value_method( value)
    
            
    @Rule(angle(angle1=P(lambda x: x < 30)), angle(angle2=P(lambda x:  150>x >100)),
         angle(angle3=P(lambda x: x < 30)), angle(angle4=P(lambda x:  150>x >100)) ,
         AS.fact5 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2),
         direction_type(direct = P(lambda x: x == 0)))
    def check2(self):        
        value =motion.CLOSED_D_HANDS
        self.set_value_method( value)
    
    
    @Rule(angle(angle1=P(lambda x: x >30)), angle(angle2=P(lambda x:  140>x >60)),
         angle(angle3=P(lambda x: x > 30)), angle(angle4=P(lambda x:  140>x >60)) ,
         AS.fact5 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 >= dist2),
         direction_type(direct = P(lambda x: x == 0)))
    def check3(self):        
        value =motion.HAND_ON_HIP
        self.set_value_method( value)

        
    
    @Rule(angle(angle1=P(lambda x: x <30)), angle(angle2=P(lambda x: x >40)),
          angle(angle3=P(lambda x: x <30)), angle(angle4=P(lambda x: x >40)),
         AND(
         AS.fact3 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2),
         AS.fact4 <<  Fact(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4)),
         direction_type(direct = P(lambda x: x == 0)))
    def check4(self):        
        value =motion.HAND_CROSSED
        self.set_value_method( value)  
        
        
    @Rule(
    angle(angle1=P(lambda x: x >115)), angle(angle2=P(lambda x: x>115)),
    AS.fact1 << BodyPart(Rsh_x_pos=MATCH.Rsh_x_pos,Rw_x_pos=MATCH.Rw_x_pos),
    AS.fact2 << BodyPart(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
    TEST(lambda Rw_x_pos,Rsh_x_pos : Rw_x_pos < (Rsh_x_pos + 50)),
    TEST(lambda Rsh_x_pos,Rw_x_pos:( Rsh_x_pos - 50) < Rw_x_pos),
    TEST(lambda Lw_x_pos,Lsh_x_pos : Lw_x_pos < (Lsh_x_pos + 50)),
    TEST(lambda Lsh_x_pos,Lw_x_pos:( Lsh_x_pos - 50) < Lw_x_pos),      
    direction_type(direct = P(lambda x: x == 0)))
    def check5(self):
        value = motion.STRAIGHT_DOWN
        self.set_value_method(value)   
        
        
    @Rule(
    angle(angle1=P(lambda x: x >115)), angle(angle2=P(lambda x: x>115)),
    AS.fact1 << BodyPart(Rsh_x_pos=MATCH.Rsh_x_pos,Rw_x_pos=MATCH.Rw_x_pos),
    AS.fact2 << BodyPart(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
    TEST(lambda Rw_x_pos,Rsh_x_pos : Rw_x_pos < (Rsh_x_pos + 50)),
    TEST(lambda Rsh_x_pos,Rw_x_pos:( Rsh_x_pos - 50) < Rw_x_pos),
    TEST(lambda Lw_x_pos,Lsh_x_pos : Lw_x_pos < (Lsh_x_pos + 50)),
    TEST(lambda Lsh_x_pos,Lw_x_pos:( Lsh_x_pos - 50) < Lw_x_pos),      
    direction_type(direct = P(lambda x: x == 2)))
    def check6(self):
        value = motion.STRAIGHT_DOWN_LEFT
        self.set_value_method(value)    
        
        
    @Rule(
    angle(angle1=P(lambda x: x >115)), angle(angle2=P(lambda x: x>115)),
    AS.fact1 << BodyPart(Rsh_x_pos=MATCH.Rsh_x_pos,Rw_x_pos=MATCH.Rw_x_pos),
    AS.fact2 << BodyPart(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
    TEST(lambda Rw_x_pos,Rsh_x_pos : Rw_x_pos < (Rsh_x_pos + 50)),
    TEST(lambda Rsh_x_pos,Rw_x_pos:( Rsh_x_pos - 50) < Rw_x_pos),
    TEST(lambda Lw_x_pos,Lsh_x_pos : Lw_x_pos < (Lsh_x_pos + 50)),
    TEST(lambda Lsh_x_pos,Lw_x_pos:( Lsh_x_pos - 50) < Lw_x_pos),      
    direction_type(direct = P(lambda x: x == 1)))
    def check7(self):
        value = motion.STRAIGHT_DOWN_RIGHT
        self.set_value_method(value)  
        
        
    @Rule(angle(angle1=P(lambda x: x <40)), angle(angle2=P(lambda x: x >40)),
          angle(angle3=P(lambda x: x <40)), angle(angle4=P(lambda x: x >40)),
         AS.fact3 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2),
         AS.fact4 <<  Fact(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4),
         direction_type(direct = P(lambda x: x == 2 )))
    def check8(self):        
        value =motion.HAND_CROSSED_LEFT
        self.set_value_method( value)
        
        
        
    @Rule(angle(angle1=P(lambda x: x <40)), angle(angle2=P(lambda x: x >40)),
          angle(angle3=P(lambda x: x <40)), angle(angle4=P(lambda x: x >40)),
         AS.fact3 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2),
         AS.fact4 <<  Fact(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4),
         direction_type(direct = P(lambda x: x == 1 )))
    def check9(self):        
        value =motion.HAND_CROSSED_RIGHT
        self.set_value_method( value)     
        
        
        
    @Rule(OR(
          AND(AND(angle(angle1=P(lambda x: x <25)), angle(angle2=P(lambda x: x <30))),
          AS.fact1 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2)), 
        
          AND(AND(angle(angle3=P(lambda x: x <25)), angle(angle4=P(lambda x: x <30))) ,
          AND (AS.fact2 <<  Fact(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4)))) ,
          direction_type(direct = P(lambda x: x == 0))
           ) 
    def check10(self):        
        value =motion.HAND_ON_HEAD
        self.set_value_method(value)

        
        
    @Rule(
          AND(AND(angle(angle1=P(lambda x: 25<x <40)), angle(angle2=P(lambda x: 30< x <60))),
          AS.fact1 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2)),
        
#           AND(AND(angle(angle3=P(lambda x: x <30)), angle(angle4=P(lambda x: x <40))) ,
#           AND (AS.fact2 <<  Fact(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4)))) ,
          direction_type(direct = P(lambda x: x == 2))
           ) 
    
    def check11(self):        
        value =motion.HAND_ON_HEAD_left
        self.set_value_method(value)
        

        

    @Rule(
          AND(AND(angle(angle1=P(lambda x: 25<x <40)), angle(angle2=P(lambda x: 30< x <60))),
          AS.fact1 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 < dist2)),
        
#           AND(AND(angle(angle3=P(lambda x: x <30)), angle(angle4=P(lambda x: x <40))) ,
#           AND (AS.fact2 <<  Fact(dist3 = MATCH.dist3,dist4 =MATCH.dist4),TEST(lambda dist3,dist4: dist3 < dist4)))) ,
          direction_type(direct = P(lambda x: x == 1))
           ) 
    
    def check12(self):        
        value =motion.HAND_ON_HEAD_right
        self.set_value_method(value)        
        

        
    @Rule(angle(angle1=P(lambda x: x >30)), angle(angle2=P(lambda x:  150>x >60)),
#          AS.fact5 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 >= dist2),
         AS.fact2 << BodyPart(Rsh_x_pos=MATCH.Rsh_x_pos,Rw_x_pos=MATCH.Rw_x_pos),
         TEST(lambda Rw_x_pos,Rsh_x_pos : Rw_x_pos < (Rsh_x_pos + 50)),
         TEST(lambda Rsh_x_pos,Rw_x_pos:( Rsh_x_pos - 50) < Rw_x_pos), 
         direction_type(direct = P(lambda x: x == 2)))
    def check14(self):        
        value =motion.HAND_ON_HIP_Left
        self.set_value_method( value)
 

    @Rule(angle(angle1=P(lambda x: x >30)), angle(angle2=P(lambda x:  150>x >60)),
#          AS.fact5 <<  Fact(dist1 = MATCH.dist1,dist2 =MATCH.dist2),TEST(lambda dist1,dist2: dist1 >= dist2),
         AS.fact2 << BodyPart(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
         TEST(lambda Lw_x_pos,Lsh_x_pos : Lw_x_pos < (Lsh_x_pos + 50)),
         TEST(lambda Lsh_x_pos,Lw_x_pos:( Lsh_x_pos - 50) < Lw_x_pos), 
         direction_type(direct = P(lambda x: x == 1)))
    def check15(self):        
        value =motion.HAND_ON_HIP_Right
        self.set_value_method( value)        

                
    @Rule(angle(angle1=P(lambda x: x >30)), angle(angle2=P(lambda x:  135>x >80)),
         AS.fact2 << BodyPart(Rsh_x_pos=MATCH.Rsh_x_pos,Rw_x_pos=MATCH.Rw_x_pos),
         TEST(lambda Rw_x_pos,Rsh_x_pos : Rw_x_pos > (Rsh_x_pos + 20)),
         direction_type(direct = P(lambda x: x == 2)))
    def check16(self):        
        value =motion.CLOSSED_HAND_LEFT
        self.set_value_method( value)
 

    @Rule(angle(angle1=P(lambda x: x >30)), angle(angle2=P(lambda x:  135>x >80)),
         AS.fact2 << BodyPart(Lsh_x_pos=MATCH.Lsh_x_pos,Lw_x_pos=MATCH.Lw_x_pos),
         TEST(lambda Lw_x_pos,Lsh_x_pos : Lw_x_pos < (Lsh_x_pos - 20)),
         direction_type(direct = P(lambda x: x == 1)))
    def check17(self):        
        value =motion.CLOSSED_HAND_RIGHT
        self.set_value_method( value)  