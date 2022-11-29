from flask import jsonify, request
import pandas as pd
from datetime import datetime as dt

# Our models
from Models.DataPoint import DataPoint
from Models.ChartData import ChartData


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
        self.df = df
        self.by_group = by_group

        self.df = self.df[self.df.group == self.by_group]

        return self.df

    def get_chart_data(self, df, column, group=None):

        # json = request.get_json()
        # page_name = json["page_name"]
        # group = json["group"]
        # column = json["column"]

        # if page_name:
        #    root_dir = _root_directory()
        #    page_dir = f"{root_dir}/static/{page_name}"
        # else:
        #    return None, 499

        # page_data = pd.read_csv(page_dir)

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
        self.df = df
        self.column = column
        self.group = group

        if self.group or self.group == 0:
            self.df = self._subset(self.df, int(self.group))
            if self.column:
                self.df = self.df[["date", self.column, "group"]]
                return self.df
            else:
                return None, 498

        else:
            if self.column:
                self.df = self.df[["date", self.column]]
                return self.df
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
        self.df = df
        self.freq = freq
        self.column = column
        self.group = group

        self.df = self.get_chart_data(self.df, self.column, self.group)

        dates = pd.to_datetime(self.df.date, format='%Y-%m-%d %H:%M:%S')
        self.df = (self.df.assign(date=dates)
                   .groupby([self.column, pd.Grouper(key='date', freq=self.freq)])
                   .sum()
                   .reset_index())

        return self.df

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
        self.df = df
        self.freq = freq
        self.column = column
        self.group = group

        self.df = self.get_data_with_frequency(self.df, self.freq, self.column, self.group)

        data_points = []

        for row in self.df.iterrows():
            row_data = row[1]

            point = DataPoint(
                x=int(dt.timestamp(row_data["date"])),
                y=row_data[self.column],
                label=None,
                group=self.group
            )

            data_points.append(point)

        return data_points

    def create_chart(self, df, freq, column, chart_type, group=None):
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
        self.df = df
        self.freq = freq
        self.column = column
        self.chart_type = chart_type
        self.group = group

        self.data_points = self.create_data_points(self.df, self.freq, self.column, self.group)

        chart = ChartData(
            chart_type=self.chart_type,
            y_name=self.column,
            x_name="date",
            data_points=self.data_points
        )

        return chart
