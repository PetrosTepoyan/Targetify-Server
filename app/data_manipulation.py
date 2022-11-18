from flask import jsonify, request
import pandas as pd

def _subset(df, by_group):
    return df[df.group == by_group]

def get_chart_data():

    json = request.get_json()
    page_name = json["page_name"]
    group = json["group"]
    column = json["column"]

    if page_name:
        root_dir = _root_directory()
        page_dir = f"{root_dir}/static/{page_name}"
    else:
        return None, 499

    page = pd.read_csv(page_dir)

    if group: 
        page_data = _subset(page_data, int(group))
    else: 
        return None, 498

    if column:
        return page_data[column], 200
    else:
        return None, 497

