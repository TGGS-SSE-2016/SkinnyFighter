import pygame, sys
from pygame.locals import *
import math
from random import randint
import background

indigo = (121, 134, 203)
sun_red = (191,54,12)
radius_red = (230,74,25)
sea = (13,71,161)
lightblue1 = (3,155,229)
lightblue2 = (41,182,246)
blue = (2,119,189)
darkblue = (129,212,250)
white =(255,255,255)
orange = (255,152,0)
amber = (255,111,0)
earth = (0,77,64)

def draw(display,display_width,display_height):
    display.fill((255,255,255))
    draw_sand(display,display_width,display_height)
    draw_sky(display,display_width,display_height)
    draw_sun(display,display_width,display_height)
    draw_wave(display,display_width,display_height)

def draw_sun(display,display_width,display_height):
    sun_center = (200, 100)
    radius_number = 10+randint(0,10)
    radius_length = 40+randint(0,10)
    sub_radius_angle = 360/radius_number
    sun_radius = 50+randint(0,10)
    sun_radius_gap = 10+randint(0,10)
    for radius_index in range(0,radius_number):
        angle = math.radians((radius_index-1)*sub_radius_angle)
        X = sun_center[0]
        Y = sun_center[1]
        radius_start = radius_length+sun_radius_gap+randint(0,40)
        radius_end = sun_radius+radius_length+sun_radius_gap+randint(0,40)
        point1 = (math.floor(X - (math.cos(angle)*(radius_start))),math.floor(Y - (math.sin(angle)*(radius_start))))
        point2 = (math.floor(X - (math.cos(angle)*(radius_end))),math.floor(Y - (math.sin(angle)*(radius_end))))
        sun1 = pygame.draw.lines(display, radius_red, True, [point1,point2], 10)

    sun2 = pygame.draw.circle(display, sun_red, sun_center, radius_length, 0)

    return [sun1,sun2]

def draw_cloud(display,display_width,display_height):
    pygame.draw.arc(display, indigo, (600,150,100,80), math.radians(0), math.radians(randint(10,300)),4)

def draw_wave(display,display_width,display_height):
    sea_tick = 20
    rim_tick = 20
    start_point = 600
    sea_start = start_point
    wave_start = start_point
    max_wave = 10
    min_wave = 10
    max_amp = 50
    wave_gap = 25
    wave_gang = randint(min_wave,max_wave)

    for wave in range(0,wave_gang):
        vary_base = randint(30,50)
        amp = randint(vary_base,max_amp)
        wave_start -= wave_gap
        random_sea = randint(0,3)
        for xaxis in range(0,display_width):
            if wave == 0 or wave == wave_gang-1:
                wave = pygame.draw.circle(display, sea, (xaxis, (wave_start)+math.floor((amp)*math.sin(math.radians(xaxis)))), rim_tick, 0)
            elif wave == 0 or wave == wave_gang-1:
                wave = pygame.draw.circle(display, sea, (xaxis, (wave_start)+math.floor((amp)*math.sin(math.radians(xaxis)))), rim_tick, 0)
            else:
                if random_sea == 0:
                    wave = pygame.draw.circle(display, blue, (xaxis, (wave_start)+math.floor((amp)*math.sin(math.radians(xaxis)))), sea_tick, 0)
                elif random_sea == 1:
                    wave = pygame.draw.circle(display, lightblue1, (xaxis, (wave_start)+math.floor((amp)*math.sin(math.radians(xaxis)))), sea_tick, 0)
                elif random_sea == 2:
                    wave = pygame.draw.circle(display, lightblue2, (xaxis, (wave_start)+math.floor((amp)*math.sin(math.radians(xaxis)))), sea_tick, 0)
                elif random_sea == 3:
                    wave = pygame.draw.circle(display, darkblue, (xaxis, (wave_start)+math.floor((amp)*math.sin(math.radians(xaxis)))), sea_tick, 0)

    return wave

def draw_sky(display,display_width,display_height):
    start_point = 500
    end_point = 800
    gap = math.floor((end_point-start_point)/20)
    amp = 1
    for sand in range(0,4):
        amp = 10
        start = sand*30
        for xaxis in range(0,display_width,randint(5,20)):
            if randint(0,1) == 0:
                if sand%2 == 0:
                    sky = pygame.draw.circle(display, orange, (xaxis, (start)+math.floor((amp)*math.sin(math.radians(xaxis)))), 10, 0)
                else:
                    sky = pygame.draw.circle(display, amber, (xaxis, (start)+math.floor((amp)*math.sin(math.radians(xaxis)))), 10, 0)
            else:
                if sand%2 == 0:
                    sky = pygame.draw.circle(display, sea, (xaxis, (start)+math.floor((amp)*math.sin(math.radians(xaxis)))), 10, 0)
                else:
                    sky = pygame.draw.circle(display, blue, (xaxis, (start)+math.floor((amp)*math.sin(math.radians(xaxis)))), 10, 0)



def draw_sand(display,display_width,display_height):
    sand = pygame.draw.rect(display, earth, (0,0,display_width,display_height), 0)
    return sand
