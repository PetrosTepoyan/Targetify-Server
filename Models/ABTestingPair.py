class ABTestingPair:
    def __init__(self, group1Description, group2Description, meanDifference, pValue, reject, effectSize, powerSize):
        self.group1Description = group1Description
        self.group2Description = group2Description
        self.meanDifference = meanDifference
        self.pValue = pValue
        self.reject = reject
        self.effectSize = effectSize
        self.powerSize = powerSize