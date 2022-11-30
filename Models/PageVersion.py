class PageVersion:
    
    def __init__(self, version, code):
        self.version = version
        self.code = code
        
    def __repr__(self):
        return f"PageVersion({self.version} | {self.code})"