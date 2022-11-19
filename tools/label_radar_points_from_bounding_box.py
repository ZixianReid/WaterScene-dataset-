from waterScene.waterScene import WaterScene
import numpy as np
from waterScene.transformation import project_pcl_to_image
import os
from waterScene import commonutils
import matplotlib.pyplot as plt
import pandas as pd
from waterScene import settings
from tqdm import tqdm
from generate_kitti_label_format import ImageLabel


label_code_str = {"pier": 999,
                  "buoy": 999,
                  "ship": 999,
                  "boat": 999,
                  "vessel": 999}


def filter_radar(x1, y1, x2, y2, uvs, radar, label, threshold):
    """
    filter radar data based on image box and radar depth
    :param label:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param uvs:
    :param radar:
    :param threshold: threshold for tolerate image box bias
    """

    depth_threshold = label_code_str[label]
    idx = uvs[:, 0] > 0
    idx = np.logical_and(idx, uvs[:, 0] >= x1 - threshold)
    idx = np.logical_and(idx, uvs[:, 0] <= x2 + threshold)
    idx = np.logical_and(idx, uvs[:, 1] <= y1 + threshold)
    idx = np.logical_and(idx, uvs[:, 1] >= y2 - threshold)

    # filter radar data based on radar depth
    radar_filter = radar[idx]
    if radar_filter.shape[0] > 0:
        radar_min_depth = radar_filter[:, 2].min()

        idx = np.logical_and(idx, radar[:, 2] >= radar_min_depth)
        idx = np.logical_and(idx, radar[:, 2] <= radar_min_depth + depth_threshold)

    label_number = int(settings.label_code_str[label])

    # output = idx + 0
    # output = output * (label_number + 1)
    # output = output - 1
    index = np.argwhere(idx == True).flatten()
    radar[index, -1] = label_number


class RadarLabeler:
    def __init__(self, name_prefix, source_location, label_dict):
        self.source_location = source_location
        self.image_path = os.path.join(source_location, 'image', name_prefix + ".jpg")

        self.radar_path = os.path.join(source_location, 'radar', name_prefix + ".csv")
        self.label_dict = label_dict
        self.t_camera_lidar, self.camera_projection_matrix = commonutils.loadCailbMatrix(
            os.path.join(source_location, 'calib', name_prefix + ".txt")
        )

    @property
    def image_shape(self):
        return self.__get_image_data().shape

    def __get_image_data(self):
        """

        :return:
        """
        return plt.imread(self.image_path)

    def get_radar_data(self):
        """
        read uvs, change abs_velocity
        :return:
        """
        radar_source = pd.read_csv(self.radar_path, dtype=np.float32)

        radar = radar_source[['z', '']]
        uvs = radar_source[['u', 'v']].to_numpy(dtype=np.int64)

        return uvs, radar

    def label_data(self):
        """

        :return:
        """
        uvs, radar = self.get_radar_data()

        for img_label in self.label_dict:
            filter_radar(img_label['xmin'], img_label['ymax'], img_label['xmax']
                         , img_label['ymin'], uvs, radar
                         , img_label['class'],
                         threshold=10)
        return radar

    def build(self):
        return self.label_data()


if __name__ == '__main__':
    data_root = "/media/reid/ext_disk1/all"
    eles = os.listdir(os.path.join(data_root, "image"))
    flowsc = WaterScene(root_dir=data_root)
    eles = tqdm(eles)
    for ele in eles:
        nu = os.path.splitext(ele)[0]
        label_path = os.path.join(data_root, "label", str(nu) + '.xml')
        imageLabeler = ImageLabel(label_path)
        radarLabeler = RadarLabeler(nu, data_root, imageLabeler.label_dict)
        radar = radarLabeler.build()
