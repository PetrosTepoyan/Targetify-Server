from flask import Flask, jsonify, request
import os
import data_manipulation

app = Flask(__name__, static_url_path='/static/')

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

@app.route("/chart_data")
def get_chart_data():
    print("no")
    return None, 497
    # json = request.get_json()
    # print(json)
    # page_name = json["page_name"]
    # group = json["group"]
    # column = json["column"]

    # if page_name:
    #     root_dir = _root_directory()
    #     page_dir = f"{root_dir}/static/{page_name}"
    # else:
    #     return None, 499

    # page = pd.read_csv(page_dir)

    # if group: 
    #     page_data = _subset(page_data, int(group))
    # else: 
    #     return None, 498

    # if column:
    #     return page_data[column], 200
    # else:
    #     return None, 497
    

def  _root_directory():
    app_dir = os.path.dirname(__file__)
    app_dir_list = app_dir.split(sep = "/")
    app_dir_list = app_dir_list[1:-1]
    root_dir = "/" + "/".join(app_dir_list)
    return root_dir



def _subset(df, by_group):
    return df[df.group == by_group]