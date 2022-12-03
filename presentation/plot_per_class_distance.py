import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from waterScene.waterScene import WaterScene
from tqdm import tqdm
from waterScene.settings import LABEL_CODE_STR

dataroot = "/media/reid/ext_disk1/waterscene_all"

data_pier = np.load('vessel.npy')

plt.hist(data_pier, bins=25, facecolor="skyblue", edgecolor="skyblue", alpha=0.7)
plt.xlabel("Distance(m)")
plt.title("Vessel")
plt.show()

# flowsc = WaterScene(dataroot)
# all_samples = flowsc.getTrainFrame()
# all_samples.extend(flowsc.getValtFrame())
# all_samples.extend(flowsc.getTestFrame())
#
# labels_dict = {"pier": [], "ship": [], "boat": [], "vessel": []}
# for sample in tqdm(all_samples):
#     frame = flowsc.loadFrame(sample)
#     labels = frame.label_data.label_dict
#     radar = frame.radar_data
#     radar = radar[np.where(radar[:, 7] != 0)]
#     distance = radar[:, 2].mean()
#     labels_dict[labels[0]['class']].append(distance)
#
#
# np.save('pier.npy', np.array(labels_dict['pier']))
# np.save('ship.npy', np.array(labels_dict['ship']))
# np.save('boat.npy', np.array(labels_dict['boat']))
# np.save('vessel.npy', np.array(labels_dict['vessel']))
