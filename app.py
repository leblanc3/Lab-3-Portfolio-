from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/contacts')
def contact():
    return render_template('contacts.html')

@app.route('/works/uppercase', methods=['GET','POST'])
def touppercase():
    original = None
    result = None
    if request.method == 'POST':
        text = request.form.get('inputString', '').strip()
        if text:
            result = text.upper()
            original = text
    return render_template('/works/touppercase.html', result=result, original=original)

@app.route('/works/circle', methods=['GET','POST'])
def area_circle():
    radius = None
    result = None
    if request.method == 'POST':
        raw = request.form.get('radius', '').strip()
        if raw:
            try:
                r = float(raw)
                if r < 0:
                    r = None
                else:
                    import math
                    result = 3.14 * r * r
                    radius = raw
            except ValueError:
                pass
    return render_template('/works/area_circle.html',result=result , radius=radius)

@app.route('/works/triangle', methods=['GET', 'POST'])
def area_triangle():
    base = None
    height = None
    result = None
    if request.method == 'POST':
        raw_base = request.form.get('base', '').strip()
        raw_height = request.form.get('height', '').strip()
        if raw_base and raw_height:
            try:
                b = float(raw_base)
                h = float(raw_height)
                if b >= 0 and h >= 0:
                    a = 0.5 * b * h
                    result = {
                        "base": round(b, 10),
                        "height": round(h, 10),
                        "area": round(a, 10),
                    }
                    base = raw_base
                    height = raw_height
            except ValueError:
                pass
    return render_template('/works/area_triangle.html', result=result, base=base, height=height)

@app.route('/works/infixconverter', methods=['GET', 'POST'])
def infix_converter():
    
    infix_expr = None
    postfix_result = None
    error = None
    
    if request.method == 'POST':
        try:
            postfix_result = infix_to_postfix(infix_expr)
        except Exception as e:
                error = f"Error: Invalid expression. {str(e)}"

    return render_template('/works/lab5.html', 
                         infix=infix_expr, 
                         postfix=postfix_result,
                         error=error)

def infix_to_postfix(expression):
    """Converts infix to postfix using Shunting Yard Algorithm."""
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    associativity = {'+': True, '-': True, '*': True, '/': True, '^': False}
    
    ops_stack = []
    output = []
    expression = expression.replace(' ', '')
    
    for token in expression:
        if token.isalnum():
            output.append(token)
        elif token == '(':
            ops_stack.append(token)
        elif token == ')':
            while ops_stack and ops_stack[-1] != '(':
                output.append(ops_stack.pop())
            if ops_stack:
                ops_stack.pop()
        elif token in precedence:
            while ops_stack and ops_stack[-1] != '(' and ops_stack[-1] in precedence:
                top_op = ops_stack[-1]
                if (associativity[token] and precedence[token] <= precedence[top_op]) or \
                   (not associativity[token] and precedence[token] < precedence[top_op]):
                    output.append(ops_stack.pop())
                else:
                    break
            ops_stack.append(token)
    
    while ops_stack:
        output.append(ops_stack.pop())
    
    return ''.join(output)

if __name__ == '__main__':
    app.run(debug=True)