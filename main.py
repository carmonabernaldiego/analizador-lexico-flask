import re
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

identifiers = {'a', 'b', 'c', 'la', 'suma', 'es'}
reserved_words = {'for', 'do', 'while', 'if', 'int',
                  'else', 'print', 'end', 'read', 'programa'}
symbols = {';', '"', '+', '=', ',', '(', ')', '{', '}'}


def analyze_code(code):
    lines = code.split('\n')
    tokens = []
    errors = []

    for i, line in enumerate(lines, start=1):
        words = re.findall(r'\b\w+\b|[\(\){};"+=,]', line)
        for word in words:
            if word in reserved_words:
                reserved = 'x'
            else:
                reserved = ''
            if word not in reserved_words and word not in symbols and not word.isdigit() and word not in identifiers:
                errors.append({'token': word, 'line': i})
            token = {
                'token': word,
                'line': i,
                'reserved': reserved,
                'symbol': 'x' if word in symbols else '',
                'comma': 'x' if word == ',' else '',
                'semicolon': 'x' if word == ';' else '',
                'left_paren': 'x' if word == '(' else '',
                'right_paren': 'x' if word == ')' else '',
                'left_brace': 'x' if word == '{' else '',
                'right_brace': 'x' if word == '}' else '',
                'number': 'x' if word.isdigit() else '',
                'identifier': 'x' if word in identifiers else '',
            }
            tokens.append(token)

    total_counts = {key: sum(
        1 for token in tokens if token[key] == 'x') for key in tokens[0].keys() if key != 'token'}
    tokens.append(total_counts)

    return tokens, errors


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
            tokens, errors = analyze_code(code)
            return render_template('index.html', tokens=tokens, errors=errors, code=code)
        else:
            code = request.form['code']
            tokens, errors = analyze_code(code)
            return render_template('index.html', tokens=tokens, errors=errors, code=code)
    return render_template('index.html', tokens=[], errors=[], code='')


@app.route("/analyze", methods=['POST'])
def analyze():
    code = request.json['code']
    tokens, errors = analyze_code(code)
    return jsonify({'tokens': tokens, 'errors': errors})


if __name__ == '__main__':
    app.run(debug=True)
