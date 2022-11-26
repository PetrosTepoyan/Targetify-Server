class DataPoint:
    
    def __init__(self, x = None, y, label = None, group = None):
        """
            x: int/float, x value, can be None
            y: int/float, y value
            label: str, label of the point, can be None
            group: str, group (A/B), can be None 
        """
        self.x = x
        self.y = y
        self.label = label
        self.group = group
        
    def __repr__(self):
        return f"DataPoint(x = {self.x}, y = {self.y}, group = {self.group})"