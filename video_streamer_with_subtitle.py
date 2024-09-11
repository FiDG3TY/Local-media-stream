from flask import Flask, Response, render_template_string, request, send_file
import cv2
import os
import subprocess

app = Flask(__name__)

# Configuration
VIDEO_PATH = '/Users/abhimanyuray/Desktop/mummy/Mothers_day.mp4'
SUBTITLE_PATH = '/Users/abhimanyuray/Desktop/mummy/Mothers_day.srt'
HLS_OUTPUT_PATH = '/tmp/hls/'  # Temporary directory for HLS files
CAMERA_INDEX = 0  # Use default system camera

def start_ffmpeg_hls(video_path, subtitle_path, output_path):
    """Starts FFmpeg to create HLS stream from a video with subtitles."""
    os.makedirs(output_path, exist_ok=True)
    command = [
        'ffmpeg', '-re', '-i', video_path,
        '-vf', f"subtitles={subtitle_path}",
        '-c:v', 'libx264', '-c:a', 'aac', '-preset', 'ultrafast',
        '-flags', '+cgop', '-g', '30', '-hls_time', '1',
        '-hls_list_size', '5', '-hls_flags', 'delete_segments',
        '-f', 'hls', os.path.join(output_path, 'stream.m3u8')
    ]
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def generate_camera_frames():
    """Generator to stream frames from the camera."""
    camera = cv2.VideoCapture(CAMERA_INDEX)
    while camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    camera.release()

@app.route('/')
def index():
    return render_template_string("""
    <html><head><title>Streamer</title></head>
    <body>
        <h1>Video Streaming</h1>
        <form action="/video_feed" method="get">
            <button type="submit" name="type" value="camera">Stream from Camera</button>
            <button type="submit" name="type" value="video">Stream Video with Audio and Subtitles</button>
        </form>
    </body></html>
    """)

@app.route('/video_feed')
def video_feed():
    stream_type = request.args.get('type')
    if stream_type == 'camera':
        return Response(generate_camera_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    elif stream_type == 'video':
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Video Streaming</title>
            <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
        </head>
        <body>
            <video id="my-video" class="video-js vjs-default-skin" controls preload="auto" width="640" height="264"
                   data-setup='{}'>
                <source src="/hls/stream.m3u8" type="application/x-mpegURL">
            </video>
            <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
        </body>
        </html>
        """)
    return "Invalid stream type", 400

@app.route('/hls/<path:filename>')
def hls(filename):
    return send_file(os.path.join(HLS_OUTPUT_PATH, filename))

if __name__ == '__main__':
    # Start FFmpeg process for HLS streaming
    hls_process = start_ffmpeg_hls(VIDEO_PATH, SUBTITLE_PATH, HLS_OUTPUT_PATH)
    try:
        app.run(host='0.0.0.0', port=5002, debug=True)
    finally:
        # Terminate FFmpeg when the Flask app stops
        hls_process.terminate()
        hls_process.wait()
        print("FFmpeg process terminated.")
