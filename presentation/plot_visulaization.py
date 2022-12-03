import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from waterScene.waterScene import WaterScene
from tqdm import tqdm
from waterScene.settings import LABEL_CODE_STR


dataroot = "/media/reid/ext_disk1/waterscene_all"

data_pier = np.load('vessel.npy')


flowsc = WaterScene(dataroot)
all_samples = flowsc.getTrainFrame()
all_samples.extend(flowsc.getValtFrame())
all_samples.extend(flowsc.getTestFrame())

for sample in tqdm(all_samples):
    frame = flowsc.loadFrame(sample)
    labels = frame.label_data.label_dict
    if labels[0]['class'] == 'vessel':
        print(sample)

