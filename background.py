import pygame
import sys
from pygame.locals import *
import math
from random import randint
import background
import time

class vec2d(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

indigo = (121, 134, 203)
sun_red = (191, 54, 12)
radius_red = (230, 74, 25)
sea = (13, 71, 161)
lightblue1 = (3, 155, 229)
lightblue2 = (41, 182, 246)
blue = (2, 119, 189)
darkblue = (129, 212, 250)
white = (255, 255, 255)
orange = (255, 152, 0)
amber = (255, 111, 0)
earth = (0, 77, 64)
day_sky = (128,222,234)
dark_sky = (0,96,100)
moon = (255,241,118)


def draw(display, display_width, display_height):
    millis_weight = 10
    mod_range = 1000
    mod_weight = millis_weight*mod_range
    mod_middle = mod_weight/2
    millis = int(round(time.time() * 1000))
    display.fill((255, 255, 255))
    if millis%mod_weight > mod_middle:
        draw_day(display, display_width, display_height)
    elif millis%mod_weight< mod_middle:
        draw_dark(display, display_width, display_height)

    draw_sky(display, display_width, display_height)
    draw_wave(display, display_width, display_height)

    if millis%mod_weight > mod_middle:
        draw_sun(display, display_width, display_height)
    elif millis%mod_weight< mod_middle:
        draw_moon(display)


def draw_sun(display, display_width, display_height):
    sun_center = (200, 100)
    radius_number = 10 + randint(0, 10)
    radius_length = 40 + randint(0, 10)
    sub_radius_angle = 360 / radius_number
    sun_radius = 50 + randint(0, 10)
    sun_radius_gap = 10 + randint(0, 10)
    for radius_index in range(0, radius_number):
        angle = math.radians((radius_index - 1) * sub_radius_angle)
        X = sun_center[0]
        Y = sun_center[1]
        radius_start = radius_length + sun_radius_gap + randint(0, 40)
        radius_end = sun_radius + radius_length + \
            sun_radius_gap + randint(0, 40)
        point1 = (math.floor(X - (math.cos(angle) * (radius_start))),
                  math.floor(Y - (math.sin(angle) * (radius_start))))
        point2 = (math.floor(X - (math.cos(angle) * (radius_end))),
                  math.floor(Y - (math.sin(angle) * (radius_end))))
        pygame.draw.lines(
            display, radius_red, True, [point1, point2], 10)

    pygame.draw.circle(display, sun_red, sun_center, radius_length, 0)


def draw_cloud(display, display_width, display_height):
    pygame.draw.arc(display, indigo, (600, 150, 100, 80),
                    math.radians(0), math.radians(randint(10, 300)), 4)


def draw_wave(display, display_width, display_height):
    sea_tick = 20
    rim_tick = 20
    start_point = 600
    sea_start = start_point
    wave_start = start_point
    max_wave = 10
    min_wave = 10
    max_amp = 50
    wave_gap = 25
    wave_gang = randint(min_wave, max_wave)

    for wave in range(0, wave_gang, 2):
        vary_base = randint(30, 50)
        amp = randint(vary_base, max_amp)
        wave_start -= wave_gap
        random_sea = randint(0, 3)
        for xaxis in range(0, display_width, 15):
            if wave == 0 or wave == wave_gang - 1:
                pygame.draw.circle(display, sea, (xaxis, (wave_start) + math.floor(
                    (amp) * math.sin(math.radians(xaxis)))), rim_tick, 0)
            elif wave == 0 or wave == wave_gang - 1:
                pygame.draw.circle(display, sea, (xaxis, (wave_start) + math.floor(
                    (amp) * math.sin(math.radians(xaxis)))), rim_tick, 0)
            else:
                if random_sea == 0:
                    pygame.draw.circle(display, blue, (xaxis, (wave_start) + math.floor(
                        (amp) * math.sin(math.radians(xaxis)))), sea_tick, 0)
                elif random_sea == 1:
                    pygame.draw.circle(display, lightblue1, (xaxis, (
                        wave_start) + math.floor((amp) * math.sin(math.radians(xaxis)))), sea_tick, 0)
                elif random_sea == 2:
                    pygame.draw.circle(display, lightblue2, (xaxis, (
                        wave_start) + math.floor((amp) * math.sin(math.radians(xaxis)))), sea_tick, 0)
                elif random_sea == 3:
                    pygame.draw.circle(display, darkblue, (xaxis, (wave_start) + math.floor(
                        (amp) * math.sin(math.radians(xaxis)))), sea_tick, 0)


def draw_sky(display, display_width, display_height):
    start_point = 500
    end_point = 800
    gap = math.floor((end_point - start_point) / 20)
    amp = 1
    for sand in range(0, 4):
        amp = 10
        start = sand * 30
        for xaxis in range(0, display_width, randint(5, 20)):
            if randint(0, 1) == 0:
                if sand % 2 == 0:
                    pygame.draw.circle(
                        display, orange, (xaxis, (start) + math.floor((amp) * math.sin(math.radians(xaxis)))), 10, 0)
                else:
                    pygame.draw.circle(
                        display, amber, (xaxis, (start) + math.floor((amp) * math.sin(math.radians(xaxis)))), 10, 0)
            else:
                if sand % 2 == 0:
                    pygame.draw.circle(
                        display, sea, (xaxis, (start) + math.floor((amp) * math.sin(math.radians(xaxis)))), 10, 0)
                else:
                    pygame.draw.circle(
                        display, blue, (xaxis, (start) + math.floor((amp) * math.sin(math.radians(xaxis)))), 10, 0)


def draw_day(display, display_width, display_height):
    pygame.draw.rect(
        display, day_sky, (0, 0, display_width, display_height), 0)

def draw_dark(display, display_width, display_height):
    pygame.draw.rect(
        display, dark_sky, (0, 0, display_width, display_height), 0)


def draw_moon(display):
    width = 30
    height = 200
    moon_head = [300, 100]
    moon_tail = [moon_head[0], moon_head[1] + height]
    body_top = [moon_head[0]-(width+80), moon_head[1]+20]
    body_low = [moon_head[0]-(width+80), moon_tail[1]-20]

    for fillMoon in range(0, width):
        control_points = [vec2d(moon_head[0], moon_head[1]), vec2d(body_top[0]+fillMoon, body_top[
            1]), vec2d(body_low[0]+fillMoon, body_low[1]), vec2d(moon_tail[0], moon_tail[1])]

        # Draw bezier curve
        b_points = compute_bezier_points([(x.x, x.y) for x in control_points])
        pygame.draw.lines(display, moon, False, b_points, 2)


def compute_bezier_points(vertices, numPoints=None):
    if numPoints is None:
        numPoints = 30
    if numPoints < 2 or len(vertices) != 4:
        return None

    result = []

    b0x = vertices[0][0]
    b0y = vertices[0][1]
    b1x = vertices[1][0]
    b1y = vertices[1][1]
    b2x = vertices[2][0]
    b2y = vertices[2][1]
    b3x = vertices[3][0]
    b3y = vertices[3][1]

    # Compute polynomial coefficients from Bezier points
    ax = -b0x + 3 * b1x + -3 * b2x + b3x
    ay = -b0y + 3 * b1y + -3 * b2y + b3y

    bx = 3 * b0x + -6 * b1x + 3 * b2x
    by = 3 * b0y + -6 * b1y + 3 * b2y

    cx = -3 * b0x + 3 * b1x
    cy = -3 * b0y + 3 * b1y

    dx = b0x
    dy = b0y

    # Set up the number of steps and step size
    numSteps = numPoints - 1  # arbitrary choice
    h = 1.0 / numSteps  # compute our step size

    # Compute forward differences from Bezier points and "h"
    pointX = dx
    pointY = dy

    firstFDX = ax * (h * h * h) + bx * (h * h) + cx * h
    firstFDY = ay * (h * h * h) + by * (h * h) + cy * h

    secondFDX = 6 * ax * (h * h * h) + 2 * bx * (h * h)
    secondFDY = 6 * ay * (h * h * h) + 2 * by * (h * h)

    thirdFDX = 6 * ax * (h * h * h)
    thirdFDY = 6 * ay * (h * h * h)

    # Compute points at each step
    result.append((int(pointX), int(pointY)))

    for i in range(numSteps):
        pointX += firstFDX
        pointY += firstFDY

        firstFDX += secondFDX
        firstFDY += secondFDY

        secondFDX += thirdFDX
        secondFDY += thirdFDY

        result.append((int(pointX), int(pointY)))

    return result
