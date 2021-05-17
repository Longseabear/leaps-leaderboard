import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
class Metric(object):
    def __init__(self, name):
        self.name = name
        self.is_loss = True # if false, this is distance,

    def __call__(self, img, gt):
        raise NotImplementedError

    @staticmethod
    def factory(type):
        if type == "MSEMetric":
            return MSEMetric('MSEMetric')
        elif type == "L1Metric":
            return L1Metric('L1Metric')
        elif type == "PSNRMetric":
            return PSNRMetric('PSNRMetric')
        elif type=="SSIMMetric":
            return SSIMMetric('SSIMMetric')
        else:
            raise NotImplementedError

class MSEMetric(Metric):
    def __call__(self, img, gt):
        return ((img-gt)**2).mean()

class L1Metric(Metric):
    def __call__(self, img, gt):
        return np.abs(img-gt).mean()

class PSNRMetric(Metric):
    def __call__(self, img, gt):
        # img, gt is float
        return peak_signal_noise_ratio(gt, img, data_range=1.0)

class SSIMMetric(Metric):
    def __call__(self, img, gt):
        # img, gt is float
        return structural_similarity(gt, img, multichannel=True)

if __name__ == '__main__':
    gt = np.random.rand(11,11)
    pred = gt + np.random.normal(0, 0.1,(11,11))
    print(pred, gt)
    print(SSIMMetric('SSIM')(pred, gt))
