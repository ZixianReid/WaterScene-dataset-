from waterScene.waterScene import WaterScene
import argparse
import os
import json
from waterScene.settings import LABEL_CODE_STR
from tqdm import tqdm


# mini_dataset 3000 training 240 test, 240 validation

def run(data_dir, out_dir):
    flowsc = WaterScene(root_dir=args.dataroot)
    sets = ['train', 'val', 'test']
    all_samples = flowsc.getTrainFrame()
    img_id = 0
    ann_id = 0
    json_name = 'gt_coco_point_mini_%s.json'


    train_num = 3000
    test_num = 240
    start_iter = 0
    end_iter = 0
    for data_set in sets:
        print(f"Starting {data_set}")
        ann_dict = {}
        images = []
        annotations = []

        if data_set == 'train':
            end_iter += train_num

        if data_set == 'val':
            start_iter += train_num
            end_iter += test_num

        if data_set == 'test':
            start_iter += test_num
            end_iter += test_num

        for i in range(start_iter, end_iter):
            frame = flowsc.loadFrame(all_samples[i])
            image = dict()
            image['id'] = img_id
            img_id += 1
            image['width'] = 1920
            image['height'] = 1080
            image['file_name'] = frame.image_location
            image['pc_file_name'] = frame.image_location.replace("image", 'radar').replace('jpg', 'csv')
            image['pc_image_file_name'] = frame.image_location.replace("image", "imagepc").replace('jpg', 'png')
            images.append(image)
            labels = frame.label_data.label_dict
            for label in labels:
                legal_box = True
                ann = dict()
                ann['legal'] = legal_box
                ann['id'] = ann_id
                ann_id += 1
                ann['image_id'] = image['id']
                ann['category_id'] = int(LABEL_CODE_STR[label['class']])
                ann['iscrowd'] = 0
                xyxy_box = [label['xmin'], label['ymin'], label['xmax'], label['ymax']]
                xywh_box = xyxy_to_xywh(xyxy_box)
                ann['bbox'] = xywh_box
                ann['area'] = xywh_box[2] * xywh_box[3]
                ann['segmentation'] = xyxy_to_polygn(xyxy_box)
                annotations.append(ann)

            # categories = [{"id": 0, "name": "background"}, {"id": 1, "name": 'pier'}, {"id": 2, "name": 'buoy'},
            #               {"id": 3, "name": 'ship'}, {"id": 4, "name": 'boat'}]
        categories = [{"id": 1, "name": 'pier'}, {"id": 2, "name": 'buoy'},
                      {"id": 3, "name": 'ship'}, {"id": 4, "name": 'boat'}, {"id": 5, "name": "vessel"}]
        ann_dict['images'] = images
        ann_dict['categories'] = categories
        ann_dict['annotations'] = annotations
        print("Num categories: %s" % len(categories))
        print("Num images: %s" % len(images))
        print("Num annotations: %s" % len(annotations))
        with open(os.path.join(out_dir, json_name % data_set), 'w') as outfile:
            outfile.write(json.dumps(ann_dict))

def xyxy_to_xywh(xyxy_box):
    xmin, ymin, xmax, ymax = xyxy_box
    TO_REMOVE = 1
    xywh_box = (xmin, ymin, xmax - xmin + TO_REMOVE, ymax - ymin + TO_REMOVE)
    return xywh_box


def xyxy_to_polygn(xyxy_box):
    xmin, ymin, xmax, ymax = xyxy_box
    xywh_box = [[xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]]
    return xywh_box


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert radar point',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dataroot', type=str, default='/media/reid/ext_disk1/waterscene_all')
    args = parser.parse_args()
    run(args.dataroot, args.dataroot)
