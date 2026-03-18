import turtle

class Tekening:
    def __init__(self):
        self.t = turtle.Turtle()

    def vierkant(self):
        self.t.color("blue")
        self.t.begin_fill()

        for i in range(4):
            self.t.forward(100)
            self.t.right(90)

        self.t.end_fill()

# object maken
tekening = Tekening()

# uitvoeren
tekening.vierkant()

turtle.done()
def tweede_vierkant(self):
    self.t.penup()
    self.t.goto(150, 0)
    self.t.pendown()

    for i in range(4):
        self.t.forward(100)
        self.t.right(90)