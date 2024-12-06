from google.cloud import storage

def get_coaching_urls(request):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    """Cloud Function to read URLs from a GCS file."""
    try:
        bucket_name = "tennis-expertise-bucket"
        file_name = "coaching-urls.txt"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        content = blob.download_as_string().decode("utf-8")  # Decode to string

        urls = [line.strip() for line in content.splitlines() if line.strip()]  # Remove empty lines
        return {"urls": urls}, 200, {'Content-Type': 'application/json'} 

    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return {"error": str(e)}, 500, {'Content-Type': 'application/json'}
