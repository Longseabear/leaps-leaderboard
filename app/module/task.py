import time
import uw
import zipfile
import matplotlib.pyplot as plt
import skimage.io as io
import numpy as np
from PIL import Image
import io
#from app.module.logics import

class ImageTask():
    def __init__(self, task_name, ):
        self.task_name = task_name
        self.byte_zip = None

def threaded_task(duration):
    for i in range(duration):
        print("Working... {}/{}".format(i + 1, duration))
        time.sleep(1)

@thread
def uwsgi_task(duration):
    for i in range(duration):
        print("Working in uwsgi thread... {}/{}".format(i + 1, duration))
        time.sleep(1)

if __name__ == '__main__':
    pass