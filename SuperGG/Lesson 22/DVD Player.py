import random
import time
import turtle
Screen = turtle.Screen()
Screen.title("DVD Player")
turtle.tracer(0)
colors = ["red", "blue", "green", "yellow", "orange", "purple",]
t=turtle.Turtle("circle")
t.left(45)
t.up()
x = 0
y = 0
dx = 10
dy = 10
while True:
    x = x + dx
    y = y + dy
    t.setpos(x, y)
    if x >= 300 or x <= -300:
        dx = -dx
        c = random.choice(colors)
        t.color(c)
    if y >= 250 or y <= -250:
        dy = -dy
        c = random.choice(colors)
        t.color(c)
    turtle.update()
    time.sleep(0.03)
