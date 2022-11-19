import os
from tqdm import tqdm
from waterScene.waterScene import WaterScene
from waterScene.dataloader import DataLoader
from waterScene.visual import Visualization2D


if __name__ == '__main__':
    root_dir = "/media/reid/ext_disk1/waterscene_all"

    source_location = WaterScene(root_dir=root_dir,
                                    output_dir="/media/reid/ext_disk1/waterscene_all/projectionResult")

    eles = os.listdir(os.path.join(root_dir, "image"))
    eles = tqdm(eles)
    for ele in eles:
        nu = os.path.splitext(ele)[0]

        frame = DataLoader(frame_number=nu,
                           source_location=source_location)

        vis2d = Visualization2D(frame)
        vis2d.plot(show_labels=True, show_radar_label=True, show_radar=True, plot_figure=False, save_figure=True)