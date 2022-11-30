from flask import Flask, jsonify, request
import os
from tools import DataManipulation
import pandas as pd
import json

app = Flask(__name__, static_url_path='/static/')

dm = DataManipulation()

@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route("/pages")
def get_pages():
    root_dir = _root_directory()
    pages = os.listdir(f"{root_dir}/static/")
    
    return jsonify(pages), 200

@app.route("/page")
def get_page():

    page_name = request.args.get('name')
    root_dir = _root_directory()
    page = f"{root_dir}/static/{page_name}"
    return open(page, "r")

@app.route("/chart_data", methods = ["POST"])
def get_chart_data():

    print("Accepted", request)
    data = json.loads(request.stream.read(), strict=False)
    print(data)

    page_name = data["page"]
    chart_type = data["chart_type"]
    freq = data["freq"]
    column = data["column"]

    chart_data = dm.create_chart(
        page = page_name,
        freq = freq,
        column = column,
        group = None)
        
    return_json = json.dumps(chart_data, default = lambda x: x.__dict__)

    return return_json, 200

def  _root_directory():
    app_dir = os.path.dirname(__file__)
    app_dir_list = app_dir.split(sep = "/")
    app_dir_list = app_dir_list[1:-1]
    root_dir = "/" + "/".join(app_dir_list)
    return root_dir



def _subset(df, by_group):
    return df[df.group == by_group]