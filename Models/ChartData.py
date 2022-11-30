class ChartData:
    
    def __init__(self, page, y_name, x_name, data_points):
        """
        chart_type: enum | Type of the chart. Can beline, bar or circular
        y_name: str | Name of the column that was used for y values
        x_time: str | Name of the column that was used for x values, usually date column
        """
        
        self.page = page
        self.y_name = y_name
        self.x_name = x_name
        self.data_points = data_points