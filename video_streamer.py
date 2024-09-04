from flask import Flask, Response, stream_with_context
import cv2

app = Flask(__name__)

# A global variable to hold the camera object
camera = None

def get_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)  # Open the camera
    return camera

def generate_frames():
    camera = get_camera()
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()

@app.route('/video_feed')
def video_feed():
    return Response(stream_with_context(generate_frames()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>Video Streaming</title>
        </head>
        <body>
            <h1>Video Streaming</h1>
            <img src="/video_feed" width="640" height="480">
        </body>
    </html>
    """

@app.teardown_appcontext
def shutdown_session(exception=None):
    global camera
    if camera is not None:
        camera.release()
        camera = None
    print("Camera released.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
