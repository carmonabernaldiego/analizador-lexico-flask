
x = 10
y = 20
z = 30


def add(a, b):
    return a + b


if x > y:
    print("x es mayor que y")
elif x < y:
    print("x es menor que y")
else:
    print("x es igual a y")

for i in range(10):
    print(i)

while x < 15:
    x += 1
    print(x)


class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años")


persona = Persona("Juan", 25)
persona.saludar()
