
import turtle

class Logo:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.pensize(3)

    def teken_w(self):
        self.t.penup()
        self.t.goto(250, 0)
        self.t.pendown()

        self.t.right(75)
        self.t.forward(100)
        self.t.left(150)
        self.t.forward(100)
        self.t.right(150)
        self.t.forward(100)
        self.t.left(150)
        self.t.forward(100)

logo = Logo()
logo.teken_w()

turtle.done()