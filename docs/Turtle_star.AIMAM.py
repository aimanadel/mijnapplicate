import turtle

aiman = turtle.Turtle()
aiman.getscreen().bgcolor("#994444")
aiman.color("yellow")
aiman.speed(0)

def star(t, size):
    if size <= 10:
        return
    for i in range(5):
        t.forward(size)
        star(t, size/2)
        t.left(216)

star(aiman, 100)
turtle.done()