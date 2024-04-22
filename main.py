from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Function to get the title of a YouTube video given its URL
def get_video_title(url):
    try:
        yt = YouTube(
            url,
            use_oauth=False,
            allow_oauth_cache=True
            )
        return yt.title
    except Exception as e:
        return None

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the download request
@app.route('/download', methods=['POST'])
def download():
    try:
        # Get the URL of the video from the form submitted by the user
        url = request.form['url']
        # Get the title of the video
        title = get_video_title(url)
        if title:
            # If the title is obtained successfully, create a YouTube object
            yt = YouTube(
                url, 
                use_oauth=False,
                allow_oauth_cache=True)
            # Get the stream with the highest resolution and a file extension of mp4
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            if stream:
                # Specify the directory where the video should be saved
                directory = 'videos'
                # Create the directory if it doesn't exist
                if not os.path.exists(directory):
                    os.makedirs(directory)
                # Sanitize the filename to remove any potentially dangerous characters
                filename = secure_filename(title) + '.mp4'
                # Combine the directory and filename to get the full filepath
                filepath = os.path.join(directory, filename)
                # Download the video to the specified filepath
                stream.download(output_path=directory, filename=filename)
                # Send the downloaded file as an attachment for the user to download
                return send_file(filepath, as_attachment=True)
            else:
                return "No stream available for this video."
        else:
            return "Failed to get video title."
    except Exception as e:
        # If any error occurs during the process, return an error message
        return f"An error occurred: {str(e)}"

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)