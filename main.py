import re
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

python_reserved_words = {
    'for', 'while', 'if', 'else', 'print', 'def', 'import', 'from', 'return', 'and', 'or', 'not', 'class', 'try',
    'except', 'finally', 'raise', 'assert', 'with', 'yield', 'lambda', 'global', 'nonlocal', 'pass', 'break', 'continue', 'in', 'is', 'del',
    'async', 'await', 'None', 'True', 'False'
}

javascript_reserved_words = {
    'for', 'while', 'if', 'else', 'console', 'function', 'import', 'export', 'return', 'var', 'let', 'const', 'switch', 'case',
    'default', 'try', 'catch', 'finally', 'throw', 'class', 'extends', 'super', 'this', 'new', 'typeof', 'delete', 'async', 'await', 'instanceof', 'void',
    'do', 'in', 'of', 'continue', 'break', 'debugger', 'eval', 'with'
}

ruby_reserved_words = {
    'BEGIN', 'END', 'alias', 'and', 'begin', 'break', 'case', 'class', 'def', 'defined?', 'do', 'else', 'elsif', 'end', 'ensure',
    'false', 'for', 'if', 'in', 'module', 'next', 'nil', 'not', 'or', 'redo', 'rescue', 'retry', 'return', 'self', 'super', 'then',
    'true', 'undef', 'unless', 'until', 'when', 'while', 'yield'
}

symbols = {';', '"', '+', '=', ','}
identifiers = {'suma', 'a', 'b', 'c', 'la',
               'es', 'Diego Carmona Bernal', 'Code CBDX'}


def analyze_code(code):
    lines = code.split('\n')
    tokens = []
    counts = {
        'python_reserved_words': 0,
        'javascript_reserved_words': 0,
        'ruby_reserved_words': 0,
        'symbols': 0,
        'identifiers': 0,
        'numbers': 0,
        'left_paren': 0,
        'right_paren': 0,
        'left_brace': 0,
        'right_brace': 0,
        'lexical_errors': 0
    }

    for i, line in enumerate(lines, start=1):
        words = re.findall(r'\b\w+\b|[\(\){};"+=,]', line)
        for word in words:
            token = {
                'token': word,
                'line': i,
                'python_reserved': 'x' if word in python_reserved_words else '',
                'javascript_reserved': 'x' if word in javascript_reserved_words else '',
                'ruby_reserved_words': 'x' if word in ruby_reserved_words else '',
                'symbol': 'x' if word in symbols else '',
                'comma': 'x' if word == ',' else '',
                'semicolon': 'x' if word == ';' else '',
                'left_paren': 'x' if word == '(' else '',
                'right_paren': 'x' if word == ')' else '',
                'left_brace': 'x' if word == '{' else '',
                'right_brace': 'x' if word == '}' else '',
                'number': 'x' if word.isdigit() else '',
                'identifier': 'x' if word in identifiers else '',
                'lexical_error': 'x' if not any([word in python_reserved_words, word in javascript_reserved_words,
                                                 word in ruby_reserved_words, word in symbols,
                                                 word == '(', word == ')', word == '{', word == '}',
                                                 word.isdigit(), word in identifiers]) else ''
            }

            if token['python_reserved']:
                counts['python_reserved_words'] += 1
            if token['javascript_reserved']:
                counts['javascript_reserved_words'] += 1
            if token['ruby_reserved_words']:
                counts['ruby_reserved_words'] += 1
            if token['symbol']:
                counts['symbols'] += 1
            if token['identifier']:
                counts['identifiers'] += 1
            if token['number']:
                counts['numbers'] += 1
            if token['left_paren']:
                counts['left_paren'] += 1
            if token['right_paren']:
                counts['right_paren'] += 1
            if token['left_brace']:
                counts['left_brace'] += 1
            if token['right_brace']:
                counts['right_brace'] += 1
            if token['lexical_error']:
                counts['lexical_errors'] += 1

            tokens.append(token)

    return tokens, counts


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return render_template('index.html', tokens=[], counts={}, code='', file_error="No se ha seleccionado ningún archivo")
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            with open(file_path, 'r') as f:
                code = f.read()
            tokens, counts = analyze_code(code)
            return render_template('index.html', tokens=tokens, counts=counts, code=code)
        else:
            code = request.form['code']
            tokens, counts = analyze_code(code)
            return render_template('index.html', tokens=tokens, counts=counts, code=code)
    return render_template('index.html', tokens=[], counts={}, code='')


@app.route("/analyze", methods=['POST'])
def analyze():
    code = request.json['code']
    tokens, counts = analyze_code(code)
    return jsonify({'tokens': tokens, 'counts': counts})


if __name__ == '__main__':
    app.run(debug=True)
