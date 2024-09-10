from flask import Flask, Response, stream_with_context, request, render_template_string
import cv2
import os

app = Flask(__name__)

# Global variables for video file and camera index
video_path = '/Users/abhimanyuray/Desktop/mummy/Mothers_day.mp4'
video_capture = None
CAMERA_INDEX = 0  # Update this if needed

def get_video_capture():
    global video_capture
    if video_capture is None:
        if not os.path.exists(video_path):
            print(f"Video file not found at path: {video_path}")
            return None
        video_capture = cv2.VideoCapture(video_path)  # Open the video file
        if not video_capture.isOpened():
            print("Failed to open video file.")
            video_capture = None
    return video_capture

def generate_camera_frames():
    camera = cv2.VideoCapture(CAMERA_INDEX)  # Initialize the camera here
    if not camera.isOpened():
        print(f"Failed to open camera with index {CAMERA_INDEX}.")
        return
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        camera.release()
        print("Camera released.")

def generate_video_frames():
    video_capture = get_video_capture()
    if video_capture is None:
        print("No video file available.")
        return
    try:
        while True:
            success, frame = video_capture.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        video_capture.release()
        video_capture = None
        print("Video capture released.")

@app.route('/video_feed')
def video_feed():
    stream_type = request.args.get('type', 'camera')
    if stream_type == 'video':
        return Response(stream_with_context(generate_video_frames()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    elif stream_type == 'camera':
        return Response(stream_with_context(generate_camera_frames()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Invalid stream type", 400

@app.route('/')
def index():
    stream_type = request.args.get('type', None)
    return render_template_string("""
    <html>
        <head>
            <title>Video Streaming</title>
        </head>
        <body>
            <h1>Video Streaming</h1>
            <form action="/" method="get">
                <button type="submit" name="type" value="camera">Stream from Camera</button>
                <button type="submit" name="type" value="video">Stream from Video</button>
            </form>
            {% if stream_type %}
            <img src="/video_feed?type={{ stream_type }}" width="640" height="480">
            {% endif %}
        </body>
    </html>
    """, stream_type=stream_type)

@app.teardown_appcontext
def shutdown_session(exception=None):
    global video_capture
    if video_capture is not None:
        video_capture.release()
        video_capture = None
    print("Video capture released.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
