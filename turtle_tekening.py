import turtle

t = turtle.Turtle()
t.left(75)
t.forward(100)

t.right(150)
t.forward(100)

t.backward(50)
t.right(105)
t.forward(25)
t.penup()
t.goto(50, 0)
t.pendown()

t.left(90)
t.forward(100)
t.right(150)
t.forward(115)
t.left(150)
t.forward(100)
t.penup()
t.goto(150, 0)
t.pendown()

t.circle(30, 180)
t.circle(-30, 180)
turtle.done()