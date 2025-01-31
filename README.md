To build: `docker build -t flocker-app .`

To run the container: `docker run --rm -it -v "$(pwd):/app" --device=/dev/video0:/dev/video0 flocker-app`

Update webcam permissions:
```bash
sudo chmod 777 /dev/video0
```

Or using docker compose `docker-compose up (--build)`