import os
from . import commonutils
from .dataloader import DataLoader


class FileLocations:
    """
    This class contains the information regarding the locations of data for the dataset.
    """

    def __init__(self, root_dir: str, output_dir: str = None, frame_set_path: str = None, pred_dir: str = None):
        """
Constructor which based on a few parameters defines the locations of possible data.
        :param root_dir: The root directory of the dataset.
        :param output_dir: Optional parameter of the location where output such as pictures should be generated.
        :param frame_set_path: Optional parameter of the text file of which output should be generated.
        :param pred_dir: Optional parameter of the locations of the prediction labels.
        """

        # Input parameters
        self.root_dir: str = root_dir
        self.output_dir: str = output_dir
        self.frame_set_path: str = frame_set_path
        self.pred_dir: str = pred_dir

        # Automatically defined variables. The location of sub-folders can be customized here.
        # Current definitions are based on the recommended locations.
        self.camera_dir = commonutils.mkDataDirs(self.root_dir, 'image')
        self.radar_dir = commonutils.mkDataDirs(self.root_dir, 'radar')
        self.radar_calib_dir = commonutils.mkDataDirs(self.root_dir, 'calib')

        self.label_dir = commonutils.mkDataDirs(self.root_dir, 'label_kitti')
        self.label_voc_dir = commonutils.mkDataDirs(self.root_dir, 'label')
        self.split_dir = commonutils.mkDataDirs(self.root_dir, "ImageSets")


class WaterScene(FileLocations):
    def __init__(self, root_dir: str, output_dir: str = None, frame_set_path: str = None, pred_dir: str = None):
        super().__init__(root_dir, output_dir, frame_set_path, pred_dir)

    def loadFrame(self, frame_number):
        return DataLoader(frame_number, self)

    def getTrainFrame(self):
        with open(os.path.join(self.split_dir, "train.txt"), "r") as f:
            return [ele.replace('\n', '') for ele in f.readlines()]

    def getTestFrame(self):
        with open(os.path.join(self.split_dir, "test.txt"), "r") as f:
            return [ele.replace('\n', '') for ele in f.readlines()]

    def getValtFrame(self):
        with open(os.path.join(self.split_dir, "val.txt"), "r") as f:
            return [ele.replace('\n', '') for ele in f.readlines()]
