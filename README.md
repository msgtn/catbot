# CatBot

Raw CatBot scripts. 
`remote_camera.py` runs on the Pi 0 with the camera monitoring the scene.
`main.py` runs on the computer running the object detector.
The Pi 0 needs to run an `ngrok` tunnel so that Twilio can request images to send in texts.

Requires updating either environment variables or directly in `main.py`:
- Twilio SID, authtoken, number
- The origin of the `ngrok` tunnel, e.g. `https://some-set-of-words.ngrok-free.app/`
- The origin of the Raspberry Pi with the camera, e.g. `http://rpi0.local:5000`
