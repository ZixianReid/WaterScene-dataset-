class FrameLabels:
    def __init__(self, label_location):
        self.label_location = label_location

    @property
    def label_dict(self):
        return self.get_label_dict()

    def get_label_dict(self):
        labels = []
        f = open(self.label_location)
        for line in f.readlines():
            label_class, difficult, xmin, ymin, xmax, ymax = line.split()
            xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])
            labels.append({'class': label_class,
                           'xmin': xmin,
                           'ymin': ymin,
                           'xmax': xmax,
                           'ymax': ymax}
                          )
        return labels