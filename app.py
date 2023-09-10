from flask import Flask, render_template
from azure.storage.blob import BlobServiceClient
import configparser

app = Flask(__name__)

# Initialize blob_service_client as None
blob_service_client = None

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Try to initialize BlobServiceClient
try:
    blob_service_client = BlobServiceClient.from_connection_string(config['Azure']['storage_connection_string'])
except Exception as e:
    print(f"Failed to initialize BlobServiceClient: {e}")

def fetch_blob_url(container_name, blob_name):
    # If blob_name is a URL, return it directly
    if blob_name.startswith("http"):
        return blob_name
    
    if blob_service_client:
        try:
            return blob_service_client.get_blob_client(container_name=container_name, blob_name=blob_name).url
        except Exception as e:
            print(f"An error occurred while fetching blob: {e}")
            return None
    return None

@app.route('/video')
def video_page():
    video_url = fetch_blob_url(config['Media']['video_container'], config['Media']['video_blob'])
    error_message = "The video content couldn't be loaded due to storage account issues." if not video_url else None
    return render_template('video.html', video_url=video_url, error_message=error_message)

@app.route('/image')
def image_page():
    image_url = fetch_blob_url(config['Media']['image_container'], config['Media']['image_blob'])
    error_message = "The image content couldn't be loaded due to storage account issues." if not image_url else None
    return render_template('image.html', image_url=image_url, error_message=error_message)

@app.route('/music')
def music_page():
    music_url = fetch_blob_url(config['Media']['music_container'], config['Media']['music_blob'])
    error_message = "The music content couldn't be loaded due to storage account issues." if not music_url else None
    return render_template('music.html', music_url=music_url, error_message=error_message)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
