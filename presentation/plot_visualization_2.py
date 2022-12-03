import os
from tqdm import tqdm
from waterScene.waterScene import WaterScene
from waterScene.dataloader import DataLoader
from waterScene.visual import Visualization2D



root_dir = "/media/reid/ext_disk1/waterscene_all"

flowsc = WaterScene(root_dir)
sample = '1665121227.45964'
frame = flowsc.loadFrame(sample)
vis2d = Visualization2D(frame)
vis2d.plot(show_labels=False, show_radar_label=False, show_radar=False, plot_figure=True, save_figure=False)

vis2d.plot(show_labels=True, show_radar_label=False, show_radar=False, plot_figure=True, save_figure=False)

vis2d.plot(show_labels=True, show_radar_label=True, show_radar=True, plot_figure=True, save_figure=False)