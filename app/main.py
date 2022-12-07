from flask import Flask, jsonify, request
import os
from tools import DataManipulation
import pandas as pd
import json
from Models.BFFABTestingModel import BFFABTestingModel
import simplejson
from abtesting import Multivar_AB_Testing
from Models.ABTestingPair import ABTestingPair

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
        
    return_json = __to_json(chart_data)
    return return_json, 200

@app.route("/pages_info")
def get_pages_info():

    dm = DataManipulation()

    pageVersions = dm.get_pages_info()
    return_json = __to_json(pageVersions)

    return return_json, 200

@app.route("/create_ab_testing", methods = ["POST"])
def create_ab_testing():

    data = json.loads(request.stream.read(), strict=False)

    title = data["title"]
    groups = data["groups"]
    page = data["page"]
    print(data)
    try:
        testings = pd.read_csv(testings_file, index_col = [0])
        testings.loc[len(testings)] = [len(testings), title, groups, page]
        testings.to_csv(testings_file)
    except:
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

        models_ = []

        for row in testings.iterrows():
            props = row[1]
            title = props["title"]
            groups = props["groups"]
            page = props["page"]
            models_.append(BFFABTestingModel(title, groups, page))

        return_json = __to_json(models_)

        return return_json, 200
    except:
        return [], 200

@app.route("/delete_testing", methods = ["POST"])
def delete_testing():

    data = json.loads(request.stream.read(), strict=False)
    id = int(data["id"])

    testings = pd.read_csv(testings_file, index_col = [0])
    try:
        testings.drop([id], axis=0, inplace=True)
        testings.to_csv(testings_file)
    except:
        return "success", 200

    return "success", 200

@app.route("/get_statistic", methods = ["POST"])
def get_statistic():
    data = json.loads(request.stream.read(), strict=False)
    page = data["page"]
    groups = data["groups"]
    df = pd.read_csv(f"static/pages/{page}")
    page_name = page.split(sep="_")[1][:-5]

    t_df = Multivar_AB_Testing(df, page_name, "group", "clicks")

    t_df = t_df[[e in groups for e in t_df["group1"]]]
    t_df = t_df[[e in groups for e in t_df["group2"]]]
    print(data)
    print(t_df)
    if groups != "":
        t_df = t_df[["group1.codes", "group2.codes", "meandiff", "p-adj", "reject", "effect_size", "power_size"]]
        models_ = []

        for row in t_df.iterrows():
            props = row[1]
            group1 = props["group1.codes"]
            group2 = props["group2.codes"]
            meandiff = props["meandiff"]
            padj = props["p-adj"]
            reject = props["reject"]
            effectSize = props["effect_size"]
            powerSize = props["power_size"]
            pair = ABTestingPair(group1, group2, meandiff, padj, reject, effectSize, powerSize)
            models_.append(pair)

        return_json = __to_json(models_)

        return return_json, 200
    else:
        return {}, 400

def  _root_directory():
    app_dir = os.path.dirname(__file__)
    app_dir_list = app_dir.split(sep = "/")
    app_dir_list = app_dir_list[1:-1]
    root_dir = "/" + "/".join(app_dir_list)
    return root_dir

def __to_json(object):
    return simplejson.dumps(object, ignore_nan=True, default = lambda x: x.__dict__)
    # return json.dumps(object, default = lambda x: x.__dict__, indent = 4, allow_nan = False)


def _subset(df, by_group):
    return df[df.group == by_group]