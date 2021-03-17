import numpy as np
class Loss(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, img, gt):
        raise NotImplementedError

class MSELoss(Loss):
    def __call__(self, img, gt):
        return ((img-gt)**2).mean()

LOSSES = {}
LOSSES['colorization'] = [MSELoss('MSE')]

