import numpy as np

class ComplexNumber:
    def __init__(self, val, weight= 1):
        self.val = val
        self.weight = weight

    def __getitem__(self, i):
        return  np.complex(0, self.weight * self.val[i])
    

class RealNumber:
    def __init__(self, val, weight =1):
        self.val = val
        self.weight = weight

    def __getitem__(self, i):
        return self.weight * self.val[i]
