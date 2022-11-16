from waterScene.waterScene import WaterScene

import argparse
import numpy as np
import os
import json


def run(data_dir, out_dir):
    flowsc = WaterScene(root_dir=args.dataroot)
    # os.mkdir(os.path.join(args.dataroot, "norm_info"))
    all_samples = [flowsc.getTrainFrame(), flowsc.getValtFrame(), flowsc.getTestFrame()]
    all_samples = sum(all_samples, [])

    # load per image norm info
    # for samples in all_samples:
    #     norm_info = {}
    #     norm_save_path = os.path.join(args.dataroot, 'norm_info', samples + '.json')
    #     frame = flowsc.loadFrame(samples)
    #     im = np.copy(frame.image)
    #     im = im.astype('float64')
    #     means = im.mean(axis=(0, 1), dtype='float64')
    #     stds = im.std(axis=(0, 1), dtype='float64')
    #     mean = np.reshape(means, [3, 1])
    #     std = np.reshape(stds, [3, 1])
    #     norm_info['mean'] = (mean[0, 0], mean[1, 0], mean[2, 0])
    #     norm_info['std'] = (std[0, 0], std[1, 0], std[2, 0])
    #     with open(norm_save_path, 'w') as f:
    #         json.dump(norm_info, f, sort_keys=True, indent=4)

    # calcaute dataset image norm info

    all_samples = [flowsc.getTrainFrame(),]
    all_samples = sum(all_samples, [])
    num_item = 0
    json_name = 'gt_coco_train.json'
    for samples in all_samples:
        norm_param = {}
        num_item += 1
        with open(os.path.join(args.dataroot, "norm_info", samples + '.json'), 'r') as f:
            image_info = json.load(f)
        if num_item == 1:
            pc_im_means, pc_im_stds = np.asarray(image_info['mean']), np.asarray(image_info['std'])
        else:
            tmp_pc_im_means, tmp_pc_im_stds = np.asarray(image_info['mean']), np.asarray(image_info['std'])

            pc_im_means = (num_item - 1) / num_item * pc_im_means + tmp_pc_im_means / num_item
            pc_im_stds = (num_item - 1) / num_item * pc_im_stds + tmp_pc_im_stds / num_item

    norm_param['im_means'] = [item for item in pc_im_means]
    norm_param['im_stds'] = [item for item in pc_im_stds]
    with open(os.path.join(out_dir, 'norm_param_' + json_name),
                  'w') as outfile:
        outfile.write(json.dumps(norm_param))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert radar point',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dataroot', type=str,
                        default='/media/reid/ext_disk1/dataset-1031')
    args = parser.parse_args()
    run(args.dataroot, args.dataroot)
