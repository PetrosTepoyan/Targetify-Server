from flask import Flask, jsonify, request
import os
from tools import DataManipulation
import pandas as pd
import json
from Models.BFFABTestingModel import BFFABTestingModel

app = Flask(__name__, static_url_path='/static/')

testings_file = "static/active_testings.csv"

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

    data = json.loads(request.stream.read(), strict=False)

    title = data["title"]
    groups = data["groups"]
    page = data["page"]

    try:
        testings = pd.read_csv(testings_file, index_col = [0])
        testings.loc[len(testings)] = [len(testings), title, groups, page]
        testings.to_csv(testings_file)
    except:
        print("Couldn't open")
        title = data["title"]
        groups = data["groups"]
        page = data["page"]

        df = pd.DataFrame({"id" : [0], "title" : [title], "groups" : [groups], "page" : [page]})
        df.set_index("id")
        df.to_csv(testings_file)

    return "success", 200

@app.route("/active_testings")
def get_active_testings():
    try:
        testings = pd.read_csv(testings_file, index_col = [0])

        models = []

        for row in testings.iterrows():
            props = row[1]
            title = props["title"]
            groups = props["groups"]
            page = props["page"]
            models.append(BFFABTestingModel(title, groups, page))

        return_json = json.dumps(models, default = lambda x: x.__dict__)

        return return_json, 200
    except:
        return [], 200


def  _root_directory():
    app_dir = os.path.dirname(__file__)
    app_dir_list = app_dir.split(sep = "/")
    app_dir_list = app_dir_list[1:-1]
    root_dir = "/" + "/".join(app_dir_list)
    return root_dir



def _subset(df, by_group):
    return df[df.group == by_group]