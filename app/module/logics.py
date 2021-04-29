import numpy as np
import os
import config
from skimage.io import imread
from app.module.LOSSES import Metric
import zipfile
import matplotlib.pyplot as plt
import skimage.io as io
import numpy as np
from PIL import Image
import io
import config

class PreProcessor():
    @staticmethod
    def factory(image_type):
        if image_type == 'image':
            return ToImage()
        else:
            raise NotImplementedError

class ToImage(PreProcessor):
    def preprocess(self, raw, gt_path):
        img_bytes = io.BytesIO(bytearray(raw))
        gt_bytes = open(gt_path, 'rb')

        img = np.array(Image.open(img_bytes))
        gt = np.array(Image.open(gt_bytes))
        img = img[:, :, :3] / 255.
        gt = gt[:, :, :3] / 255.

        return img, gt

class LossProcessor():
    def __init__(self, task):
        self.loss_fns = [Metric.factory(l) for l in config.TASK_MODELS[task].losses]

    def calculate(self, img, gt):
        losses = {}
        for loss_fn in self.loss_fns:
            losses[loss_fn.name] = 0

        for loss_fn in self.loss_fns:
            losses[loss_fn.name] += loss_fn(img, gt)

        return losses

if __name__ == '__main__':
    pass
    # zipfile.ZipFile('../resources/Pictures.zip')
    # config.RESOURCE_PATH = "../resources"
    # LossProcessor('colorization', '../resources/task/task_input').calculate()
