import turtle

class LogoANSW:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.speed(3)
        self.t.pensize(4)

    def teken_vierkant(self, x, y, grootte):
        self.t.penup()
        self.t.goto(x, y)
        self.t.pendown()
        self.t.color("black")
        for _ in range(4):
            self.t.forward(grootte)
            self.t.right(90)
        self.t.penup()

    def teken_A(self):
        self.t.color("red")
        self.t.penup()
        self.t.goto(10, 0)  # aangepaste positie
        self.t.pendown()
        self.t.left(75)
        self.t.forward(60)   # kleiner
        self.t.right(150)
        self.t.forward(60)   # kleiner
        self.t.backward(30)
        self.t.right(105)
        self.t.forward(15)
        self.t.setheading(0)

    def teken_N(self):
        self.t.color("green")
        self.t.penup()
        self.t.goto(80, 0)   # positie aangepast
        self.t.pendown()
        self.t.left(90)
        self.t.forward(60)
        self.t.right(150)
        self.t.forward(70)
        self.t.left(150)
        self.t.forward(60)
        self.t.setheading(0)

    def teken_S(self):
        self.t.color("blue")
        self.t.penup()
        self.t.goto(150, 30)  # positie aangepast
        self.t.pendown()
        self.t.right(90)
        self.t.circle(20, 180)  # kleiner
        self.t.circle(-20, 180)
        self.t.setheading(0)

    def teken_W(self):
        self.t.color("purple")
        self.t.penup()
        self.t.goto(210, 0)   # positie aangepast
        self.t.pendown()
        self.t.right(75)
        self.t.forward(60)
        self.t.left(150)
        self.t.forward(60)
        self.t.right(150)
        self.t.forward(60)
        self.t.left(150)
        self.t.forward(60)
        self.t.setheading(0)

# Maak object en teken het kleinere vierkant + logo
logo = LogoANSW()
logo.teken_vierkant(0, 100, 300)  # kleiner vierkant, past beter
logo.teken_A()
logo.teken_N()
logo.teken_S()
logo.teken_W()

turtle.hideturtle()
turtle.done()