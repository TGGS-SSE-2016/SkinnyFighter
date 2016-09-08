import pygame, sys
from pygame.locals import *
import math
from random import randint

radius = 30;
mini_radius = 10;
H_body = 100;
W_body = 70;
N_RANDOM_WALK = 0;
arm_leg_length = 80
sword_length = 180;


COLOR = [(0,0,0) , (128,128,128) , (30,128,255) , (255,0,0)];
BOT1_CUR_POS = [];
INTERVAL_TIME = 250;        # milli sec
global MOTION_STATE ;   MOTION_STATE = "IDLE";
MOTION_SEQ = 0;
BOT1_POSITION = [];
SWORD_ANGLE = 0;

class Point:
    '''
    my node to keep row/column that bit change as list
    '''
    def __init__(self,i,j):
        self.i = i
        self.j = j

    def getX(self):
        return self.i;

    def getY(self):
        return self.j;

    def setX(self,val):
         self.i = val;
    def setY(self,val):
        self.j = val;



#########                     UPDATE POINT
#HEAD
BOT1_POSITION.append(Point(256,256));
#BODY
BOT1_POSITION.append(Point(256-W_body/2,256+radius));    #TL_CORNER_POS
x =  int(BOT1_POSITION[1].getX());
y = int(BOT1_POSITION[1].getY());
BOT1_POSITION.append(Point(x+W_body,y));                 #TR_CORNER_POS
BOT1_POSITION.append(Point(x,y+H_body));                 #BL_CORNER_POS
BOT1_POSITION.append(Point(x+W_body,y+H_body));          #BR_CORNER_POS
#hands and foot
BOT1_POSITION.append(Point(256-W_body/2-arm_leg_length,256+radius));    #TL_CORNER_POS
BOT1_POSITION.append(Point(x+W_body+arm_leg_length,y));                 #TR_CORNER_POS
BOT1_POSITION.append(Point(x,y+H_body+arm_leg_length));                 #BL_CORNER_POS
BOT1_POSITION.append(Point(x+W_body,y+H_body+arm_leg_length));          #BR_CORNER_POS

#SWORD
BOT1_POSITION.append(Point(BOT1_POSITION[6].getX(),BOT1_POSITION[6].getY()-sword_length));          #SWORD
SWORD_ANGLE = 90;
########################################################################

pygame.init()
DISPLAY = pygame.display.set_mode((1024,768))
DISPLAY.fill((255,255,255))                             #BG init

#ANGLE PATTERN
WALK_MOTION = [ [180,235,200,210,220],      #L ARM
                [0,355,350,355,350],        #R
                [260,270,265,260,275],      #L LEG
                [280,285,280,275,270]] ;    #R LEG

IDLE_MOTION = [ [180],        #L ARM
                [0],       #ARM
                [270],      #L LEG
                [270]] ;    #R LEG

ATK_MOTION = [ [220,250,280,285,290],      #L ARM
                [335,330,320,310,300],        #R
                [270,270,270,270,270],      #L LEG
                [272,274,276,278,280]] ;    #R LEG

def getDestination(index,Angle , Length):
    global BOT1_POSITION;
    angle = -1 * Angle;
    radar = (BOT1_POSITION[index].getX(),BOT1_POSITION[index].getY())
    POS = BOT1_POSITION[index];
    x = BOT1_POSITION[index].getX() + math.cos(math.radians(angle)) * Length;
    y = BOT1_POSITION[index].getY()+ math.sin(math.radians(angle)) * Length;
    return Point(x,y)

def InitdrawSkinny():
        #HEAD
        pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
        #BODY
        pygame.draw.rect(
                    DISPLAY,
                    COLOR[0],
                    (BOT1_POSITION[1].getX(),  # x pos
                     BOT1_POSITION[1].getY(),  # y pos
                    W_body,   # width
                    H_body)   # height
                    )

        pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[1].getX()),int(BOT1_POSITION[1].getY())), mini_radius, 0);
        pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[2].getX()),int(BOT1_POSITION[2].getY())), mini_radius, 0);
        pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[3].getX()),int(BOT1_POSITION[3].getY())), mini_radius, 0);
        pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[4].getX()),int(BOT1_POSITION[4].getY())), mini_radius, 0);
        pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[5].getX()),int(BOT1_POSITION[5].getY())), mini_radius, 0);
        pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[6].getX()),int(BOT1_POSITION[6].getY())), mini_radius, 0);
        pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[7].getX()),int(BOT1_POSITION[7].getY())), mini_radius, 0);
        pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[8].getX()),int(BOT1_POSITION[8].getY())), mini_radius, 0);


        #ARM & LEG
        angle = -1 * 180;
        radar = (BOT1_POSITION[1].getX(),BOT1_POSITION[1].getY())
        x = BOT1_POSITION[1].getX() + math.cos(math.radians(angle)) * arm_leg_length;
        y = BOT1_POSITION[1].getY()+ math.sin(math.radians(angle)) * arm_leg_length;
        pygame.draw.line(DISPLAY, COLOR[2], radar, (x,y), 1)

        angle = -1 * 0;
        radar = (BOT1_POSITION[2].getX(),BOT1_POSITION[2].getY())
        x = BOT1_POSITION[2].getX() + math.cos(math.radians(angle)) * arm_leg_length;
        y = BOT1_POSITION[2].getY()+ math.sin(math.radians(angle)) * arm_leg_length;

        pygame.draw.line(DISPLAY, COLOR[2], radar, (x,y), 1)

        angle = -1 * 270;
        radar = (BOT1_POSITION[3].getX(),BOT1_POSITION[3].getY())
        x = BOT1_POSITION[3].getX() + math.cos(math.radians(angle)) * arm_leg_length;
        y = BOT1_POSITION[3].getY()+ math.sin(math.radians(angle)) * arm_leg_length;

        pygame.draw.line(DISPLAY, COLOR[2], radar, (x,y), 1)

        angle = -1 * 270;
        radar = (BOT1_POSITION[4].getX(),BOT1_POSITION[4].getY())
        x = BOT1_POSITION[4].getX() + math.cos(math.radians(angle)) * arm_leg_length;
        y = BOT1_POSITION[4].getY()+ math.sin(math.radians(angle)) * arm_leg_length;

        pygame.draw.line(DISPLAY, COLOR[2], radar, (x,y), 1)

        #Draw sword
        pygame.draw.line(DISPLAY, COLOR[3], (BOT1_POSITION[6].getX(),BOT1_POSITION[6].getY()), (BOT1_POSITION[9].getX(),BOT1_POSITION[9].getY()), 10)

def STATE_EVENT():

    DISPLAY.fill((255,255,255))

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
    global N_RANDOM_WALK; N_RANDOM_WALK =   randint(2,4);
    print (MOTION_STATE , str(MOTION_SEQ));
    MOTION_STATE = "WALK"
    MOTION_SEQ = 0
    #Update state
    myPoint = getDestination(1,IDLE_MOTION[0][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(5,myPoint)
    BOT1_POSITION.pop(6)

    myPoint1 = getDestination(2,IDLE_MOTION[1][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(6,myPoint1)
    BOT1_POSITION.pop(7)
    SWORD_ANGLE = IDLE_MOTION[1][MOTION_SEQ] +90 ;

    myPoint2 = getDestination(3,IDLE_MOTION[2][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(7,myPoint2)
    BOT1_POSITION.pop(8)

    myPoint3 = getDestination(4,IDLE_MOTION[3][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(8,myPoint3)
    BOT1_POSITION.pop(9)

    myPoint4 = getDestination(6,SWORD_ANGLE,sword_length)
    BOT1_POSITION.insert(9,myPoint4)
    BOT1_POSITION.pop(10)



def WALK():
    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global SWORD_ANGLE;
    global sword_length;
    global N_RANDOM_WALK;
    print (MOTION_STATE , str(MOTION_SEQ));

    if MOTION_SEQ >= N_RANDOM_WALK:
        MOTION_STATE = "ATK"
        MOTION_SEQ = 0;
        return

    rand_step = randint(20,50);
    direct = randint(0,1);
    if direct == 0:
        rand_step *= -1;

    nextX = BOT1_POSITION[0].getX() + rand_step;
    if(nextX <= 150):
        nextX = 150;
    if(nextX > 462):
        nextX = 462;
    DIFX = nextX - BOT1_POSITION[0].getX();
    # need to limit range of step move
    BOT1_POSITION[0].setX( nextX );
    #BODY
    BOT1_POSITION[1].setX(BOT1_POSITION[1].getX()+DIFX);    #
    BOT1_POSITION[2].setX(BOT1_POSITION[2].getX()+DIFX);    #
    BOT1_POSITION[3].setX(BOT1_POSITION[3].getX()+DIFX);    #
    BOT1_POSITION[4].setX(BOT1_POSITION[4].getX()+DIFX);    #

    #ARM LEG

    myPoint = getDestination(1,WALK_MOTION[0][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(5,myPoint)
    BOT1_POSITION.pop(6)

    myPoint1 = getDestination(2,WALK_MOTION[1][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(6,myPoint1)
    BOT1_POSITION.pop(7)
    SWORD_ANGLE = WALK_MOTION[1][MOTION_SEQ] +90 ;

    myPoint2 = getDestination(3,WALK_MOTION[2][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(7,myPoint2)
    BOT1_POSITION.pop(8)

    myPoint3 = getDestination(4,WALK_MOTION[3][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(8,myPoint3)
    BOT1_POSITION.pop(9)

    #SWORD
    myPoint4 = getDestination(6,SWORD_ANGLE,sword_length)
    BOT1_POSITION.insert(9,myPoint4)
    BOT1_POSITION.pop(10)

    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION_SEQ = MOTION_SEQ + 1;
    print (">>>" , str(MOTION_SEQ))

def ATK():
    global BOT1_POSITION;
    global MOTION_STATE;
    global MOTION_SEQ;
    global SWORD_ANGLE;
    global sword_length;
    global N_RANDOM_WALK;
    print (MOTION_STATE , str(MOTION_SEQ));

    if MOTION_SEQ >= 5:
        MOTION_STATE = "IDLE"
        MOTION_SEQ = 0;
        return

    #ARM LEG
    myPoint = getDestination(1,ATK_MOTION[0][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(5,myPoint)
    BOT1_POSITION.pop(6)

    myPoint1 = getDestination(2,ATK_MOTION[1][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(6,myPoint1)
    BOT1_POSITION.pop(7)
    SWORD_ANGLE = ATK_MOTION[1][MOTION_SEQ] +90 ;

    myPoint2 = getDestination(3,ATK_MOTION[2][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(7,myPoint2)
    BOT1_POSITION.pop(8)

    myPoint3 = getDestination(4,ATK_MOTION[3][MOTION_SEQ],arm_leg_length)
    BOT1_POSITION.insert(8,myPoint3)
    BOT1_POSITION.pop(9)

    #SWORD
    myPoint4 = getDestination(6,SWORD_ANGLE,sword_length)
    BOT1_POSITION.insert(9,myPoint4)
    BOT1_POSITION.pop(10)

    #pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    MOTION_SEQ = MOTION_SEQ + 1;
    print (">>>" , str(MOTION_SEQ))
def drawGame():
    #HEAD
    pygame.draw.circle(DISPLAY, COLOR[0], (BOT1_POSITION[0].getX(),BOT1_POSITION[0].getY()), radius, 0)
    #BODY
    pygame.draw.rect(
                    DISPLAY,
                    COLOR[0],
                    (BOT1_POSITION[1].getX(),  # x pos
                     BOT1_POSITION[1].getY(),  # y pos
                    W_body,   # width
                    H_body)   # height
                    )

    pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[1].getX()),int(BOT1_POSITION[1].getY())), mini_radius, 0);
    pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[2].getX()),int(BOT1_POSITION[2].getY())), mini_radius, 0);
    pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[3].getX()),int(BOT1_POSITION[3].getY())), mini_radius, 0);
    pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[4].getX()),int(BOT1_POSITION[4].getY())), mini_radius, 0);
    pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[5].getX()),int(BOT1_POSITION[5].getY())), mini_radius, 0);
    pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[6].getX()),int(BOT1_POSITION[6].getY())), mini_radius, 0);
    pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[7].getX()),int(BOT1_POSITION[7].getY())), mini_radius, 0);
    pygame.draw.circle(DISPLAY, COLOR[1], (int(BOT1_POSITION[8].getX()),int(BOT1_POSITION[8].getY())), mini_radius, 0);


    pygame.draw.line(DISPLAY, COLOR[2], (int(BOT1_POSITION[1].getX()),int(BOT1_POSITION[1].getY())), (int(BOT1_POSITION[5].getX()),int(BOT1_POSITION[5].getY())), 1)
    pygame.draw.line(DISPLAY, COLOR[2], (int(BOT1_POSITION[2].getX()),int(BOT1_POSITION[2].getY())), (int(BOT1_POSITION[6].getX()),int(BOT1_POSITION[6].getY())), 1)
    pygame.draw.line(DISPLAY, COLOR[2], (int(BOT1_POSITION[3].getX()),int(BOT1_POSITION[3].getY())), (int(BOT1_POSITION[7].getX()),int(BOT1_POSITION[7].getY())), 1)
    pygame.draw.line(DISPLAY, COLOR[2], (int(BOT1_POSITION[4].getX()),int(BOT1_POSITION[4].getY())), (int(BOT1_POSITION[8].getX()),int(BOT1_POSITION[8].getY())), 1)

    pygame.draw.line(DISPLAY, COLOR[3], (BOT1_POSITION[6].getX(),BOT1_POSITION[6].getY()), (BOT1_POSITION[9].getX(),BOT1_POSITION[9].getY()), 10)

Eventid = pygame.USEREVENT+1
pygame.time.set_timer(Eventid, INTERVAL_TIME)
InitdrawSkinny()
pygame.display.update()
print("Hello World")

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if (event.type == Eventid):
            STATE_EVENT();
            drawGame();
            pygame.display.update()
