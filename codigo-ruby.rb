# Declaraciones de variables
x = 10
y = 20
z = 30

# Método
def add(a, b)
  a + b
end

# Condicionales
if x > y
  puts "x es mayor que y"
elsif x < y
  puts "x es menor que y"
else
  puts "x es igual a y"
end

# Bucles
for i in 0...10
  puts i
end

while x < 15
  x += 1
  puts x
end

# Clases
class Persona
  def initialize(nombre, edad)
    @nombre = nombre
    @edad = edad
  end

  def saludar
    puts "Hola, mi nombre es #{@nombre} y tengo #{@edad} años"
  end
end

persona = Persona.new("Juan", 25)
persona.saludar
