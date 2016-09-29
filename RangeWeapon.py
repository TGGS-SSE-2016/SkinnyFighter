import pygame
import math, random

class RangeWeapon:

    shuriken_scale_distance_x = 4
    shuriken_scale_distance_y = 4
    shuriken_power_range_lower = 30
    shuriken_power_range_upper = 60
    shuriken_angle_range_lower = 0
    shuriken_angle_range_upper = 45
    shuriken_step_time = 0.4
    shuriken_color = (255, 0, 0)
    shuriken_center_color = (0, 0, 0)
    #shuriken_color_left = (255, 0, 0)
    #shuriken_color_right = (0, 0, 255)
    #shuriken_center_color = (0, 0, 0)

    u = random.randint(shuriken_power_range_lower, shuriken_power_range_upper)
    angle = random.randint(shuriken_angle_range_lower, shuriken_angle_range_upper) * math.pi / 180
    t = 0
    g = 10
    x = 0
    y = 0
    theta = 0
    hand_x = 0
    hand_y = 0
    drawX = 0
    drawY = 0

    r_shuriken = [40, 15]
    r_circle_shuriken = 10
    theta_offset = [0,30,90,120,180,210,270,300]

    #Character Position only 1 or 2 - 1 is left side, 2 is right side
    #Shuriken type have 2 type - odd and even
    def __init__(self, display_width, display_height, character_position, shuriken_type):
        self.display_width = display_width
        self.display_height = display_height
        self.character_position = character_position
        self.shuriken_type = shuriken_type

    def getDrawX(self):
        return self.drawX

    def getDrawY(self):
        return self.drawY

    def getRadius(self):
        return self.r_shuriken[0]

    def shuriken_setup(self, hand_x, hand_y, shuriken_color, shuriken_center_color):
        self.hand_x = hand_x
        self.hand_y = hand_y
        self.shuriken_color = shuriken_color
        self.shuriken_center_color = shuriken_center_color

    def shuriken_show(self, display):
        #global u, angle, time, g, x, y, theta, r_shuriken, r_circle_shuriken, theta_offset
        
        self.x = self.u * math.cos(self.angle) * self.t
        self.y = self.u * math.sin(self.angle) * self.t - self.g * pow(self.t,2) / 2
        
        if self.character_position == 1:
            self.drawX = int(self.hand_x + (self.x * self.shuriken_scale_distance_x))
            self.drawY = int(self.hand_y - (self.y * self.shuriken_scale_distance_y))
        else:
            self.drawX = int(self.hand_x - self.x * self.shuriken_scale_distance_x)
            self.drawY = int(self.hand_y - (self.y * self.shuriken_scale_distance_y))

        self.t += self.shuriken_step_time
        self.theta += self.u
        
        if self.shuriken_type%2 != 0:
            shuriken_point = []
            for i in range(len(self.theta_offset)):
                shuriken_point.append([self.drawX + (self.r_shuriken[i%2] * math.cos((self.theta + self.theta_offset[i]) * math.pi / 180)),self.drawY + (self.r_shuriken[i%2] * math.sin((self.theta + self.theta_offset[i]) * math.pi / 180))])
        else:
            shuriken_point = [[-10, -10],[0, -40],[10, -10],[40, 0],[10, 10],[0, 40],[-10, 10],[-40, 0]]
            for i in range(len(shuriken_point)):
                shuriken_point[i][0] = self.drawX + (shuriken_point[i][0] * math.cos(self.theta * math.pi / 180))
                shuriken_point[i][1] = self.drawY + (shuriken_point[i][1] * math.sin(self.theta * math.pi / 180))
        pygame.draw.polygon(display, self.shuriken_color, shuriken_point)
        pygame.draw.circle(display, self.shuriken_center_color, (self.drawX, self.drawY), self.r_circle_shuriken)
        if self.character_position == 1:
            if self.drawY > self.display_height or self.drawX > self.display_width:
                self.t = 0
                self.theta = 0
                self.u = random.randint(self.shuriken_power_range_lower, self.shuriken_power_range_upper)
                self.angle = random.randint(self.shuriken_angle_range_lower, self.shuriken_angle_range_upper) * math.pi / 180
                self.x = 0
                self.y = 0
                return True
            else:
                return False
        else:
            if self.drawY < 0 or self.drawX < 0:
                self.t = 0
                self.theta = 0
                self.u = random.randint(self.shuriken_power_range_lower, self.shuriken_power_range_upper)
                self.angle = random.randint(self.shuriken_angle_range_lower, self.shuriken_angle_range_upper) * math.pi / 180
                self.x = 0
                self.y = 0
                return True
            else:
                return False
