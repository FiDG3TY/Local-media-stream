from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

# Define the path correctly inside the static folder
VIDEO_FILE_PATH = 'static/Mothers_day.mp4'

# HTML template with embedded JavaScript and CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Streamer</title>
    <style>
        #videoElement {
            width: 80%;
            margin-top: 20px;
        }
        button {
            padding: 10px 20px;
            margin: 10px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Select Streaming Option:</h1>
    <button onclick="streamFromCamera()">Stream from Camera</button>
    <button onclick="streamFromVideo()">Stream from Video File</button>
    <video id="videoElement" controls autoplay></video>

    <script>
        const videoElement = document.getElementById('videoElement');

        function stopStreamedVideo() {
            const stream = videoElement.srcObject;
            if (stream) {
                const tracks = stream.getTracks();
                tracks.forEach(track => track.stop());
                videoElement.srcObject = null;
            }
        }

        function streamFromCamera() {
            stopStreamedVideo();
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    videoElement.srcObject = stream;
                })
                .catch(error => {
                    console.error("Error accessing camera:", error);
                    alert("Unable to access the camera.");
                });
        }

        function streamFromVideo() {
            stopStreamedVideo();
            videoElement.src = '/static/Mothers_day.mp4';  // Correct path to the video file
        }

        // Stop streaming when the tab is closed or navigated away
        window.addEventListener('beforeunload', stopStreamedVideo);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Serve the video file from the static folder
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Ensure the static folder exists and contains the video file
    os.makedirs('static', exist_ok=True)
    # Check if the video file exists and if not, prompt the user
    if not os.path.exists(VIDEO_FILE_PATH):
        print(f"Please place your video file at {VIDEO_FILE_PATH} or create a symbolic link in the static folder.")
    # Run the server on all interfaces and a specified port
    app.run(debug=True, host='0.0.0.0', port=5001)
