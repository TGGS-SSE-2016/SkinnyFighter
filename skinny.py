import json
import math
import pygame
from pygame.locals import *
from random import randint
import sys

#HEAD 1 , 2 , 3 , 4


radius = 30;
mini_radius = 10;
H_body = 100;
W_body = 70;
N_RANDOM_WALK = 0;
arm_leg_length = 80
sword_length = 200;


COLOR = [(0, 0, 0), (128, 128, 128), (30, 128, 255), (255, 0, 0)];
INTERVAL_TIME = 150;        # milli sec
global MOTION_STATE;   MOTION_STATE = "IDLE";
MOTION_SEQ = 0;
BOT1_POSITION = [];
SWORD_ANGLE = 0;
cetha1 = 0;
cetha2 = 0;
cetha3 = 0; 
ATK_SPEED = 1;
CONTS_R_LEG_OFFSET = -5; 
data = [];

class Point:
    '''
    my node to keep row/column that bit change as list 
    '''
    def __init__(self, i, j):
        self.i = i 
        self.j = j
        
    def getX(self):
        return self.i;

    def getY(self):
        return self.j;
    
    def setX(self, val):
        self.i = val;
    def setY(self, val):
        self.j = val;
    
def getDestination(index, Angle, Length):
    global BOT1_POSITION;
    angle = -1 * Angle;
    radar = (BOT1_POSITION[index].getX(), BOT1_POSITION[index].getY())
    POS = BOT1_POSITION[index];
    x = BOT1_POSITION[index].getX() + math.cos(math.radians(angle)) * Length;
    y = BOT1_POSITION[index].getY() + math.sin(math.radians(angle)) * Length;
    return Point(x, y)    

#########                     UPDATE POINT
#HEAD
BOT1_POSITION.append(Point(256, 256));                           
#BODY
BOT1_POSITION.append(Point(256-W_body / 2, 256 + radius));    #TL_CORNER_POS 1
x = int(BOT1_POSITION[1].getX());
y = int(BOT1_POSITION[1].getY());
BOT1_POSITION.append(Point(x + W_body, y));                 #TR_CORNER_POS 2 
BOT1_POSITION.append(Point(x, y + H_body));                 #BL_CORNER_POS 3
BOT1_POSITION.append(Point(x + W_body, y + H_body));          #BR_CORNER_POS 4
#1st arm and leg
BOT1_POSITION.append(Point(256-W_body / 2-arm_leg_length, 256 + radius));    #TL_CORNER_POS 5
BOT1_POSITION.append(Point(x + W_body + arm_leg_length, y));                 #TR_CORNER_POS 6
BOT1_POSITION.append(Point(x, y + H_body + arm_leg_length));                 #BL_CORNER_POS 7
BOT1_POSITION.append(Point(x + W_body, y + H_body + arm_leg_length));          #BR_CORNER_POS 8



#2nd joint arm and foot
BOT1_POSITION.append(Point(BOT1_POSITION[5].getX()-arm_leg_length, BOT1_POSITION[5].getY()));    #TL_CORNER_POS 9
BOT1_POSITION.append(Point(BOT1_POSITION[6].getX() + arm_leg_length, BOT1_POSITION[6].getY()));                 #TR_CORNER_POS 10
BOT1_POSITION.append(Point(BOT1_POSITION[7].getX(), BOT1_POSITION[7].getY() + arm_leg_length));  #BL_CORNER_POS 11
BOT1_POSITION.append(Point(BOT1_POSITION[8].getX(), BOT1_POSITION[8].getY() + arm_leg_length));          #BR_CORNER_POS 12


#SWORD
BOT1_POSITION.append(Point(BOT1_POSITION[10].getX(), BOT1_POSITION[10].getY()-sword_length));          #SWORD 13
SWORD_ANGLE = 90;
########################################################################

pygame.init()
DISPLAY = pygame.display.set_mode((1024, 768))
DISPLAY.fill((255, 255, 255))                             #BG init

#ANGLE PATTERN 
WALK_MOTION = [
    [180, 235, 200, 210, 220], #L ARM 0
    [0, 355, 350, 355, 350], #R ARM 1
    [260, 280, 290, 250, 270], #L LEG 2
    [290, 260, 250, 280, 265], #R LEG 3
    [180, 235, 200, 210, 220], #L hand       4
    [0, 355, 350, 355, 350],   #R hand      5         
    [225, 190, 285, 240, 270], #L_FOOT 6
    [280, 250, 225, 275, 265]  #R FOOT  7
    ];    
                
IDLE_MOTION = [
    [225], #L ARM
    [0], #ARM
    [270], #L LEG
    [270],
    [250], #L ARM
    [0], #ARM
    [270], #L LEG
    [270]
    ];    #R LEG
                
    
MALEE_MOTION = [
    [225], #L ARM
    [45], #ARM ****************
    [270], #L LEG
    [270],
    [225], #L ARM
    [90], #ARM  ****************
    [270], #L LEG
    [270]
    ];    #R LEG


def initDrawSkinny():
    #HEAD
    pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(), BOT1_POSITION[0].getY()), radius, 0)
    #BODY
    pygame.draw.rect(DISPLAY,COLOR[0],(BOT1_POSITION[1].getX(),BOT1_POSITION[1].getY(),W_body,H_body))                     
    i = 1;
    while(i<=12):
        if i == 4 or i == 8 or i == 12:
            y_offset_r_leg = CONTS_R_LEG_OFFSET;
        else:
            y_offset_r_leg = 0           
        pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[i].getX()), int(BOT1_POSITION[i].getY())+y_offset_r_leg), mini_radius, 0);
        i = i+1;
    
    i = 1;
    while(i<=8):
        if i == 4 or i == 8:
            y_offset_r_leg = CONTS_R_LEG_OFFSET;
        else:
            y_offset_r_leg = 0         
        pygame.draw.line(DISPLAY, COLOR[2], (BOT1_POSITION[i].getX(), BOT1_POSITION[i].getY()+y_offset_r_leg), (BOT1_POSITION[i+4].getX(), BOT1_POSITION[i+4].getY()+y_offset_r_leg), 2)
        i = i+1;
    #Draw Weapon
    pygame.draw.line(DISPLAY, COLOR[3], (BOT1_POSITION[10].getX(), BOT1_POSITION[10].getY()), (BOT1_POSITION[13].getX(), BOT1_POSITION[13].getY()), 10)
        
        

def STATE_EVENT():
    
    DISPLAY.fill((255, 255, 255)) 
    
    if MOTION_STATE == "IDLE":
        IDLE();
    elif MOTION_STATE == "WALK":
        WALK();
    else:
        ATK();
    

def IDLE():
    
    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global N_RANDOM_WALK; N_RANDOM_WALK = randint(2, 5);
    print (MOTION_STATE, str(MOTION_SEQ));
    
    #Update state   
    myPoint = getDestination(1, IDLE_MOTION[0][MOTION_SEQ], arm_leg_length)
    BOT1_POSITION.insert(5, myPoint)            
    BOT1_POSITION.pop(6)
    
    myPoint1 = getDestination(2, IDLE_MOTION[1][MOTION_SEQ], arm_leg_length)
    BOT1_POSITION.insert(6, myPoint1)            
    BOT1_POSITION.pop(7)
   
    
    myPoint2 = getDestination(3, IDLE_MOTION[2][MOTION_SEQ], arm_leg_length)
    BOT1_POSITION.insert(7, myPoint2)            
    BOT1_POSITION.pop(8)
    
    myPoint3 = getDestination(4, IDLE_MOTION[3][MOTION_SEQ], arm_leg_length)
    BOT1_POSITION.insert(8, myPoint3)            
    BOT1_POSITION.pop(9)
    
    ####
    myPoint = getDestination(5, IDLE_MOTION[4][MOTION_SEQ], arm_leg_length)
    BOT1_POSITION.insert(9, myPoint)            
    BOT1_POSITION.pop(10)
    
    myPoint1 = getDestination(6, IDLE_MOTION[5][MOTION_SEQ], arm_leg_length)
    BOT1_POSITION.insert(10, myPoint1)            
    BOT1_POSITION.pop(11)
    
    myPoint2 = getDestination(7, IDLE_MOTION[6][MOTION_SEQ], arm_leg_length)
    BOT1_POSITION.insert(11, myPoint2)            
    BOT1_POSITION.pop(12)
    
    myPoint3 = getDestination(8, IDLE_MOTION[7][MOTION_SEQ], arm_leg_length)
    BOT1_POSITION.insert(12, myPoint3)            
    BOT1_POSITION.pop(13)
    
    #SWORD
    SWORD_ANGLE = IDLE_MOTION[5][MOTION_SEQ] + 90;
    myPoint4 = getDestination(10, SWORD_ANGLE, sword_length)
    BOT1_POSITION.insert(13, myPoint4)            
    BOT1_POSITION.pop(14)
    
    MOTION_STATE = "WALK"
    MOTION_SEQ = 0
    
    
def WALK():  
    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global SWORD_ANGLE;
    global sword_length;
    global N_RANDOM_WALK;
    print (MOTION_STATE, str(MOTION_SEQ));
    
    if MOTION_SEQ >= N_RANDOM_WALK:
        MOTION_STATE = "ATK"   
        MOTION_SEQ = 0;
        return   
    
    rand_step = randint(20, 50);
    direct = randint(0, 1);
    if direct == 0:
        rand_step *= -1;
    
    nextX = BOT1_POSITION[0].getX() + rand_step;
    if(nextX <= 150):
        nextX = 150;
    if(nextX > 462):
        nextX = 462;
    DIFX = nextX - BOT1_POSITION[0].getX();
    # need to limit range of step move 
    BOT1_POSITION[0].setX(nextX);
    #BODY
    i = 1;
    while i <= 4:
        BOT1_POSITION[i].setX(BOT1_POSITION[i].getX() + DIFX);    #
        i = i+1
        
    #ARM LEG 
    for i in range (8):
        myPoint = getDestination(i+1, WALK_MOTION[i][MOTION_SEQ], arm_leg_length)
        BOT1_POSITION.insert(i+5, myPoint)            
        BOT1_POSITION.pop(i+6)  
         
    #SWORD
    SWORD_ANGLE = WALK_MOTION[1][MOTION_SEQ] + 90;
    myPoint4 = getDestination(10, SWORD_ANGLE, sword_length)
    BOT1_POSITION.insert(13, myPoint4)            
    BOT1_POSITION.pop(14)

    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION_SEQ = MOTION_SEQ + 1;
    print (">>>", str(MOTION_SEQ))

def ATK():  
    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global SWORD_ANGLE;
    global sword_length;
    global N_RANDOM_WALK;
    global cetha1
    global cetha2 
    global cetha3
    
    print (MOTION_STATE, str(MOTION_SEQ));
    
    
     
    if (MOTION_SEQ == 0 ) :
        
        for i in range (8):
            myPoint = getDestination(i+1, MALEE_MOTION[i][MOTION_SEQ], arm_leg_length)
            BOT1_POSITION.insert(i+5, myPoint)            
            BOT1_POSITION.pop(i+6)               
        #SWORD
        cetha1 = 45
        cetha2 = 90
        cetha3 = (cetha2 + 90)%360;
        myPoint4 = getDestination(10, cetha3, sword_length)
        BOT1_POSITION.insert(13, myPoint4)            
        BOT1_POSITION.pop(14)       
    else:
        cetha1 = cetha1 - 5*ATK_SPEED;
        cetha2 = cetha2 - 5* ATK_SPEED*2;
        if cetha2 < cetha1:
            cetha2 = cetha1            
        cetha3 = (cetha2 + 90)%360;
 
        # 3 joint arm for atk
        myPoint1 = getDestination(2, cetha1, arm_leg_length)
        BOT1_POSITION.insert(6, myPoint1)            
        BOT1_POSITION.pop(7)        
        myPoint1 = getDestination(6, cetha2, arm_leg_length)
        BOT1_POSITION.insert(10, myPoint1)            
        BOT1_POSITION.pop(11)
        myPoint4 = getDestination(10, cetha3, sword_length)
        BOT1_POSITION.insert(13, myPoint4)            
        BOT1_POSITION.pop(14)
        
        print(cetha1)
    
    if (cetha1) < -60 :
        MOTION_STATE = "IDLE"   
        MOTION_SEQ = 0;
        return   
        
    

    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION_SEQ = MOTION_SEQ + 1;
    print (">>>", str(MOTION_SEQ))
    
    


def loadJSON():
    global data;
    with open('ATL.json') as data_file:
        data = json.load(data_file)
    


Eventid = pygame.USEREVENT + 1
pygame.time.set_timer(Eventid, INTERVAL_TIME)
initDrawSkinny()
pygame.display.update()
print("Hello World")
loadJSON()
print(data["om_points"]);

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if (event.type == Eventid):
            STATE_EVENT();
            initDrawSkinny()
            pygame.display.update()

