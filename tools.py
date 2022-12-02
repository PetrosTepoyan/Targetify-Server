from flask import jsonify, request
import pandas as pd
from datetime import datetime as dt
import calendar

# Our models
from Models.DataPoint import DataPoint
from Models.ChartData import ChartData
from Models.PageVersion import PageVersion

import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)


class DataManipulation:
    
    def _subset(self, df, by_group):
        """
        A function used to subset a dataframe by a given group
        
        Attributes
        ------------
        df: dataframe | The dataframe that we want to subset
        by_group: int | The group that is used for subsetting (0,1,...,9)
        
        Returns
        ------------
        The given dataframe subsetted by the given group
        """
        df = df
        by_group = by_group
    
        df = df[df.group == by_group]
        
        return df

    def get_chart_data(self, df, column, group=None):
        
        #json = request.get_json()
        #page_name = json["page_name"]
        #group = json["group"]
        #column = json["column"]
        
        #if page_name:
        #    root_dir = _root_directory()
        #    page_dir = f"{root_dir}/static/{page_name}"
        #else:
        #    return None, 499

        #page_data = pd.read_csv(page_dir)
        
        """
        A function used to get the data needed for creating the chart
        
        Attributes
        ------------
        df: dataframe | The dataset for the given page
        column: str | The column used for y values
        group: int | The given group that is used for subsetting (0,1,...,9), can be None
        
        Returns
        ------------
        A dataframe containing the column values, date and group (if given)
        """
        df = df
        column = column
        group = group
        
        if group or group==0:
            df = self._subset(df, int(group))
            if column:
                df = df[["date", column, "group"]]
                return df
            else:
                return None, 498
        
        else:
            if column:
                df = df[["date", column]]
                return df
            else:
                return None, 497
        
    def get_data_with_frequency(self, df, freq, column, group=None):
        """
        A function used to aggregate the data by the given column and time period
        
        Attributes
        ------------
        df: dataframe | The dataset for the given page
        freq: str | The time period used for aggregating the data ("1H", "2H", ..., "1D", "1W", "1M")
        column: str | The column used for y values
        group: int | The given group that is used for subsetting (0,1,...,9), can be None
        
        Returns
        ------------
        The aggregated dataframe containing the column values, date and group (if given)
        """
            
        df = self.get_chart_data(df, column, group)
        dates =  pd.to_datetime(df.date, format='%Y-%m-%d %H:%M:%S')
        df.date = dates
        df["index"] = pd.DatetimeIndex(dates)
        df = df.set_index("index")
        df = df.sort_values("index")
        
        isStringType = df.dtypes[column] == "object"
        if isStringType:
            series = df.groupby(pd.Grouper(key = column)).count()["date"]
        else:
            series = df.groupby(pd.Grouper(key = 'date', freq = freq)).mean()[column]
            series.index = pd.DatetimeIndex(series.index)
            months = [int(i) for i in series.index.strftime('%m')]
            formatted_index = [calendar.month_abbr[month] for month in months]
            series.index = formatted_index

        return series
    
    def create_data_points(self, df, freq, column, group=None):
        """
        A function used to create data points from the given dataframe
        
        Attributes
        ------------
        df: dataframe | The dataset for the given page
        freq: str | The time period used for aggregating the data ("1H", "2H", ..., "1D", "1W", "1M")
        column: str | The column used for y values
        group: int | The given group that is used for subsetting (0,1,...,9), can be None
        
        Returns
        ------------
        A list of DataPoint objects
        """
        df = df
        freq = freq
        column = column
        group = group
        
        series = self.get_data_with_frequency(df, freq, column, group)
        
        data_points = []
        
        for ind, element in enumerate(series):
            
            try:
                x = int(dt.timestamp(series.index[ind]))
            except:
                x = None
                
            y = float(series[ind])
            label = str(series.index[ind])
            group = group
            
            point = DataPoint(
                x = x,
                y = y,
                label = label,
                group = group
            )
            
            data_points.append(point)

        return data_points
    
    def create_chart(self, page, freq, column, groups = None):
        """
        A function used to create a ChartData object from a given dataframe
        
        Attributes
        ------------
        df: dataframe | The dataset for the given page
        freq: str | The time period used for aggregating the data ("1H", "2H", ..., "1D", "1W", "1M")
        column: str | The column used for y values
        chart_type: enum | Type of the chart. Can be line, bar or circular
        group: int | The given group that is used for subsetting (0,1,...,9), can be None
        
        Returns
        ------------
        A ChartData object
        """
        
        df = pd.read_csv(f"static/pages/{page}")
        freq = freq
        column = column

        if groups:

            data_points_list = []

            for group in groups:
                data_points = self.create_data_points(df, freq, column, group)
                data_points_list = data_points_list + data_points

            chart = ChartData(
                page = page,
                y_name = column,
                x_name = "date",
                data_points = data_points_list
            )

            return chart

        else:
            data_points = self.create_data_points(df, freq, column, groups)
            
            chart = ChartData(
                page = page,
                y_name = column,
                x_name = "date",
                data_points = data_points
            )
            
            return chart

    def get_pages_info(self):
        df_info = pd.read_csv("static/pages_info.csv")
        pageVersions = [PageVersion(row[1]["page_name"], row[1]["code"], row[1]["description"]) for row in df_info.iterrows()]
        return pageVersions

    