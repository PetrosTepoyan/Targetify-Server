from flask import Flask, jsonify, request

app = Flask(__name__, static_url_path='/static')

@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return 'here is my text', 200

@app.route('/ab_testing', method = ['POST'])