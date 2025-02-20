# Flockr
Flockr uses a [Tensor Flow Lite model](https://www.kaggle.com/models/google/aiy/tfLite/vision-classifier-birds-v1/3?tfhub-redirect=true) to classify the species of a bird. It was heavily inspired by the [Who's at My Feeder](https://github.com/mmcc-xx/WhosAtMyFeeder/blob/master/speciesid.py) project. 

But, in this build, the classificaiton runs locally on a Raspberry Pi 5 and transmits the Base64 encoded image and classifcation results over serial to a [Particle Boron](https://store.particle.io/products/boron-lte-cat-m1-noram-with-ethersim-4th-gen). The Particle device should be running the [Flockr Transmitter firmware](https://github.com/epietrowicz/flockr-transmitter) which handles uploading the image and classification results. 

The Pi also hosts a web server that can be used to view the current feed if WiFi is available, but WiFi access is not necessary for this system to work. If you want to use the demo route in the web viewer, you will need to add a `test-video.mp4` file to the root of the project's directory. I've [provided a test video](https://drive.google.com/file/d/1tTz1Gps4WgYqqTi08huPQqQcx8DzA_3P/view?usp=sharing), but I cannot promise it will be hosted at this link indefinitely. I encourage sourcing your own.

![sample-classification](https://github.com/user-attachments/assets/ee12eabd-3c7d-4980-957e-c50986bf321e)

![sample-classification-particle](https://github.com/user-attachments/assets/ab706e47-30df-44bb-af55-a7fb3d8975ed)

## Running Fockr
[Docker and Docker Compose](https://docs.docker.com/engine/install/raspberry-pi-os/) are necessary to build and run the container.

Make sure that the Particle board and USB camera are plugged in **before** starting up the container.

To build: `docker-compose up --build`

To run the container: `docker-compose up`

Navigate to <rpi_ip>:5000 with any browser on the same network to view the live feed and test the classification.

## Possible Errors

If you get errors that a specific device is not found such as `/dev/ttyACM0` or `/dev/video0` change the mapings in [docker-compose.yml](https://github.com/epietrowicz/flockr-app/blob/main/docker-compose.yml). If the Particle device connected via serial is the device not found, then you'll also have to change the `SERIAL_DEV` variable in [utils.py](https://github.com/epietrowicz/flockr-app/blob/main/src/utils.py).
