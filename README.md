# WaterScene-dataset-
Waterscene dev


## Overview

-[Install](#Install) \
-[Prepare-Data](#Prepare-DATA) \
-[COCO-annotations](#COCO-annotations) \
-[Radar-pseudo-image](#Radar-pseudo-image)


## Install
Please refer following instruction to install waterscene dev
```shell
git clone git@github.com:ZixianReid/WaterScene-dataset-.git
cd your_repositroy
python setup.py build develop --no-deps
```

## Prepare-DATA
Please download Waterscene dataset from [this]().

Then, please run the following script
```shell
cd your_repositroy
python tools/generate_kitti_label_format.py --data_root your_dataset_root
```

### Test validation
After the above work, the dataset should be available. Please test it by
following commands.
```shell
python tools/test_vaildation.py --data_root your_dataset_root
```

## COCO-annotations
Generally, most developed benchmark for waterscene is based on coco evaluation. So
coco format annotations is necessary.

If you need to generate fully annotations for waterscene. Please run:
```shell
python tools/generate_2d_coco_annotations.py --data_root your_dataset_root
```

If you nned to generate annotations for part of waterscene. Please run:
```shell
python tools/generate_mini_2d_coco_annotations.py --data_root your_dataset_root
```
The script will generate 3000 samples for training, 240 samples for validation and 240
samples for testing.

## Radar-pseudo-image

If you want to reimplement networks using radar pseudo image, such as [SAF-FCOS](https://github.com/Singingkettle/SAF-FCOS)
or [ CameraRadarFusionNet](https://github.com/TUMFTM/CameraRadarFusionNet). Please run the following scripts
```shell
python tools/covert_radar_point_to_image.py --data_root your_dataset_root
```


## radar-data-format

1. x
2. y
3. z
4. rcs
5. doppler
6. u
7. v
8. label