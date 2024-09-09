from flask import Flask, Response, render_template_string, url_for
import cv2

app = Flask(__name__)

# Path to the predefined video file
VIDEO_FILE_PATH = 'video.mp4'  # Ensure this file is present in the same directory

# HTML template minimized and embedded in Python
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Video Streamer</title>
</head>
<body>
    <h1>Select Streaming Option:</h1>
    <button onclick="location.href='/camera'">Stream from Camera</button>
    <button onclick="location.href='/video'">Stream from Video File</button>
    <video id="videoElement" controls autoplay></video>

    <script>
        // Function to set video source dynamically
        const videoElement = document.getElementById('videoElement');
        if (location.pathname === '/camera') {
            videoElement.src = '{{ url_for("camera_feed") }}';
        } else if (location.pathname === '/video') {
            videoElement.src = '{{ url_for("video_feed") }}';
        }

        // Stop video stream when tab is closed
        window.addEventListener('beforeunload', function () {
            videoElement.pause();
            videoElement.src = "";
        });
    </script>
</body>
</html>
"""

def generate_camera_feed():
    """Generator function to yield camera frames."""
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

def generate_video_feed():
    """Generator function to yield video file frames."""
    cap = cv2.VideoCapture(VIDEO_FILE_PATH)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/camera')
def camera_page():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video')
def video_page():
    return render_template_string(HTML_TEMPLATE)

@app.route('/camera_feed')
def camera_feed():
    return Response(generate_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
