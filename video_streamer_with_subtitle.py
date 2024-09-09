from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Define global variables for camera and video capture
camera = cv2.VideoCapture(0)  # Default to camera
video_capture = None  # This will be used for video file streaming

@app.route('/')
def index():
    # Render the HTML page with buttons to select stream source
    return render_template('index.html')

def generate_frames(capture):
    while True:
        success, frame = capture.read()
        if not success:
            break
        else:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield frame to be used in Response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Serve video stream from camera or video file
    if video_capture and video_capture.isOpened():
        return Response(generate_frames(video_capture), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif camera.isOpened():
        return Response(generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Error: Unable to open video source"

@app.route('/start_camera')
def start_camera():
    global video_capture, camera
    if video_capture:
        video_capture.release()
    camera = cv2.VideoCapture(0)  # Switch to camera
    return "Camera started", 200

@app.route('/start_video')
def start_video():
    global video_capture, camera
    if camera:
        camera.release()
    # Replace 'path/to/your/video.mp4' with your actual video file path
    video_capture = cv2.VideoCapture('path/to/your/video.mp4')
    return "Video started", 200

if __name__ == '__main__':
    app.run(debug=True)
