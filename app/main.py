from flask import Flask, jsonify, request
import os
from tools import DataManipulation
import pandas as pd
import json

app = Flask(__name__, static_url_path='/static/')

@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route("/pages")
def get_pages():
    root_dir = _root_directory()
    pages = os.listdir(f"{root_dir}/static/pages")
    
    return jsonify(pages), 200

@app.route("/page")
def get_page():

    page_name = request.args.get('name')
    root_dir = _root_directory()
    page = f"{root_dir}/static/{page_name}"
    return open(page, "r")

@app.route("/chart_data", methods = ["POST"])
def get_chart_data():

    dm = DataManipulation()

    data = json.loads(request.stream.read(), strict=False)

    page_name = data["page"]
    chart_type = data["chart_type"]
    freq = data["freq"]
    column = data["column"]
    ## passing groups concatenated: "0123"
    try:
        groups = data["groups"]
    except:
        groups = None
    # group.split()

    chart_data = dm.create_chart(
        page = page_name,
        freq = freq,
        column = column,
        groups = groups)
        
    return_json = json.dumps(chart_data, default = lambda x: x.__dict__)

    return return_json, 200

@app.route("/pages_info")
def get_pages_info():

    dm = DataManipulation()

    pageVersions = dm.get_pages_info()
    return_json = json.dumps(pageVersions, default = lambda x: x.__dict__)

    return return_json, 200

@app.route("/create_ab_testing", methods = ["POST"])
def create_ab_testing():
    print("FDF", os.listdir())
    data = json.loads(request.stream.read(), strict=False)
    groups = data["groups"]

    with open("static/active_testings.txt", "r") as f:
        ex = f.readlines()

    with open("static/active_testings.txt", "w") as f:
        if ex == "":
            f.write(f"{groups}")
        else:
            f.write(f"{ex},{groups}")

    return "success", 200

@app.route("/active_testings")
def get_active_testings():
    with open('static/active_testings.txt') as f:
        lines = f.readlines()
    if lines:
        groups = lines[0].split(",")
        return groups
    else:
        return "", 200



def  _root_directory():
    app_dir = os.path.dirname(__file__)
    app_dir_list = app_dir.split(sep = "/")
    app_dir_list = app_dir_list[1:-1]
    root_dir = "/" + "/".join(app_dir_list)
    return root_dir



def _subset(df, by_group):
    return df[df.group == by_group]