import requests, glob
from functools import partial

import torch
import torchvision
from torchvision import models, transforms
from torchvision.io import ImageReadMode

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

def image_from_path(image_path):
    image = torchvision.io.read_image(
        image_path,
        mode=ImageReadMode.RGB)
    # image /= 255.
    
    return image / 255.

    

def resize(image, shape=(300,300)):
    tfs = transforms.Resize(shape)
    return tfs(image)

class CatDetector(torch.nn.Module):
    def __init__(self, ):
        super().__init__()
        # self.model = models.detection.fasterrcnn_resnet50_fpn_v2(pretrained=True)
        self.model = models.detection.fasterrcnn_mobilenet_v3_large_fpn(pretrained=True)
        self.eval()

    def forward(self, x):
        if len(x.shape)<4:
            x = torch.unsqueeze(x,0)
        x = self.model(x)
        return x

    def detect(self, x, score_threshold=0.5, animal=None):
        detections = self.forward(x)
        labels = []
        labels_scores = []
        for detection in detections:
            # labels.extend([COCO_INSTANCE_CATEGORY_NAMES[label] for label,score in zip(detection['labels'],detection)])
            for label,score in zip(detection['labels'],detection['scores']):
                label_name = COCO_INSTANCE_CATEGORY_NAMES[label]
                labels_scores.append((label_name, score))
                if score > score_threshold:
                    labels.append(label_name)
            # for label in detection['labels']: 
        if animal is None:
            return labels_scores
        else:
            return animal in labels
    detect_cat = partial(detect, animal='cat')
    detect_bird = partial(detect, animal='bird')
    
    def detect_cat(self, x, *args, **kwargs):

        return self.detect(x, animal='cat', *args, **kwargs)

                
class RemoteCameraClient:
    def __init__(self):
        self.hostname = 'http://rpi0.local:5000'
    
    def get_image(self):
        res = requests.get(
            f'{self.hostname}/image'
        )
        tmp_file_path = './tmp_image.jpg'
        with open(tmp_file_path,'wb') as _file:
            _file.write(res.content)
        return image_from_path(tmp_file_path)
        # breakpoint()

        """
        TODO
         - set rpi remote camera script to start on boot
         - set periodic requests for images
         - send notification if there is a cat detected
        """

def main(image_paths):
    model = CatDetector()
    for image_path in image_paths:
        image = image_from_path(image_path)
        image = resize(image)
        cat_in_image = model.detect_cat(image)
        # print(a)
        if cat_in_image:
            print(f'Cat {"not" if not cat_in_image else ""} in {image_path}')

if __name__=="__main__":
    image_paths = glob.glob('./images/rpi0/image*')
    main(image_paths)
