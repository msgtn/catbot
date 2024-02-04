import cat_detect
import requests
import io
import time

import torch
import torchvision

from PIL import Image
from twilio.rest import Client
import os

account_sid = os.environ.get('TWILIO_SID') 
auth_token = os.environ.get('TWILIO_AUTHTOKEN') 
client = Client(account_sid, auth_token)

# TODO - pull local then send remote for twilio
# to save bandwidth from ngrok
LOCAL_ORIGIN = 'http://rpi0.local:5000/'
CATBOT_ORIGIN = os.environ.get("NGROK_ORIGIN")
IMAGE_URL = f"{CATBOT_ORIGIN}/image"
IMAGE_SIZE = (3280, 2464)
INTERVAL = 0.5  # minutes
PHONE_NUMBER = os.environ.get("TWILIO_NUMBER")

def send_image(animal='cat',number=PHONE_NUMBER):
    message = client.messages.create(
        from_=PHONE_NUMBER,
        body=f'{animal.capitalize()} detected!',
        to=number,
        media_url=[IMAGE_URL],
    )

def tap(n_taps=2):
    requests.get(
        f"{LOCAL_ORIGIN}/tap/{n_taps}"
    )

def main():
    model = cat_detect.CatDetector()
    while True:
    # loop forever
        # get image
        print("Getting image...")
        response = requests.get(
            f"{LOCAL_ORIGIN}/image",
            headers={
                'Cache-Control': "no-cache"
            },
            )

        if response.headers['Content-Type'] == 'image/jpeg':
            image = Image.open(io.BytesIO(response.content))
            image.save('./image.jpg')
            image = torchvision.transforms.functional.pil_to_tensor(image)
            image = image.type(torch.FloatTensor)/255.
            detections = model.detect(image, score_threshold=0.4)
            labels = [d[0] for d in detections if d[1]>0.5]
            labels_higher = [d[0] for d in detections if d[1]>0.8]
            print(labels, labels_higher)
            if 'cat' in labels or 'dog' in labels: 
                print(f"Cat detected at {time.time()}")
                send_image('cat')
                INTERVAL = 2
            elif 'bird' in labels_higher:
                print(f"Bird detected at {time.time()}")
                send_image('bird')
                time.sleep(5)
                tap()
                INTERVAL = 0.5
            else:
                   # If no detections, probably night 
                   if len(detections)==0:
                       INTERVAL = 10
                   else:
                       INTERVAL = 0.3
                
        time.sleep(INTERVAL*60)

if __name__=="__main__":
    main()
