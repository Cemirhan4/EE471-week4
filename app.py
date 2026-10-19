from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid JSON input'}), 400

    num1 = data.get('num1')
    operator = data.get('operator')
    num2 = data.get('num2')

    # Validate inputs
    if num1 is None or num2 is None or operator is None:
        return jsonify({'error': 'Missing fields: num1, operator, num2 are required'}), 400

    try:
        num1 = float(num1)
        num2 = float(num2)
    except (ValueError, TypeError):
        return jsonify({'error': 'num1 and num2 must be numbers'}), 400

    # Perform calculation
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*' or operator == 'x' or operator == '×':
        result = num1 * num2
    elif operator == '/' or operator == '÷':
        if num2 == 0:
            return jsonify({'error': 'Division by zero is not allowed'}), 400
        result = num1 / num2
    else:
        return jsonify({'error': f'Invalid operator: {operator}'}), 400

    # Return integer if result is whole number
    if result == int(result):
        result = int(result)

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
