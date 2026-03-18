import turtle

ayman = turtle.Turtle()
ayman.getscreen().bgcolor("#994444")
ayman.color("yellow")
ayman.speed(0)

def star(t, size):
    if size <= 10:
        return
    for i in range(5):
        t.forward(size)
        star(t, size/2)
        t.left(216)

star(ayman, 100)
turtle.done()