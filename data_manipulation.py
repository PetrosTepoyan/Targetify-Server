from flask import jsonify, request
import pandas as pd

# Our models
from DataPoint import *
from ChartData import *

class DataManipulation:

    def _subset(self, df, by_group):
        return df[df.group == by_group]

    def get_chart_data(self):

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

    def create_data_points(self):

        data_points = []

        for row in df.iterrows():
            
            row_data = row[1]
            
            point = DataPoint(
                x = int(datetime.timestamp(row_data["date"])),
                y = row_data["clicks"],
                label = None,
                group = row_data["group"]
            )
            
            data_points.append(point)

        data_points