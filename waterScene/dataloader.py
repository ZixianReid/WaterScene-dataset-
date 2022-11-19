import pandas
from matplotlib import pyplot as plt
import os
import logging
import numpy as np
from .labels import FrameLabels
import pandas as pd

class DataLoader:
    def __init__(self, frame_number, source_location):
        self.source_location = source_location
        self.frame_number = frame_number

        # tmp
        self.image_location = os.path.relpath(os.path.join(source_location.camera_dir, frame_number+'.jpg'),
                                               source_location.root_dir)
        self.label_dir = os.path.relpath(os.path.join(source_location.label_dir, frame_number+'.txt'),
                                         source_location.root_dir)

        # self.image_location = image_location
        # self.radar_location = radar_location
        # self.t_camera_radar_location = t_camera_radar_location
        # self.camera_projection_matrix_location = camera_projection_matrix_location
        # self.label_location = label_location

    @property
    def image(self):
        return self.get_image()

    @property
    def radar_data(self):
        return self.get_radar_data()

    @property
    def label_data(self):
        return self.get_label_data()

    @property
    def t_camera_lidar(self):
        return self.get_t_camera_lidar()

    @property
    def camera_projection_matrix(self):
        return self.get_camera_projection_matrix()

    def get_label_data(self):
        try:
            label = FrameLabels(os.path.join(self.source_location.label_dir, f'{self.frame_number}.txt'))
        except FileNotFoundError:
            logging.error(f"{self.frame_number}.jpg does not exist at location: {self.source_location.label_dir}!")
            return None
        return label

    def get_image(self):
        try:
            img = plt.imread(
                os.path.join(self.source_location.camera_dir, f'{self.frame_number}.jpg'))
        except FileNotFoundError:
            logging.error(f"{self.frame_number}.jpg does not exist at location: {self.source_location.camera_dir}!")
            return None

        return img

    def get_radar_data(self):
        try:
            radar_file = os.path.join(self.source_location.radar_dir, f'{self.frame_number}.csv')
            scan = pandas.read_csv(radar_file, dtype=np.float32)
            scan = scan[['x', 'y', 'z', 'rcs', 'doppler', 'u', 'v', 'label']]
            return scan.to_numpy(dtype=np.float32)

        except FileNotFoundError:
            logging.error(f"{self.frame_number}.bin does not exist at location: {self.source_location.radar_dir}!")
            return None

        return scan

    def get_t_camera_lidar(self):
        try:
            with open(os.path.join(self.source_location.radar_calib_dir, f"{self.frame_number}.txt"), "r") as f:
                lines = f.readlines()
                matrix = np.array(lines[0].strip().split(' ')[1:], dtype=np.float32).reshape(4, 4)
        except FileNotFoundError:
            logging.error(f"{self.frame_number}.bin does not exist at location: {self.source_location.radar_dir}!")
            return None

        return matrix

    def get_camera_projection_matrix(self):
        try:
            with open(os.path.join(self.source_location.radar_calib_dir, f"{self.frame_number}.txt"), "r") as f:
                lines = f.readlines()
                matrix = np.array(lines[1].strip().split(' ')[1:], dtype=np.float32).reshape(3, 4)
        except FileNotFoundError:
            logging.error(f"{self.frame_number}.bin does not exist at location: {self.source_location.radar_dir}!")
            return None

        return matrix
