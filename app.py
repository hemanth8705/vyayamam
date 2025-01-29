from flask import Flask, Response, request
import requests

app = Flask(__name__)

# Replace with your Google Drive file ID
FILE_ID = "15pdwkrhL7CgpJYEtAmbKMT6tHoXD7jAI"

@app.route('/')
def index():
    """Serve the HTML page."""
    return open("templates/index.html").read()

@app.route('/video')
def video_stream():
    """Stream video from Google Drive."""
    google_drive_url = f"https://drive.google.com/uc?id={FILE_ID}&export=download"
    headers = {}

    # Handle HTTP Range request for partial content
    range_header = request.headers.get('Range', None)
    if range_header:
        range_values = range_header.replace("bytes=", "").split("-")
        start = int(range_values[0])
        headers['Range'] = f"bytes={start}-"
    else:
        start = 0

    # Fetch video stream from Google Drive
    drive_response = requests.get(google_drive_url, headers=headers, stream=True)
    if drive_response.status_code not in [200, 206]:
        return Response("Failed to fetch video from Google Drive", status=drive_response.status_code)

    # Relay the Google Drive video stream to the client
    response = Response(
        drive_response.iter_content(chunk_size=1024),
        status=206 if range_header else 200,
        content_type="video/mp4",
    )
    content_range = drive_response.headers.get("Content-Range")
    if content_range:
        response.headers["Content-Range"] = content_range
    response.headers["Accept-Ranges"] = "bytes"
    return response


if __name__ == '__main__':
    app.run(port=8000, debug=True)
