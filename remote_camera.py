# from picamera import PiCamera 
import time, os
from flask import Flask, send_file

# camera = PiCamera()
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/_image")
def _image():
    # grab image
    # send in response
    image_path = os.path.expanduser('~/image.jpg')
    camera.start_preview()
    time.sleep(4)
    camera.capture(image_path)
    time.sleep(1)
    camera.stop_preview()
    return send_file(image_path, mimetype='image/jpeg')

@app.route("/image")
def image():
    image_path = os.path.expanduser('~/image.jpg')
    os.system(f'raspistill -q 10 -o {image_path}')
    return send_file(image_path, mimetype='image/jpeg')


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
