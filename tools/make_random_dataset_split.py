import os
import pandas as pd
import numpy as np
from waterScene.waterScene import WaterScene
from tqdm import tqdm


def makeImageSets(base_path, split_path, camera_path):
    data = []
    flowsc = WaterScene(base_path)
    split_path = split_path
    for ele in tqdm(os.listdir(camera_path)):
        name_prefix = os.path.splitext(ele)[0]
        try:
            frame = flowsc.loadFrame(name_prefix)
            _ = frame.image, frame.radar_data, frame.camera_projection_matrix, frame.t_camera_lidar, frame.label_data
            data.append(name_prefix)
        except Exception:
            print(f"error data of {name_prefix}")

    train_set, testval_set = split_train_test(pd.Series(data), 0.2)
    test_set, val_set = split_train_test(testval_set, 0.5)

    with open(os.path.join(split_path, 'train.txt'), 'w') as f:
        for ele in train_set.values:
            f.write(ele)
            f.write("\n")

    with open(os.path.join(split_path, 'test.txt'), 'w') as f:
        for ele in test_set.values:
            f.write(ele)
            f.write("\n")

    with open(os.path.join(split_path, 'val.txt'), 'w') as f:
        for ele in val_set.values:
            f.write(ele)
            f.write("\n")


def split_train_test(data, test_ratio):
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]


if __name__ == '__main__':
    base_path = "/media/reid/ext_disk1/waterscene_all"
    split_path = "/media/reid/ext_disk1/waterscene_all/ImageSets"
    camera_path = "/media/reid/ext_disk1/waterscene_all/image"
    makeImageSets(base_path, split_path, camera_path)
