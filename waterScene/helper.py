import matplotlib.pyplot as plt


class ImageBox(object):
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


# transform form yolov5 format to
def transfer2Pixel(locations, image_shape):
    center_x = locations[0] * image_shape[1]
    center_y = locations[1] * image_shape[0]
    width = locations[2] * image_shape[1]
    height = locations[3] * image_shape[0]

    x1 = int(center_x - (width / 2))
    y1 = int(center_y + (height / 2))
    x2 = int(center_x + (width / 2))
    y2 = int(center_y - (height / 2))
    return [x1, y1, x2, y2]


def plot_boxes(locations, color):
    imageBox = ImageBox(locations[0], locations[2], locations[1], locations[3])
    plt.plot([imageBox.x1, imageBox.x1], [imageBox.y1, imageBox.y2],
             color=color)
    plt.plot([imageBox.x1, imageBox.x2], [imageBox.y1, imageBox.y1],
             color=color)
    plt.plot([imageBox.x2, imageBox.x2], [imageBox.y1, imageBox.y2],
             color=color)
    plt.plot([imageBox.x1, imageBox.x2], [imageBox.y2, imageBox.y2],
             color=color)
