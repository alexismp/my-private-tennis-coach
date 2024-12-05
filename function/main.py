from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict, Any
import json
import functions_framework
from google.cloud import storage

def save_transcript_to_file(transcript: List[Dict[str, Any]], filename: str, bucket_name: str) -> None:
    """Saves a transcript to a JSON file in Cloud Storage."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(json.dumps(transcript, indent=4, ensure_ascii=False), content_type='application/json')
        print(f"Transcript saved to: gs://{bucket_name}/{filename}")
    except Exception as e:
        print(f"Error saving transcript to gs://{bucket_name}/{filename}: {e}")

def transcribe_youtube_videos(video_urls: List[str], bucket_name: str) -> None:
    """
    Transcribes a list of YouTube video URLs and saves them to Cloud Storage.
    """
    for url in video_urls:
        try:
            video_id = extract_video_id(url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_filename = f"{video_id}_transcript.json"
            save_transcript_to_file(transcript, transcript_filename, bucket_name)

            text = get_text_from_transcript(transcript)
            text_filename = f"{video_id}_text.txt"
            save_text_to_file(text, text_filename, bucket_name)

            print(f"Successfully transcribed: {url}")
        except Exception as e:
            print(f"Error transcribing {url}: {e}")


def extract_video_id(url: str) -> str:
  """Extracts the video ID from a YouTube URL."""
  # ... (same as original code)

def get_text_from_transcript(transcript: List[Dict[str, Any]]) -> str:
    """Extracts only the text content from a transcript."""
    # ... (same as original code)

def save_text_to_file(text: str, filename: str, bucket_name: str) -> None:
    """Saves text content to a file in Cloud Storage."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(text, content_type='text/plain')
        print(f"Text saved to: gs://{bucket_name}/{filename}")
    except Exception as e:
        print(f"Error saving text to gs://{bucket_name}/{filename}: {e}")

def load_video_urls_from_gcs(bucket_name: str, filename: str) -> List[str]:
    """Loads video URLs from a file in Cloud Storage."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        content = blob.download_as_text()
        video_urls = [line.strip() for line in content.splitlines()]
        return video_urls
    except Exception as e:
        print(f"Error loading URLs from gs://{bucket_name}/{filename}: {e}")
        return []


#def process_video_urls(data, context):
def process_video_urls(cloud_event):
    """Cloud Function triggered by finalize event in Cloud Storage."""
    data = cloud_event.data

    bucket_name = data['bucket']
    file_name = data['name']


    if file_name == 'coaching-urls.txt':  # Check if the uploaded file is the URL list
        video_urls = load_video_urls_from_gcs(bucket_name, 'coaching-urls.txt')
        if video_urls:
            transcribe_youtube_videos(video_urls, bucket_name)
        else:
            print("No video URLs loaded. Exiting.")





# # Triggered by a change in a storage bucket
# @functions_framework.cloud_event
# def hello_gcs(cloud_event):
#     data = cloud_event.data

#     event_id = cloud_event["id"]
#     event_type = cloud_event["type"]

#     bucket = data["bucket"]
#     name = data["name"]
#     metageneration = data["metageneration"]
#     timeCreated = data["timeCreated"]
#     updated = data["updated"]

#     print(f"Event ID: {event_id}")
#     print(f"Event type: {event_type}")
#     print(f"Bucket: {bucket}")
#     print(f"File: {name}")
#     print(f"Metageneration: {metageneration}")
#     print(f"Created: {timeCreated}")
#     print(f"Updated: {updated}")
