# Flockr
Flockr uses a Tensor Flow Lite model to classify the species of a bird. The classificaiton runs locally on a Raspberry Pi 5 and transmits the Base64 encoded image and the classifcation results over serial to a [Particle Boron](https://store.particle.io/products/boron-lte-cat-m1-noram-with-ethersim-4th-gen). The Particle device is responsible for sending this data to the cloud via LTE. 

![sample-classification-particle](https://github.com/user-attachments/assets/ab706e47-30df-44bb-af55-a7fb3d8975ed)

The Pi also hosts a web server that can be used to view the current feed if WiFi is available, but WiFi access is not necessary for this system to work.

![sample-classification](https://github.com/user-attachments/assets/ee12eabd-3c7d-4980-957e-c50986bf321e)

## Running Fockr
[Docker and Docker Compose](https://docs.docker.com/engine/install/raspberry-pi-os/) are necessary to build and run the container.

Make sure that the Particle board and USB camera are plugged in **before** starting up the container.

To build: `docker-compose up --build`

To run the container: `docker-compose up`

Navigate to <rpi_ip>:5000 with any browser on the same network to view the live feed and test the classification.

## Possible Errors

If you get errors that a specific device is not found such as `/dev/ttyACM0` or `/dev/video0` change the mapings in [docker-compose.yml](https://github.com/epietrowicz/flockr-app/blob/main/docker-compose.yml). If the Particle device connected via serial is the device not found, then you'll also have to change the `SERIAL_DEV` variable in [utils.py](https://github.com/epietrowicz/flockr-app/blob/main/src/utils.py).
