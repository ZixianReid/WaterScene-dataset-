
import os
from tqdm import tqdm
from waterScene.waterScene import WaterScene


root_dir = "/media/reid/ext_disk1/all"

flowsc = WaterScene(root_dir=root_dir)

frame = flowsc.loadFrame('1664091257.87023')

xx = frame.radar_data

frame1 = flowsc.loadFrame('1664091257.87023')
yy = frame1.radar_data
