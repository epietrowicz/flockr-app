from flask import Flask, Response, render_template
from flask_socketio import SocketIO

from utils import generate_frames, fast_forward, rewind

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/demo")
def demo():
    return render_template("demo.html")

@app.route("/capture")
def capture():
    return render_template("capture.html")

@app.route("/video-capture")
def video_capture():
    return Response(
        generate_frames(True, socketio), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/demo-video")
def demo_video():
    return Response(
        generate_frames(False, socketio), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@socketio.on("fast_forward")
def fast_forward_handler():
    fast_forward()

@socketio.on("rewind")
def rewind_handler():
    rewind()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
