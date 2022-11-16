import os
import ntpath
import numpy as np
import glob
path = "/media/reid/Dataset/dataset/dataset_clean"

radarPath = os.path.join(path, "radar")
radars = glob.glob(os.path.join(radarPath, "*"))
radars = sorted(radars)

for idx, radarName in enumerate(radars):
    name_prefix = os.path.splitext(ntpath.basename(radarName))[0]
    aa = os.path.join(radarPath, name_prefix + ".bin")
    radarTimestamp = np.fromfile(aa, dtype=np.float32).reshape(-1, 9)
    pass


