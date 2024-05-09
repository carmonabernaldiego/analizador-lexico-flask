from flask import Flask, request, render_template, jsonify
import os
import ply.lex as lex

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Definición de tokens y analizador léxico
reserved = {
    'for': 'FOR',
    'if': 'IF',
    'do': 'DO',
    'while': 'WHILE',
    'else': 'ELSE',
}

tokens = list(reserved.values()) + \
    ['IDENTIFIER', 'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'ARROBA']


def t_LBRACE(t):
    r'\{'
    return t


def t_RBRACE(t):
    r'\}'
    return t


def t_LPAREN(t):
    r'\('
    return t


def t_RPAREN(t):
    r'\)'
    return t


def t_ARROBA(t):
    r'\@@@'
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


t_ignore = ' \t'


def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('error.html', file_error="No se ha enviado ningún archivo")

        file = request.files['file']

        if file.filename == '':
            return render_template('error.html', file_error="No se ha seleccionado ningún archivo")

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Leer el contenido del archivo y mostrarlo en el área de texto
        with open(file_path, 'r') as f:
            file_content = f.read()

        return render_template('index.html', file_content=file_content)

    return render_template('index.html')


@app.route("/analyze", methods=['POST'])
def analyze_code():
    try:
        code = request.json['code']
        # Restaurar saltos de línea antes de analizar el código
        lexer.input(code)
        tokens = []
        current_line = 1  # Inicializar la línea actual
        for tok in lexer:
            token_info = {
                'lexpos': tok.lexpos,
                'lineno': current_line,  # Utilizar la línea actual
                'type': tok.type,
                'value': tok.value
            }
            if tok.type == 'LPAREN':
                token_info['description'] = "Paréntesis de apertura"
            elif tok.type == 'RPAREN':
                token_info['description'] = "Paréntesis de cierre"
            elif tok.type == 'LBRACE':
                token_info['description'] = "Llave de apertura"
            elif tok.type == 'RBRACE':
                token_info['description'] = "Llave de cierre"
            elif tok.type in reserved.values():
                token_info['description'] = f"Reservada {tok.value.capitalize()}"
            else:
                token_info['description'] = "Identificador"
             # Actualizar la línea actual si se encuentra un salto de línea
            current_line += code.count('@@@', tok.lexpos,
                                       tok.lexpos + len(tok.value))

            if tok.value != '@@@':
                tokens.append(token_info)
        return jsonify({'tokens': tokens})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
