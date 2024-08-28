from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate_frames():
    # Use your webcam, or specify a video file
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the output frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Home page that displays the video stream
    return '''
        <html>
        <head>
            <title>Video Streamer</title>
        </head>
        <body>
            <h1>Live Video Stream</h1>
            <img src="/video_feed" width="640" height="480" />
        </body>
        </html>
        '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
