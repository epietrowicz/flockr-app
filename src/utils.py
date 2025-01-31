import numpy as np
import cv2
from PIL import Image, ImageOps
import sqlite3
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

VIDEO_PATH = "test-video-2.mp4"  # Replace with your local video path
THRESHOLD = 0.7
NAMEDBPATH = "birdnames.db"

should_ff = True
should_rw = False

# Initialize the image classification model
base_options = core.BaseOptions(
    file_name="model.tflite", use_coral=False, num_threads=4
)

# Enable Coral by this setting
classification_options = processor.ClassificationOptions(
    max_results=1, score_threshold=0
)
options = vision.ImageClassifierOptions(
    base_options=base_options, classification_options=classification_options
)

# create classifier
global classifier
classifier = vision.ImageClassifier.create_from_options(options)


def load_labels_from_db():
    conn = sqlite3.connect(NAMEDBPATH)
    cursor = conn.cursor()

    # Assuming table is named 'labels' and column is 'name'
    cursor.execute("SELECT common_name FROM birdnames;")
    labels = [row[0] for row in cursor.fetchall()]

    conn.close()
    return labels


def classify(np_array):
    tensor_image = vision.TensorImage.create_from_array(np_array)
    categories = classifier.classify(tensor_image)
    return categories.classifications[0].categories


def format_frame(frame):
    # Resize as per model requirement
    image = Image.fromarray(frame)
    max_size = (224, 224)
    image.thumbnail(max_size)

    # Pad the image to fill the remaining space
    padded_image = ImageOps.expand(
        image,
        border=((max_size[0] - image.size[0]) // 2, (max_size[1] - image.size[1]) // 2),
        fill="black",
    )  # Change the fill color if necessary

    np_image = np.array(padded_image)
    return np_image


def get_common_name(scientific_name):
    conn = sqlite3.connect(NAMEDBPATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT common_name FROM birdnames WHERE scientific_name = ?",
        (scientific_name,),
    )
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        print("No common name for: " + scientific_name, flush=True)
        return "No common name found."

def fast_forward():
    global should_ff
    should_ff = True
    print(f"Stepping forward")

def rewind():
    global should_rw
    should_rw = True

def generate_frames(is_live, socketio):
    global should_ff
    global should_rw
    if is_live:
        cap = cv2.VideoCapture(0)
    else: 
        cap = cv2.VideoCapture("test-video.mp4")

    fps = cap.get(cv2.CAP_PROP_FPS)  # Get video FPS
    frame_interval = int(fps)
    frame_text = ["Unknown"]
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("End of video.")
            break

        if should_ff == True:
            current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            new_frame = current_frame + (10 * frame_interval) 
            cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            should_ff = False
        if should_rw == True:
            current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            new_frame = current_frame - (10 * frame_interval)
            new_frame = max(0, new_frame)
            cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            should_rw = False

        # Process every frame_interval-th frame (approx 1 second apart)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        np_image = format_frame(frame_rgb)
        categories = classify(np_image)
        category = categories[0]
        index = category.index
        score = category.score
        display_name = category.display_name

        if index != 964 and score > THRESHOLD:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            common_name = get_common_name(display_name)
            result_text = [f"Label: {common_name}", f"Score: {score}"]
            print(f"Timestamp: {timestamp} seconds, {result_text}")
            frame_text = result_text
        else:
            frame_text = ["Unknown"]

        socketio.emit("result", {'result': frame_text})
        _, buffer = cv2.imencode(".jpg", frame)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
        )
        frame_count += 1  # Increase frame count
