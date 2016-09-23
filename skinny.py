import json
import math
import pygame
from pygame.locals import *
from random import randint
import background
import sys

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





####  BOT 1

#global MOTION_SEQ,MOTION2_SEQ
radius = 40;
mini_radius = 10;
H_body = 100;
W_body = 70;
N_RANDOM_WALK = 0;
arm_leg_length = 50
#global sword_length;
sword_length = 200;
COLOR = [(0, 0, 0), (128, 128, 128), (30, 128, 255), (255, 0, 0),(255,255,255)];


MOTION_SEQ = 0;
BOT1_POSITION = [];
SWORD_ANGLE = 0;

cetha1 = 0; # sword
cetha2 = 0; # sword
cetha3 = 0; # sword
cetha4 = 0; # for hammer
#global atk1_count
atk1_count = 0;

# Bot2 ################################
radius2 = 40;
mini_radius2 = 10;
H_body2 = 100;
W_body2 = 70;
N_RANDOM_WALK2 = 0;
arm_leg_length2 = 50
#global sword_length2;
sword_length2 = 200;
COLOR2 = [(0, 0, 255), (128, 128, 128), (255, 128, 255), (255, 0, 0),(255,255,255)];

MOTION2_SEQ = 0;
BOT2_POSITION = [];
SWORD_ANGLE2 = 0;

cetha21 = 0; # sword
cetha22 = 0; # sword
cetha23 = 0; # sword
cetha24 = 0; # for hammer
#global atk2_count
atk2_count = 0;

##
#global MOTION_STATE;
MOTION_STATE = "IDLE";
#global MOTION2_STATE;
MOTION2_STATE = "IDLE";


ATK_SPEED1 = 1.5;
ATK_SPEED2 = 1;

H_start_offset = 150
CONTS_R_LEG_OFFSET = -5;
INTERVAL_TIME = 100;        # milli sec
data = [];

#1.sword #2.hammer #3.scythe #4.fist

skinny_type1 = 5
skinny_type2 = 5

def randSkinny():
    global skinny_type1,skinny_type2
    cur1 = skinny_type1
    cur2 = skinny_type2
    while 1:
        rand = randint(1,4)
        if rand != cur1:
            skinny_type1 = rand
            break

    while 1:
        rand = randint(1,4)
        if rand != cur2 and rand != skinny_type1 :
            skinny_type2 = rand
            break



#PARAMETER SET
def parameterInit():
    randSkinny()
    # BOT 1
    global sword_length,ATK_SPEED1
    global sword_length2,ATK_SPEED2
    global atk1_count,atk2_count
    atk1_count = 30;
    atk2_count = 30;
    if skinny_type1 == 1:
        ATK_SPEED1 = 1.8;
        sword_length = 220;
    if skinny_type1 == 2:
        ATK_SPEED1 = 1;
        sword_length = 170;
    if skinny_type1 == 3:
        ATK_SPEED1 = 1.2;
        sword_length = 180;
    if skinny_type1 == 4:
        ATK_SPEED1 = 1.2;
        sword_length = 200
        pass;

    # BOT 2
    if skinny_type2 == 1:
        ATK_SPEED2 = 1.8;
        sword_length2 = 220;
    if skinny_type2 == 2:
        ATK_SPEED2 = 1;
        sword_length2 = 150;
    if skinny_type2 == 3:
        ATK_SPEED2 = 1.2;
        sword_length2 = 180;
    if skinny_type2 == 4:
        ATK_SPEED2 = 1.2;
        sword_length2 = 200;

def getDestination(index, Angle, Length):
    global BOT1_POSITION;
    angle = -1 * Angle;
    radar = (BOT1_POSITION[index].getX(), BOT1_POSITION[index].getY())
    x = BOT1_POSITION[index].getX() + math.cos(math.radians(angle)) * Length;
    y = BOT1_POSITION[index].getY() + math.sin(math.radians(angle)) * Length;
    return Point(x, y)

def getDestination2(index, Angle, Length):
    global BOT2_POSITION;
    angle = -1 * Angle;
    radar = (BOT2_POSITION[index].getX(), BOT2_POSITION[index].getY())
    x = BOT2_POSITION[index].getX() + math.cos(math.radians(angle)) * Length;
    y = BOT2_POSITION[index].getY() + math.sin(math.radians(angle)) * Length;
    return Point(x, y)


def getDestinationFromPoint(pointx,pointy, Angle, Length): # not use yet for hammer
    global BOT1_POSITION;
    angle = -1 * Angle;
    point = Point( pointx,pointy)
    x = point.getX() + math.cos(math.radians(angle)) * Length;
    y = point.getY() + math.sin(math.radians(angle)) * Length;
    return Point(x, y)

#########                     UPDATE POINT


def pointBot1Init():
    x_center = 256
    y_center = 256 + H_start_offset
    ##HEAD
    BOT1_POSITION.append(Point(x_center, y_center));
    #BODY
    BOT1_POSITION.append(Point(x_center-W_body / 2, y_center + radius));    #TL_CORNER_POS 1
    x = int(BOT1_POSITION[1].getX());
    y = int(BOT1_POSITION[1].getY());
    BOT1_POSITION.append(Point(x + W_body, y));                 #TR_CORNER_POS 2
    BOT1_POSITION.append(Point(x, y + H_body));                 #BL_CORNER_POS 3
    BOT1_POSITION.append(Point(x + W_body, y + H_body));          #BR_CORNER_POS 4
    #1st arm and leg
    BOT1_POSITION.append(Point(x_center-W_body / 2-arm_leg_length, y_center + radius));    #TL_CORNER_POS 5
    BOT1_POSITION.append(Point(x + W_body + arm_leg_length, y));                 #TR_CORNER_POS 6
    BOT1_POSITION.append(Point(x, y + H_body + arm_leg_length));                 #BL_CORNER_POS 7
    BOT1_POSITION.append(Point(x + W_body, y + H_body + arm_leg_length));          #BR_CORNER_POS 8
    #2nd joint arm and foot
    BOT1_POSITION.append(Point(BOT1_POSITION[5].getX()-arm_leg_length, BOT1_POSITION[5].getY()));    #TL_CORNER_POS 9
    BOT1_POSITION.append(Point(BOT1_POSITION[6].getX() + arm_leg_length, BOT1_POSITION[6].getY()));                 #TR_CORNER_POS 10
    BOT1_POSITION.append(Point(BOT1_POSITION[7].getX(), BOT1_POSITION[7].getY() + arm_leg_length));  #BL_CORNER_POS 11
    BOT1_POSITION.append(Point(BOT1_POSITION[8].getX(), BOT1_POSITION[8].getY() + arm_leg_length));          #BR_CORNER_POS 12
    #1st SWORD
    BOT1_POSITION.append(Point(BOT1_POSITION[10].getX(), BOT1_POSITION[10].getY()-sword_length));     #SWORD 13
    SWORD_ANGLE = 90;


########################################################################
def pointBot2Init():
    x_center = 768
    y_center = 256 + H_start_offset
    ##HEAD
    BOT2_POSITION.append(Point(x_center, y_center));
    #BODY
    BOT2_POSITION.append(Point(x_center-W_body2 / 2, y_center + radius2));    #TL_CORNER_POS 1

    x = int(BOT2_POSITION[1].getX());
    y = int(BOT2_POSITION[1].getY());
    BOT2_POSITION.append(Point(x + W_body2, y));                 #TR_CORNER_POS 2
    BOT2_POSITION.append(Point(x, y + H_body2));                 #BL_CORNER_POS 3
    BOT2_POSITION.append(Point(x + W_body2, y + H_body2));          #BR_CORNER_POS 4
    #1st arm and leg
    BOT2_POSITION.append(Point(x_center-W_body2 / 2-arm_leg_length2, y_center + radius2));    #TL_CORNER_POS 5
    BOT2_POSITION.append(Point(x + W_body2 + arm_leg_length2, y));                 #TR_CORNER_POS 6
    BOT2_POSITION.append(Point(x, y + H_body2 + arm_leg_length2));                 #BL_CORNER_POS 7
    BOT2_POSITION.append(Point(x + W_body2, y + H_body2 + arm_leg_length2));          #BR_CORNER_POS 8
    #2nd joint arm and foot
    BOT2_POSITION.append(Point(BOT2_POSITION[5].getX()-arm_leg_length2, BOT2_POSITION[5].getY()));    #TL_CORNER_POS 9
    BOT2_POSITION.append(Point(BOT2_POSITION[6].getX() + arm_leg_length2, BOT2_POSITION[6].getY()));                 #TR_CORNER_POS 10
    BOT2_POSITION.append(Point(BOT2_POSITION[7].getX(), BOT2_POSITION[7].getY() + arm_leg_length2));  #BL_CORNER_POS 11
    BOT2_POSITION.append(Point(BOT2_POSITION[8].getX(), BOT2_POSITION[8].getY() + arm_leg_length2));          #BR_CORNER_POS 12
    #1st SWORD
    BOT2_POSITION.append(Point(BOT2_POSITION[9].getX(), BOT2_POSITION[9].getY()-sword_length2));     #SWORD 13
    SWORD_ANGLE2 = 90;


########################################################################

parameterInit();
pointBot1Init();
pointBot2Init();
pygame.init()
display_width = 1024
display_height = 768
DISPLAY = pygame.display.set_mode((display_width, display_height))
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
    ];    #R LE
MELEE_MOTION = [
    [225], #L ARM
    [45], #ARM ****************
    [270], #L LEG
    [270],
    [225], #L ARM
    [90], #ARM  ****************
    [270], #L LEG
    [270]
    ];    #R LEG

MELEE_MOTION2 = [
    [135], #L ARM
    [315], #ARM ****************
    [270], #L LEG
    [270],
    [90], #L ARM
    [90], #ARM  ****************
    [270], #L LEG
    [270]
    ];    #R LEG


def initDrawSkinny1():
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
    #drawWeaponBot1();
    #Draw Item here!
    drawItemBot1();

def initDrawSkinny2():
    #HEAD
    pygame.draw.circle(DISPLAY, COLOR2[0], (BOT2_POSITION[0].getX(), BOT2_POSITION[0].getY()), radius2, 0)
    #BODY
    pygame.draw.rect(DISPLAY,COLOR2[0],(BOT2_POSITION[1].getX(),BOT2_POSITION[1].getY(),W_body2,H_body2))
    i = 1;
    while(i<=12):
        if i == 4 or i == 8 or i == 12:
            y_offset_r_leg = CONTS_R_LEG_OFFSET;
        else:
            y_offset_r_leg = 0
        pygame.draw.circle(DISPLAY, COLOR2[1], (int(BOT2_POSITION[i].getX()), int(BOT2_POSITION[i].getY())+y_offset_r_leg), mini_radius, 0);
        i = i+1;

    i = 1;
    while(i<=8):
        if i == 4 or i == 8:
            y_offset_r_leg = CONTS_R_LEG_OFFSET;
        else:
            y_offset_r_leg = 0
        pygame.draw.line(DISPLAY, COLOR2[2], (BOT2_POSITION[i].getX(), BOT2_POSITION[i].getY()+y_offset_r_leg), (BOT2_POSITION[i+4].getX(), BOT2_POSITION[i+4].getY()+y_offset_r_leg), 2)
        i = i+1;
    #Draw Weapon
    #drawWeaponBot2();
    #Draw Item here!
    drawItemBot2();


def drawWeaponBot1():
    global MOTION_STATE
    pointlist = []
    if skinny_type1 == 1:
        pygame.draw.line(DISPLAY, COLOR[3], (BOT1_POSITION[10].getX(), BOT1_POSITION[10].getY()), (BOT1_POSITION[13].getX(), BOT1_POSITION[13].getY()), 10)
    if skinny_type1 == 2:
        pygame.draw.line(DISPLAY, COLOR[3], (BOT1_POSITION[10].getX(), BOT1_POSITION[10].getY()), (BOT1_POSITION[13].getX(), BOT1_POSITION[13].getY()), 15)
        myPoint = getDestination(13, cetha2, 100)                               #14
        pointlist.append( (BOT1_POSITION[13].getX(), BOT1_POSITION[13].getY() ))
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        myPoint = getDestination(13, cetha2-30, 80)                     #15
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        myPoint = getDestination(13, cetha2-90, 30)                     #16
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        myPoint = getDestination(13, cetha2+210, 80)                     #17
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        myPoint = getDestination(13, cetha2+180, 100)                     #18
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        pygame.draw.polygon(DISPLAY,COLOR[3] , pointlist  , 0)
        # hammer
        ang = 0
    if skinny_type1 == 3:
        pygame.draw.line(DISPLAY, COLOR[3], (BOT1_POSITION[10].getX(), BOT1_POSITION[10].getY()), (BOT1_POSITION[13].getX(), BOT1_POSITION[13].getY()), 15)
        circle_angle = 90-30
        for i in range ( circle_angle ):
            ceta = cetha2+90-i
            p = getDestinationFromPoint( BOT1_POSITION[10].getX(), BOT1_POSITION[10].getY(), ceta , sword_length )
            pointlist.append( ( p.getX(), p.getY()))

        myPoint = getDestination(10, cetha2+90, sword_length - 20)
        pointlist.append( (myPoint.getX(), myPoint.getY() ))

        pygame.draw.polygon(DISPLAY,COLOR[3] , pointlist  , 0)
        # hammer
    if skinny_type1 == 4:
        if MOTION_STATE == "ATK":
            pygame.draw.line(DISPLAY, COLOR[3], (BOT1_POSITION[10].getX(), BOT1_POSITION[10].getY()), (BOT1_POSITION[13].getX(), BOT1_POSITION[13].getY()), 2)
            pygame.draw.circle(DISPLAY, COLOR[3], (int(BOT1_POSITION[13].getX()),int(BOT1_POSITION[13].getY())), 20, 0)
        else:
            pygame.draw.line(DISPLAY, COLOR[3], (BOT1_POSITION[10].getX(), BOT1_POSITION[10].getY()), (BOT1_POSITION[10].getX(), sword_length+BOT1_POSITION[10].getY()), 2)
            pygame.draw.circle(DISPLAY, COLOR[3], (int(BOT1_POSITION[10].getX()),sword_length+int(BOT1_POSITION[10].getY())), 20, 0)
            pass;


def drawWeaponBot2():
    global MOTION2_STATE
    pointlist = []
    if skinny_type2 == 1:
        pygame.draw.line(DISPLAY, COLOR2[3], (BOT2_POSITION[9].getX(), BOT2_POSITION[9].getY()), (BOT2_POSITION[13].getX(), BOT2_POSITION[13].getY()), 10)
    if skinny_type2 == 2:
        pygame.draw.line(DISPLAY, COLOR2[3], (BOT2_POSITION[9].getX(), BOT2_POSITION[9].getY()), (BOT2_POSITION[13].getX(), BOT2_POSITION[13].getY()), 15)
        myPoint = getDestination2(13, cetha22, 100)                               #14
        pointlist.append( (BOT2_POSITION[13].getX(), BOT2_POSITION[13].getY() ))
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        myPoint = getDestination2(13, cetha22-30, 80)                     #15
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        myPoint = getDestination2(13, cetha22-90, 30)                     #16
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        myPoint = getDestination2(13, cetha22+210, 80)                     #17
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        myPoint = getDestination2(13, cetha22+180, 100)                     #18
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        pygame.draw.polygon(DISPLAY,COLOR2[3] , pointlist  , 0)
        # hammer
    if skinny_type2 == 3:
        pygame.draw.line(DISPLAY, COLOR2[3], (BOT2_POSITION[9].getX(), BOT2_POSITION[9].getY()), (BOT2_POSITION[13].getX(), BOT2_POSITION[13].getY()), 15)
        circle_angle2 = (cetha22+270) %360
        for i in range (60):
            ceta_ = circle_angle2+i
            p = getDestinationFromPoint( BOT2_POSITION[9].getX(), BOT2_POSITION[9].getY(), ceta_ , sword_length2 )
            pointlist.append( ( p.getX(), p.getY()))
        myPoint = getDestination2(9, cetha22+270, sword_length2 - 20)
        pointlist.append( (myPoint.getX(), myPoint.getY() ))
        pygame.draw.polygon(DISPLAY,COLOR2[3] , pointlist  , 0)
    if skinny_type2 == 4:
        if MOTION2_STATE == "ATK":
            pygame.draw.line(DISPLAY, COLOR2[3], (BOT2_POSITION[9].getX(), BOT2_POSITION[9].getY()), (BOT2_POSITION[13].getX(), BOT2_POSITION[13].getY()), 2)
            pygame.draw.circle(DISPLAY, COLOR2[3], (int(BOT2_POSITION[13].getX()),int(BOT2_POSITION[13].getY())), 20, 0)
        else:
            pygame.draw.line(DISPLAY, COLOR2[3], (BOT2_POSITION[9].getX(), BOT2_POSITION[9].getY()), (BOT2_POSITION[9].getX(), sword_length+BOT2_POSITION[9].getY()), 2)
            pygame.draw.circle(DISPLAY, COLOR2[3], (int(BOT2_POSITION[9].getX()),sword_length2+int(BOT2_POSITION[9].getY())), 20, 0)
            pass;





def drawItemBot1():
    if skinny_type1 == 1:
        img = pygame.image.load("glasses.png").convert_alpha()
        DISPLAY.blit(img , (BOT1_POSITION[0].getX()-radius,BOT1_POSITION[0].getY()))
    if skinny_type1 == 2:
        img = pygame.image.load("glasses.png").convert_alpha()
        DISPLAY.blit(img , (BOT1_POSITION[0].getX()-radius,BOT1_POSITION[0].getY()))
    if skinny_type1 == 3:
        offset_eye = int(radius/randint(2, 3))
        eye_size = int(radius/randint(3, 4))
        eye_size = int(radius/randint(3, 4))
        pygame.draw.circle(DISPLAY, COLOR[4], (BOT1_POSITION[0].getX()+ offset_eye+3 ,BOT1_POSITION[0].getY()  ), int(eye_size), 0)
        pygame.draw.circle(DISPLAY, COLOR[3], (BOT1_POSITION[0].getX()+ offset_eye+3, BOT1_POSITION[0].getY()  ), int(eye_size*.75), 0)
        pygame.draw.circle(DISPLAY, COLOR[4], (BOT1_POSITION[0].getX()- offset_eye+3 ,BOT1_POSITION[0].getY()  ), int(eye_size), 0)
        pygame.draw.circle(DISPLAY, COLOR[3], (BOT1_POSITION[0].getX()- offset_eye+3, BOT1_POSITION[0].getY()  ), int(eye_size*.75), 0)
    if skinny_type1 == 4:
        img = pygame.image.load("face.png").convert_alpha()
        DISPLAY.blit(img , (BOT1_POSITION[1].getX(),BOT1_POSITION[1].getY()))

def drawItemBot2():
    if skinny_type2 == 1:
        img = pygame.image.load("Thug-Life.png").convert_alpha()
        DISPLAY.blit(img , (BOT2_POSITION[0].getX()-radius,BOT2_POSITION[0].getY()))
    if skinny_type2 == 2:
        img = pygame.image.load("Thug-Life.png").convert_alpha()
        DISPLAY.blit(img , (BOT2_POSITION[0].getX()-radius,BOT2_POSITION[0].getY()))
    if skinny_type2 == 3:
        offset_eye = int(radius/randint(2, 3))
        eye_size = int(radius/randint(3, 4))
        eye_size = int(radius/randint(3, 4))
        pygame.draw.circle(DISPLAY, COLOR2[4], (BOT2_POSITION[0].getX()+ offset_eye-3 ,BOT2_POSITION[0].getY()  ), int(eye_size), 0)
        pygame.draw.circle(DISPLAY, COLOR2[3], (BOT2_POSITION[0].getX()+ offset_eye-3, BOT2_POSITION[0].getY()  ), int(eye_size*.75), 0)
        pygame.draw.circle(DISPLAY, COLOR2[4], (BOT2_POSITION[0].getX()- offset_eye-3 ,BOT2_POSITION[0].getY()  ), int(eye_size), 0)
        pygame.draw.circle(DISPLAY, COLOR2[3], (BOT2_POSITION[0].getX()- offset_eye-3, BOT2_POSITION[0].getY()  ), int(eye_size*.75), 0)
    if skinny_type2 == 4:
        img = pygame.image.load("face.png").convert_alpha()
        DISPLAY.blit(img , (BOT2_POSITION[1].getX(),BOT2_POSITION[1].getY()))

def STATE_EVENT1(): # for bot 1
    background.draw(DISPLAY,display_width,display_height)
    global atk1_count
    if MOTION_STATE == "IDLE":
        IDLE();
    elif MOTION_STATE == "WALK":
        WALK();
    else:
        if skinny_type1 == 1:
            ATK_SWORD();
        elif skinny_type1 == 2:
            ATK_HAMMER();
        elif skinny_type1 == 3 :
            ATK_SCYTHE();
        elif skinny_type1 == 4 :
            ATK_PENDULUM();
        atk1_count = atk1_count - 1

def STATE_EVENT2(): # for bot 1
    global atk2_count
    if MOTION2_STATE == "IDLE":
        IDLE2();
    elif MOTION2_STATE == "WALK":
        WALK2();
    else:
        if skinny_type2 == 1:
            ATK_SWORD2()
        elif skinny_type2 == 2:
            ATK_HAMMER2()
        elif skinny_type2 == 3:
            ATK_SCYTHE2()
        elif skinny_type2 == 4:
            ATK_PENDULUM2()
        atk2_count = atk2_count - 1





def IDLE():

    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global N_RANDOM_WALK; N_RANDOM_WALK = randint(2, 5);
    global cetha2;

    #print (MOTION_STATE, str(MOTION_SEQ));

    #Update state

    for i in range (8):
        myPoint = getDestination(i+1, IDLE_MOTION[i][MOTION_SEQ], arm_leg_length)
        BOT1_POSITION.insert(i+5, myPoint)
        BOT1_POSITION.pop(i+6)


    #SWORD
    SWORD_ANGLE = IDLE_MOTION[5][MOTION_SEQ] + 90;
    myPoint4 = getDestination(10, SWORD_ANGLE, sword_length)
    BOT1_POSITION.insert(13, myPoint4)
    BOT1_POSITION.pop(14)
    cetha2 = SWORD_ANGLE-90

    MOTION_STATE = "WALK"
    MOTION_SEQ = 0

def IDLE2():

    global BOT2_POSITION;
    global MOTION2_STATE;
    global MOTION2_SEQ;
    global N_RANDOM_WALK2; N_RANDOM_WALK2 = randint(2, 5);
    global cetha22;

    #print (MOTION2_STATE, str(MOTION2_SEQ));

    #Update state

    for i in range (8):
        myPoint = getDestination2(i+1, IDLE_MOTION[i][MOTION2_SEQ], arm_leg_length2)
        BOT2_POSITION.insert(i+5, myPoint)
        BOT2_POSITION.pop(i+6)


    #SWORD
    SWORD_ANGLE2 = IDLE_MOTION[5][MOTION2_SEQ] + 90;
    myPoint4 = getDestination2(9, SWORD_ANGLE2, sword_length2)
    BOT2_POSITION.insert(13, myPoint4)
    BOT2_POSITION.pop(14)
    cetha22 = SWORD_ANGLE2+90

    MOTION2_STATE = "WALK"
    MOTION2_SEQ = 0


def WALK():
    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global SWORD_ANGLE;
    global sword_length;
    global N_RANDOM_WALK;
    global cetha2;
    #print (MOTION_STATE, str(MOTION_SEQ));

    if MOTION_SEQ >= N_RANDOM_WALK:
        MOTION_STATE = "ATK"
        MOTION_SEQ = 0;
        return

    rand_step = randint(20, 50);
    direct = randint(0, 1);
    if direct == 0:
        rand_step *= -1;

    nextX = BOT1_POSITION[0].getX() + rand_step;
    if(nextX <  150):
        nextX = 150;
    if(nextX > 512-100):
        nextX = 512-100;
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
    #for hammer
    cetha2 = SWORD_ANGLE-90
    MOTION_SEQ = MOTION_SEQ + 1;
    #print (">>>", str(MOTION_SEQ))

def WALK2():
    global BOT2_POSITION;
    global MOTION2_STATE;
    global MOTION2_SEQ;
    global SWORD_ANGLE2;
    global sword_length2;
    global N_RANDOM_WALK2;
    global cetha22;
    #print (MOTION2_STATE, str(MOTION2_SEQ));

    if MOTION2_SEQ >= N_RANDOM_WALK2:
        MOTION2_STATE = "ATK"
        MOTION2_SEQ = 0;
        return

    rand_step = randint(20, 50);
    direct = randint(0, 1);
    if direct == 0:
        rand_step *= -1;

    nextX = BOT2_POSITION[0].getX() + rand_step;
    if(nextX >= 1024 - 150):
        nextX = 1024- 150;
    if(nextX < 512+100):
        nextX = 512+100;
    DIFX = nextX - BOT2_POSITION[0].getX();
    # need to limit range of step move
    BOT2_POSITION[0].setX(nextX);
    #BODY
    i = 1;
    while i <= 4:
        BOT2_POSITION[i].setX(BOT2_POSITION[i].getX() + DIFX);    #
        i = i+1

    #ARM LEG
    for i in range (8):
        myPoint = getDestination2(i+1, WALK_MOTION[i][MOTION2_SEQ], arm_leg_length2)
        BOT2_POSITION.insert(i+5, myPoint)
        BOT2_POSITION.pop(i+6)
    #SWORD
    SWORD_ANGLE2 = WALK_MOTION[1][MOTION2_SEQ] + 270;
    myPoint4 = getDestination2(9, SWORD_ANGLE2, sword_length2)
    BOT2_POSITION.insert(13, myPoint4)
    BOT2_POSITION.pop(14)
    #for hammer
    cetha22 = SWORD_ANGLE2+90

    MOTION2_SEQ = MOTION2_SEQ + 1;
    #print ("2 >>>", str(MOTION2_SEQ)," ",str(cetha22))

def ATK_SWORD():
    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global SWORD_ANGLE;
    global sword_length;
    global N_RANDOM_WALK;
    global cetha1
    global cetha2
    global cetha3

    #print (MOTION_STATE, str(MOTION_SEQ));



    if (MOTION_SEQ == 0 ) :

        for i in range (8):
            myPoint = getDestination(i+1, MELEE_MOTION[i][MOTION_SEQ], arm_leg_length)
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
        cetha1 = cetha1 - 5*ATK_SPEED1;
        cetha2 = cetha2 - 5* ATK_SPEED1*2;
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

        #print(cetha1)

    if (cetha1) < -60 :
        MOTION_STATE = "IDLE"
        MOTION_SEQ = 0;
        return



    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION_SEQ = MOTION_SEQ + 1;
    #print (">>>", str(MOTION_SEQ))

def ATK_SWORD2():
    global BOT2_POSITION;
    global MOTION2_STATE;
    global MOTION2_SEQ;
    global SWORD_ANGLE2;
    global sword_length2;
    global N_RANDOM_WALK2;
    global cetha21
    global cetha22
    global cetha23

    #print (MOTION2_STATE, str(MOTION2_SEQ));

    if (MOTION2_SEQ == 0 ) :

        for i in range (8):
            myPoint = getDestination2(i+1, MELEE_MOTION2[i][MOTION2_SEQ], arm_leg_length2)
            BOT2_POSITION.insert(i+5, myPoint)
            BOT2_POSITION.pop(i+6)
        #SWORD
        cetha21 = 135
        cetha22 = 90
        cetha23 = 0;
        myPoint4 = getDestination2(9, cetha23, sword_length2)
        BOT2_POSITION.insert(13, myPoint4)
        BOT2_POSITION.pop(14)
    else:
        cetha21 = cetha21 + 5*ATK_SPEED2;
        cetha22 = cetha22 + 5* ATK_SPEED2*2;
        if cetha22 > cetha21:
            cetha22 = cetha21
        cetha23 = cetha22-90

        # 3 joint arm for atk
        myPoint1 = getDestination2(1, cetha21, arm_leg_length2)
        BOT2_POSITION.insert(5, myPoint1)
        BOT2_POSITION.pop(6)
        myPoint1 = getDestination2(5, cetha22, arm_leg_length2)
        BOT2_POSITION.insert(9, myPoint1)
        BOT2_POSITION.pop(10)
        myPoint4 = getDestination2(9, cetha23, sword_length2)
        BOT2_POSITION.insert(13, myPoint4)
        BOT2_POSITION.pop(14)

        #print(cetha1)
    if (cetha21) > 240 :
        MOTION2_STATE = "IDLE"
        MOTION2_SEQ = 0;
        return



    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION2_SEQ = MOTION2_SEQ + 1;
    #print (">>>", str(MOTION2_SEQ))

def ATK_HAMMER():
    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global SWORD_ANGLE;
    global sword_length;
    global N_RANDOM_WALK;
    global cetha1
    global cetha2
    global cetha3
    #print (ATK_SPEED1,"SS")
    #print (MOTION_STATE, str(MOTION_SEQ))
    if (MOTION_SEQ == 0 ) :
        for i in range (8):
            myPoint = getDestination(i+1, MELEE_MOTION[i][MOTION_SEQ], arm_leg_length)
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
        cetha1 = cetha1 - 5* ATK_SPEED1;
        cetha2 = cetha2 - 5* ATK_SPEED1*2;
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

    if (cetha1) < -60 :
        MOTION_STATE = "IDLE"
        MOTION_SEQ = 0;
        return



    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION_SEQ = MOTION_SEQ + 1;
    #print (">>>", str(MOTION_SEQ))

def ATK_HAMMER2():
    global BOT2_POSITION;
    global MOTION2_STATE;
    global MOTION2_SEQ;
    global SWORD_ANGLE2;
    global sword_length2;
    global N_RANDOM_WALK2;
    global cetha21
    global cetha22
    global cetha23
    #print (ATK_SPEED2,"SS")
    #print (MOTION2_STATE, str(MOTION2_SEQ))
    if (MOTION2_SEQ == 0 ) :
        for i in range (8):
            myPoint = getDestination2(i+1, MELEE_MOTION[i][MOTION2_SEQ], arm_leg_length2)
            BOT2_POSITION.insert(i+5, myPoint)
            BOT2_POSITION.pop(i+6)
        #SWORD
        cetha21 = 135
        cetha22 = 90
        cetha23 = 0;
        myPoint4 = getDestination2(9, cetha23, sword_length2)
        BOT2_POSITION.insert(13, myPoint4)
        BOT2_POSITION.pop(14)
    else:
        cetha21 = cetha21 + 5 *ATK_SPEED2;
        cetha22 = cetha22 + 5* ATK_SPEED2*2;
        if cetha22 > cetha21:
            cetha22 = cetha21
        cetha23 = cetha22-90
        # 3 joint arm for atk
        myPoint1 = getDestination2(1, cetha21, arm_leg_length2)
        BOT2_POSITION.insert(5, myPoint1)
        BOT2_POSITION.pop(6)
        myPoint1 = getDestination2(5, cetha22, arm_leg_length2)
        BOT2_POSITION.insert(9, myPoint1)
        BOT2_POSITION.pop(10)
        myPoint4 = getDestination2(9, cetha23, sword_length2)
        BOT2_POSITION.insert(13, myPoint4)
        BOT2_POSITION.pop(14)

    if (cetha21) > 240 :
        MOTION2_STATE = "IDLE"
        MOTION2_SEQ = 0;
        return



    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION2_SEQ = MOTION2_SEQ + 1;
    #print (">>>", str(MOTION2_SEQ))

def ATK_SCYTHE():
    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global SWORD_ANGLE;
    global sword_length;
    global N_RANDOM_WALK;
    global cetha1
    global cetha2
    global cetha3
    #print (ATK_SPEED1,"SS")
    #print (MOTION_STATE, str(MOTION_SEQ))
    if (MOTION_SEQ == 0 ) :
        for i in range (8):
            myPoint = getDestination(i+1, MELEE_MOTION[i][MOTION_SEQ], arm_leg_length)
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
        cetha1 = cetha1 - 5* ATK_SPEED1;
        cetha2 = cetha2 - 5* ATK_SPEED1*2;
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

    if (cetha1) < -60 :
        MOTION_STATE = "IDLE"
        MOTION_SEQ = 0;
        return


    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION_SEQ = MOTION_SEQ + 1;
    #print (">>>", str(MOTION_SEQ))

def ATK_SCYTHE2():
    global BOT2_POSITION;
    global MOTION2_STATE;
    global MOTION2_SEQ;
    global SWORD_ANGLE2;
    global sword_length2;
    global N_RANDOM_WALK2;
    global cetha21
    global cetha22
    global cetha23
    #print (ATK_SPEED2,"SS")
    #print (MOTION2_STATE, str(MOTION2_SEQ))
    if (MOTION2_SEQ == 0 ) :
        for i in range (8):
            myPoint = getDestination2(i+1, MELEE_MOTION[i][MOTION2_SEQ], arm_leg_length2)
            BOT2_POSITION.insert(i+5, myPoint)
            BOT2_POSITION.pop(i+6)
        #SWORD
        cetha21 = 135
        cetha22 = 90
        cetha23 = 0;
        myPoint4 = getDestination2(9, cetha23, sword_length2)
        BOT2_POSITION.insert(13, myPoint4)
        BOT2_POSITION.pop(14)
    else:
        cetha21 = cetha21 + 5 *ATK_SPEED2;
        cetha22 = cetha22 + 5* ATK_SPEED2*2;
        if cetha22 > cetha21:
            cetha22 = cetha21
        cetha23 = cetha22-90
        # 3 joint arm for atk
        myPoint1 = getDestination2(1, cetha21, arm_leg_length2)
        BOT2_POSITION.insert(5, myPoint1)
        BOT2_POSITION.pop(6)
        myPoint1 = getDestination2(5, cetha22, arm_leg_length2)
        BOT2_POSITION.insert(9, myPoint1)
        BOT2_POSITION.pop(10)
        myPoint4 = getDestination2(9, cetha23, sword_length2)
        BOT2_POSITION.insert(13, myPoint4)
        BOT2_POSITION.pop(14)

    if (cetha21) > 240 :
        MOTION2_STATE = "IDLE"
        MOTION2_SEQ = 0;
        return



    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION2_SEQ = MOTION2_SEQ + 1;
    #print (">>>SCY ", str(cetha21))

def ATK_PENDULUM():
    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global SWORD_ANGLE;
    global sword_length;
    global N_RANDOM_WALK;
    global cetha1
    global cetha2
    global cetha3

    #print (MOTION_STATE, str(MOTION_SEQ));

    if (MOTION_SEQ == 0 ) :

        for i in range (8):
            myPoint = getDestination(i+1, MELEE_MOTION[i][MOTION_SEQ], arm_leg_length)
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
        cetha1 = cetha1 - 5*ATK_SPEED1;
        cetha2 = cetha2 - 5* ATK_SPEED1*2;
        if cetha2 < cetha1:
            cetha2 = cetha1
        cetha3 = cetha3 - 30 #(cetha2 + 90)%360;

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

        #print(cetha1)
    if (cetha1) < -60 :
        MOTION_STATE = "IDLE"
        MOTION_SEQ = 0;
        return

    MOTION_SEQ = MOTION_SEQ + 1;

def ATK_PENDULUM2():
    global BOT2_POSITION;
    global MOTION2_STATE;
    global MOTION2_SEQ;
    global SWORD_ANGLE2;
    global sword_length2;
    global N_RANDOM_WALK2;
    global cetha21
    global cetha22
    global cetha23
    #print (ATK_SPEED2,"SS")
    #print (MOTION2_STATE, str(MOTION2_SEQ))
    if (MOTION2_SEQ == 0 ) :
        for i in range (8):
            myPoint = getDestination2(i+1, MELEE_MOTION[i][MOTION2_SEQ], arm_leg_length2)
            BOT2_POSITION.insert(i+5, myPoint)
            BOT2_POSITION.pop(i+6)
        #SWORD
        cetha21 = 135
        cetha22 = 90
        cetha23 = 0;
        myPoint4 = getDestination2(9, cetha23, sword_length2)
        BOT2_POSITION.insert(13, myPoint4)
        BOT2_POSITION.pop(14)
    else:
        cetha21 = cetha21 + 5 *ATK_SPEED2;
        cetha22 = cetha22 + 5* ATK_SPEED2*2;
        if cetha22 > cetha21:
            cetha22 = cetha21
        cetha23 = cetha23+30
        # 3 joint arm for atk
        myPoint1 = getDestination2(1, cetha21, arm_leg_length2)
        BOT2_POSITION.insert(5, myPoint1)
        BOT2_POSITION.pop(6)
        myPoint1 = getDestination2(5, cetha22, arm_leg_length2)
        BOT2_POSITION.insert(9, myPoint1)
        BOT2_POSITION.pop(10)
        myPoint4 = getDestination2(9, cetha23, sword_length2)
        BOT2_POSITION.insert(13, myPoint4)
        BOT2_POSITION.pop(14)

    if (cetha21) > 240 :
        MOTION2_STATE = "IDLE"
        MOTION2_SEQ = 0;
        return



    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION2_SEQ = MOTION2_SEQ + 1;
    #print (">>>", str(MOTION2_SEQ))



def loadJSON():
    global data;
    with open('ATL.json') as data_file:
        data = json.load(data_file)


def initAll():
    ####  BOT 1

    parameterInit();
    initDrawSkinny1();
    initDrawSkinny2();

def checkDamage():
    global MOTION_STATE,MOTION2_STATE,MOTION_SEQ,MOTION2_SEQ

    if atk1_count < 0 or atk2_count < 0:
        print("KO1")
        initAll()
        pointBot1Init();
        pointBot2Init();
        MOTION_STATE = "IDLE"
        MOTION2_STATE = "IDLE"
        MOTION_SEQ = 0
        MOTION2_SEQ = 0

def randColor1():
    COLOR[3] = (randint(0,255) ,randint(0,255) ,randint(0,255)  )

def randColor2():
    COLOR2[3] = (randint(0,255) ,randint(0,255) ,randint(0,255)  )

Eventid = pygame.USEREVENT + 1
pygame.time.set_timer(Eventid, INTERVAL_TIME)
initAll()
pygame.display.update();
print("Hello World")
loadJSON()
print(data["om_points"]);
pygame.key.set_repeat(1, 3)
while True:
    for event in pygame.event.get():
        keys=pygame.key.get_pressed();
        if keys[K_UP]:
            randColor1()
        if keys[K_DOWN]:
            randColor2()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if (event.type == Eventid):
            DISPLAY.fill((255, 255, 255))  # BG HERE
            STATE_EVENT1();
            STATE_EVENT2();
            initDrawSkinny1()
            initDrawSkinny2()
            drawWeaponBot1();
            drawWeaponBot2();
            pygame.display.update()
            ## calculate damage
            checkDamage();
