import numpy as np

class ComplexNumber:
    def __init__(self, val, weight= 1):
        self.val = val
        self.weight = weight

    def __getitem__(self, i):
        if self.val[i] == b'0':
            return  np.complex(0, -self.weight)
        else:
            return  np.complex(0, self.weight)
    

class RealNumber:
    def __init__(self, val, weight = 1):
        self.val = val
        self.weight = weight

    def __getitem__(self, i):
        if self.val[i] == b'0':
            return -self.weight 
        else:
            return self.weight 
