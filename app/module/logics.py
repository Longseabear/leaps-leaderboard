import numpy as np
import os
import config
from skimage.io import imread
from app.module.LOSSES import LOSSES, Loss

config.RESOURCE_PATH = "../resources"
class LossProcessor():
    def __init__(self, task, src_paths, user=None):
        self.gt_path = os.path.join(config.RESOURCE_PATH, 'task', task)
        self.img_path = src_paths

        self.gts = [os.path.join(self.gt_path, i) for i in os.listdir(self.gt_path)]
        self.imgs = [os.path.join(self.img_path, i) for i in os.listdir(self.img_path)]

        self.gts = sorted(self.gts)
        self.imgs = sorted(self.imgs)

        self.loss_fns = LOSSES[task]

    def calculate(self):
        if len(self.imgs) != len(self.gts):
            raise Exception('')

        sets = {}
        for loss_fn in self.loss_fns:
            sets[loss_fn.name] = 0
        for img_path, gt_path in zip(self.imgs, self.gts):
            img = imread(img_path) / 255.
            gt = imread(gt_path) / 255.

            for loss_fn in self.loss_fns:
                 sets[loss_fn.name] += loss_fn(img, gt)
        for loss_fn in self.loss_fns:
            sets[loss_fn.name] /= len(self.imgs)
        print(sets)

LossProcessor('colorization', '../resources/task/task_input').calculate()
