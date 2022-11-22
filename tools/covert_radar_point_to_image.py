import argparse
import os
from concurrent import futures
import multiprocessing
from waterScene.waterScene import WaterScene
from waterScene.visual import Visualization2D
import numpy as np
from waterScene import transformation
import os
import cv2
from PIL import Image
import sys
import json

_DISTANCE_RANGE = [0, 250]
_SPEED_RANGE = [-33, 33]
_POWERRANGE = [0, 50]

CPU_COUNT = 4


# Print iterations progress (thanks StackOverflow)
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percents = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(bar_length * iteration / float(total)))
    bar = '' * filledLength + '-' * (bar_length - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\x1b[2K\r')
    sys.stdout.flush()


def draw_pc_image(pc, save_path, width=1920, height=1080):
    img_b = np.zeros((height, width), np.uint8)
    img_g = np.zeros((height, width), np.uint8)
    img_r = np.zeros((height, width), np.uint8)
    his_mask = np.zeros((height, width), np.uint8)
    pc = pc[:, pc[2, :].argsort()]
    thickness = -1
    num_points = pc.shape[1]
    for i in range(num_points):
        center_coordinates = (int(pc[0, i]), int(pc[1, i]))
        depth = pc[4, i]
        v = pc[6, i]
        power = pc[5, i]
        if (depth > _DISTANCE_RANGE[0]) and (depth < _DISTANCE_RANGE[1]):
            if (v > _SPEED_RANGE[0]) and (v < _SPEED_RANGE[1]):
                if (power > _POWERRANGE[0]) and (power < _POWERRANGE[1]):
                    red = int(depth / 250 * 128 + 127)
                    green = int((v + 20) / 40 * 128 + 127)
                    blue = int((power / 40 * 128 + 127))
                    color = (blue, green, red)
                    color = np.asarray(color).astype(np.uint8)
                    cur_mask = np.zeros((1080, 1920), np.uint8)
                    cur_mask = cv2.circle(cur_mask, center_coordinates, 1, 1, thickness)
                    save_cur_mask = cur_mask - cur_mask * his_mask
                    img_b = img_b + save_cur_mask * color[2]
                    img_g = img_g + save_cur_mask * color[1]
                    img_r = img_r + save_cur_mask * color[0]
                    his_mask = his_mask + save_cur_mask
    im = np.stack([img_r, img_g, img_b], axis=2)
    image = Image.fromarray(im, 'RGB')
    image.save(save_path)

    norm_info = {}
    norm_save_path = save_path.replace('.png', '.json')
    im = im.astype('float64')
    means = im.mean(axis=(0, 1), dtype='float64')
    stds = im.std(axis=(0, 1), dtype='float64')
    mean = np.reshape(means, [3, 1])
    std = np.reshape(stds, [3, 1])
    norm_info['mean'] = (mean[0, 0], mean[1, 0], mean[2, 0])
    norm_info['std'] = (std[0, 0], std[1, 0], std[2, 0])
    with open(norm_save_path, 'w') as f:
        json.dump(norm_info, f, sort_keys=True, indent=4)


def convert_pcd_file(idx):
    data = flowsc.loadFrame(idx)
    save_path = os.path.join(flowsc.root_dir, 'imagepc', str(idx) + '.png')
    save_folder = os.path.dirname(save_path)
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # uvs, _, _, pc = transformation.project_pcl_to_image(data.radar_data, data.t_camera_lidar,
    #                                                     data.camera_projection_matrix, data.image.shape)
    xx = data.radar_data
    uvs = data.radar_data[:, 8:10]
    pc = data.radar_data[:, 0:5]
    pc = np.concatenate((uvs, pc), axis=1).T


    draw_pc_image(pc, save_path)


def run():
    print("Generating 2D radar image by depth, v and p")
    num_threads = CPU_COUNT
    all_sample = [os.path.splitext(ele)[0] for ele in os.listdir(flowsc.camera_dir)]
    num_samples = len(all_sample)
    with futures.ProcessPoolExecutor(max_workers=num_threads) as executor:
        fs = [executor.submit(convert_pcd_file, idx) for idx in all_sample]
        for i, f in enumerate(futures.as_completed(fs)):
            print_progress(i, num_samples, prefix="flowScene", suffix='Done ', bar_length=40)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert radar point',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dataroot', type=str,
                        default='/media/reid/ext_disk1/waterscene_all')

    args = parser.parse_args()

    flowsc = WaterScene(root_dir=args.dataroot)
    run()