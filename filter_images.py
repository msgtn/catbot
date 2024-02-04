import os, glob, shutil
from PIL import Image
import torch
import torchvision
import cat_detect

IMAGES_DIR = "./images_2/rpi0/"
FILTER_DIR = "./images_2/cat/"
IMAGE_IDX = 0 

if __name__=="__main__":
    model = cat_detect.CatDetector()
    
    images = glob.glob(f"{IMAGES_DIR}/*/*.jpg")
    for image in images[:]:
        try:
            _image = Image.open(os.path.abspath(image))
        except:
            print(f"failed on {image}")
            continue
        _image = torchvision.transforms.functional.pil_to_tensor(_image)
        _image = _image.type(torch.FloatTensor)/255.
        detections = model.detect(_image, score_threshold=0.4)
        detections = [d[0] for d in detections]
        if "cat" in detections:
            shutil.copy2(image,
                os.path.join(FILTER_DIR, 
                    f"image_{IMAGE_IDX}.jpg"))    
            IMAGE_IDX += 1

        
