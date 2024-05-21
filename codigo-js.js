// Declaraciones de variables
var x = 10;
let y = 20;
const z = 30;

// Función
function add(a, b) {
    return a + b;
}

// Condicionales
if (x > y) {
    console.log("x es mayor que y");
} else if (x < y) {
    console.log("x es menor que y");
} else {
    console.log("x es igual a y");
}

// Bucles
for (let i = 0; i < 10; i++) {
    console.log(i);
}

while (x < 15) {
    x++;
    console.log(x);
}

// Clases
class Persona {
    constructor(nombre, edad) {
        this.nombre = nombre;
        this.edad = edad;
    }

    saludar() {
        console.log(`Hola, mi nombre es ${this.nombre} y tengo ${this.edad} años`);
    }
}

const persona = new Persona("Juan", 25);
persona.saludar();
