from flask import Flask, jsonify, request
import os

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route("/pages")
def get_pages():
    root_dir = _root_directory()
    pages = os.listdir(f"{root_dir}/static/")
    return jsonify(pages)

@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return 'here is my text', 200

def  _root_directory():
    app_dir = os.path.dirname(__file__)
    app_dir_list = app_dir.split(sep = "/")
    app_dir_list = app_dir_list[1:-1]
    root_dir = "/" + "/".join(app_dir_list)
    return root_dir