from matplotlib import pyplot as plt
import os
import logging
import numpy as np
from .transformation import project_pcl_to_image
from . import helper
from . import settings


class Visualization2D:
    def __init__(self, dataloader):
        self.dataloader = dataloader
        self.image_copy = self.dataloader.image

    def plot(self, plot_figure=True,
             save_figure=False,
             show_labels=False,
             show_radar=False,
             show_radar_label=False):
        fig = plt.figure(figsize=(19.2, 10.8))
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        plt.clf()
        fig.set_dpi(100)

        if show_labels:
            self.plot_gt_labels()

        if show_radar:
            self.plot_radar_pcl()

        if show_radar_label:
            self.plot_radar_label()
        plt.imshow(self.image_copy, alpha=1)
        plt.axis('off')

        if save_figure:
            plt.savefig(self.dataloader.source_location.output_dir + f'/{self.dataloader.frame_number}.png',
                        bbox_inches='tight', transparent=True)

        if plot_figure:
            plt.show()

        plt.close(fig)

        return

    def plot_gt_labels(self):
        gtLabels = self.dataloader.label_data.label_dict
        for gtLable in gtLabels:
            helper.plot_boxes([gtLable['xmin'], gtLable['ymax'], gtLable['xmax'], gtLable['ymin']],
                              settings.label_color_palette_2d[gtLable['class']])

    def plot_radar_pcl(self):
        uvs, points_depth, power, _ = project_pcl_to_image(self.dataloader.radar_data,
                                                           self.dataloader.t_camera_lidar,
                                                           self.dataloader.camera_projection_matrix,
                                                           self.dataloader.image.shape)

        plt.scatter(uvs[:, 0], uvs[:, 1], c=-points_depth, alpha=0.8, cmap='jet')
        # for i in range(uvs.shape[0]):
        #     plt.annotate(text=int(points_depth[i]), xy=(uvs[i, 0], uvs[i, 1]))

    def plot_radar_label(self):
        uvs, points_depth, power, radar = project_pcl_to_image(self.dataloader.radar_data,
                                                               self.dataloader.t_camera_lidar,
                                                               self.dataloader.camera_projection_matrix,
                                                               self.dataloader.image.shape)
        idx = radar[:, -1] != -1
        radar = radar[idx]
        uvs = uvs[idx]
        plt.scatter(uvs[:, 0], uvs[:, 1], alpha=0.8, cmap='jet', marker="*")
