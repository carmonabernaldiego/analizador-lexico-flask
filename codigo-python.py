
# Declaraciones de variables
x = 10
y = 20
z = 30

# Función
def add(a, b):
    return a + b

# Condicionales
if x > y:
    print("x es mayor que y")
elif x < y:
    print("x es menor que y")
else:
    print("x es igual a y")

# Bucles
for i in range(10):
    print(i)

while x < 15:
    x += 1
    print(x)

# Clases
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print(f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años")

persona = Persona("Juan", 25)
persona.saludar()
