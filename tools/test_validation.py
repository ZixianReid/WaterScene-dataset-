import argparse
from waterScene.waterScene import WaterScene
from waterScene.visual import Visualization2D

parser = argparse.ArgumentParser()
parser.add_argument('--data_root', type=str, default="/media/reid/ext_disk1/waterscene_all")

args = parser.parse_args()

root_dir = args.data_root

flowsc = WaterScene(root_dir=root_dir)
frame = flowsc.loadFrame('1664091257.87023')

vis2d = Visualization2D(frame)

vis2d.plot(show_labels=True, show_radar_label=True, show_radar=True)
