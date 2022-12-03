import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from waterScene.waterScene import WaterScene
from tqdm import tqdm


dataroot = "/media/reid/ext_disk1/waterscene_all"

data = np.load('tmp.npy')

plt.hist(data, bins=25, facecolor="lightgreen", edgecolor="lightgreen", alpha=0.7)
plt.xlabel("Number of Points")
plt.title("4D radar")
plt.show()

# flowsc = WaterScene(dataroot)
# all_samples = flowsc.getTrainFrame()
# all_samples.extend(flowsc.getValtFrame())
# all_samples.extend(flowsc.getTestFrame())
#
# num_points = []
# for sample in tqdm(all_samples):
#     frame = flowsc.loadFrame(sample)
#     xx = frame.radar_data
#     num_points.append(xx.size)
#
# np.save('tmp.npy', np.array(num_points))