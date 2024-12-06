from google.cloud import storage
from typing import List, Dict, Any
import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

def get_coaching_urls():
    """Reading URLs from a GCS file."""
    try:
        bucket_name = "tennis-expertise-bucket"
        file_name = "coaching-urls.txt"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        content = blob.download_as_string().decode("utf-8")  # Decode to string

        urls = [line.strip() for line in content.splitlines() if line.strip()]  # Remove empty lines
        print (urls)
        return {"urls": urls}, 200, {'Content-Type': 'application/json'} 

    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return {"error": str(e)}, 500, {'Content-Type': 'application/json'}

def getSecretKey():
    # Secret mounted as a volume: /key/gemini-key
    try:
        with open('/key/gemini-key', 'r') as f:
            key = f.read().strip()  # Read and remove leading/trailing whitespace
            return key
    except FileNotFoundError:
        key = None  # Handle the case where the file isn't found
        print("Error: /key file not found.")
    except Exception as e:
        key = None
        print(f"An error occurred while reading /key: {e}")
        