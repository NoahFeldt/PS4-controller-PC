import pygame
from pynput.mouse import Controller as mc, Button
import threading

control = 1

sensitivity = 120

pixel = (8, 2)
direction = [0, 0]

scroll_direction = [0, 0]
scroll_pixel = 10

mouse = mc()
pygame.init()

clock = pygame.time.Clock()

j = pygame.joystick.Joystick(0)
j.init()

def move():
    while True:
        for i in range(0, 2):
            if control == i:
                mouse.move(int(pixel[i] * direction[0]), int(pixel[i] * direction[1]))
                clock.tick(sensitivity)
        
        mouse.scroll(int(scroll_pixel * scroll_direction[0]), int(scroll_pixel * -scroll_direction[1]))

def cursor(event):
    global control
    for i in range(2):
        if event.axis == i:
            if abs(event.value) > 0.2:
                control = 0
                direction[i] = event.value
            else:
                direction[i] = 0

    return direction

def scroll(event):
    global control
    for i in range(2, 4):
        if event.axis == i:
            if abs(event.value) > 0.2:
                control = 0
                scroll_direction[i - 2] = event.value
            else:
                scroll_direction[i - 2] = 0

    return scroll_direction

def game():
    global direction, control
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    mouse.press(Button.right)
                if event.button == 1:
                    mouse.press(Button.left)
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    mouse.release(Button.right)
                if event.button == 1:
                    mouse.release(Button.left)

            elif event.type == pygame.JOYAXISMOTION:
                cursor(event)
                scroll(event)
            elif event.type == pygame.JOYHATMOTION:
                control = 1
                direction = [event.value[0], -event.value[1]]

        clock.tick(sensitivity)

t = threading.Thread(target=move)
t.start()

game()