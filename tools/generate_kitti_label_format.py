from waterScene.waterScene import WaterScene
import xml.dom.minidom
import os
from tqdm import tqdm
import argparse

class ImageLabel:
    def __init__(self, path):
        self.root = xml.dom.minidom.parse(path).documentElement

    @property
    def label_dict(self):
        return self.__get_label_dict()

    @property
    def width(self):
        return self.__get_width()

    @property
    def height(self):
        return self.__get_height()

    def __get_width(self):
        width = self.root.getElementsByTagName("size")[0] \
            .getElementsByTagName('width')[0] \
            .firstChild.data
        return int(width)

    def __get_height(self):
        height = self.root.getElementsByTagName("size")[0] \
            .getElementsByTagName('height')[0] \
            .firstChild.data
        return int(height)

    def __get_label_dict(self):
        labels = []
        objects = self.root.getElementsByTagName('object')
        for ele in objects:
            name = ele.getElementsByTagName('name')[0].firstChild.data
            difficult = ele.getElementsByTagName('difficult')[0].firstChild.data
            bndbox = ele.getElementsByTagName("bndbox")[0]
            xmin = bndbox.getElementsByTagName("xmin")[0].firstChild.data
            ymin = bndbox.getElementsByTagName("ymin")[0].firstChild.data
            xmax = bndbox.getElementsByTagName("xmax")[0].firstChild.data
            ymax = bndbox.getElementsByTagName("ymax")[0].firstChild.data
            labels.append({"class": name,
                           "difficult": difficult,
                           "xmin": int(xmin),
                           "ymin": int(ymin),
                           "xmax": int(xmax),
                           "ymax": int(ymax)})
        return labels

    def save_Label_dict(self, out_dir):
        with open(out_dir, 'w') as f:
            for label in self.label_dict:
                for value in label.values():
                    i = str(value) + " "
                    f.write(i)
                f.write("\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', type=str, default="/media/reid/ext_disk1/waterscene_all")

    args = parser.parse_args()
    data_root = args.data_root
    eles = os.listdir(os.path.join(data_root, "image"))
    flowsc = WaterScene(root_dir=data_root)
    eles = tqdm(eles)
    for ele in eles:
        nu = os.path.splitext(ele)[0]
        label_path = os.path.join(data_root, "label", str(nu) + '.xml')
        imageLabeler = ImageLabel(label_path)
        imageLabeler.save_Label_dict(os.path.join(data_root, "label_kitti",
                                                  str(nu) + ".txt"))

