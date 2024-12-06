from google.cloud import storage

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
