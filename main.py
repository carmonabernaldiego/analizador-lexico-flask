import re
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

reserved_words = {'for', 'do', 'while', 'if',
                  'int', 'else', 'printf', 'end', 'read'}
symbols = {';', '"', '+', '=', ',', '(', ')', '{', '}'}


def analyze_code(code):
    lines = code.split('\n')
    tokens = []

    for i, line in enumerate(lines, start=1):
        # Utilizar expresiones regulares para encontrar palabras y símbolos
        words = re.findall(r'\b\w+\b|[\(\){};"+=,]', line)
        for word in words:
            token = {
                'token': word,
                'linea': i,
                'reservada': 'x' if word in reserved_words else '',
                'simbolo': 'x' if word in symbols else '',
                'parentesis_izquierdo': 'x' if word == '(' else '',
                'parentesis_derecho': 'x' if word == ')' else '',
                'llave_izquierda': 'x' if word == '{' else '',
                'llave_derecha': 'x' if word == '}' else '',
                'numero': 'x' if word.isdigit() else '',
                'identificador': 'x' if word not in reserved_words and word not in symbols and not word.isdigit() else ''
            }
            tokens.append(token)

    return tokens


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return render_template('error.html', file_error="No se ha seleccionado ningún archivo")
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            with open(file_path, 'r') as f:
                code = f.read()
            tokens = analyze_code(code)
            return render_template('index.html', tokens=tokens, code=code)
        else:
            code = request.form['code']
            tokens = analyze_code(code)
            return render_template('index.html', tokens=tokens, code=code)
    return render_template('index.html', tokens=[], code='')


@app.route("/analyze", methods=['POST'])
def analyze():
    code = request.json['code']
    tokens = analyze_code(code)
    return jsonify({'tokens': tokens})


if __name__ == '__main__':
    app.run(debug=True)
