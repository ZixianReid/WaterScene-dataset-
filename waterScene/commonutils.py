import datetime
import os
import shutil
import logging
import numpy as np


class log(object):
    def __init__(self, log_dir):
        logging.basicConfig(filename=log_dir,
                            format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S ',
                            level=logging.INFO)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.INFO)

    @property
    def logger(self):
        logger = logging.getLogger(__name__)
        logger.addHandler(self.stream_handler)
        return logger


def timeShift(originTime, shiftHours):
    return originTime + datetime.timedelta(hours=shiftHours)


# def timestamp2Format(originTime, format):
#     return originTime.dt.strftime(format)


# def setDir(filePath, fileName):
#
#     if not os.path.exists(filePath):
#         os.mkdir(filePath)
#     return os.path.join(filePath, fileName)

def mkDataDirs(out_location, fold_name):
    path = os.path.join(out_location, fold_name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def numpy2Bin(array, locations):
    array.tofile(locations)


def loadCailbMatrix(location):
    with open(location, "r") as f:
        lines = f.readlines()
        extrinsic_matrix = np.array(lines[0].strip().split(' ')[1:], dtype=np.float32).reshape(4, 4)
        intrinsic_matrix = np.array(lines[1].strip().split(' ')[1:], dtype=np.float32).reshape(3, 4)
        return extrinsic_matrix, intrinsic_matrix


def convert_currency(value):
    """
    转换字符串数字为float类型
     - 移除 ￥ ,
     - 转化为float类型
    """
    try:
        return np.float(value)
    except ValueError as e:
        print(e)
        return np.float(0)
