
import os
from tqdm import tqdm
from waterScene.waterScene import WaterScene


root_dir = "/media/reid/ext_disk1/dataset-1031"

flowsc = WaterScene(root_dir=root_dir)

frame = flowsc.loadFrame('1663308550.20094')

xx = frame.radar_data

frame1 = flowsc.loadFrame('1664092301.08607')
yy = frame1.radar_data