import matplotlib.pyplot as plt
from waterScene.waterScene import WaterScene

dataroot = "/media/reid/ext_disk1/waterscene_all"

flowsc = WaterScene(dataroot)
all_samples = flowsc.getTrainFrame()
all_samples.extend(flowsc.getValtFrame())
all_samples.extend(flowsc.getTestFrame())
labels_dict = {"pier": 64346, "ship": 7995, "boat": 4484, "vessel": 5049}

# i = 0
# for sample in tqdm(all_samples):
#     i += 1
#     frame = flowsc.loadFrame(sample)
#     labels = frame.label_data.label_dict
#     for label in labels:
#         labels_dict[label['class']] = labels_dict[label['class']] + 1


num_list = labels_dict.values()
labels = ["pier", "ship", "boat", "vessel"]
colors = ['cyan', 'darkturquoise', 'cadetblue', 'skyblue', 'mediumseagreen']

plt.bar(range(len(num_list)), num_list, tick_label=labels, color=colors)
plt.ylabel('Num of Objects')

plt.show()
