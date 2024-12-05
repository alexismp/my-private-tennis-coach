from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict, Any
import json

def save_transcript_to_file(transcript: List[Dict[str, Any]], filename: str) -> None:
    """Saves a transcript to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, indent=4, ensure_ascii=False)  # Save as JSON with pretty printing
        print(f"Transcript saved to: {filename}")
    except Exception as e:
        print(f"Error saving transcript to {filename}: {e}")

def transcribe_youtube_videos(video_urls: List[str]) -> List[Dict[str, Any]]:
    """
    Transcribes a list of YouTube video URLs.

    Args:
        video_urls: A list of YouTube video URLs.

    Returns:
         A list of dictionaries, where each dictionary represents the transcript of a video.
         Each dictionary contains a list of phrases, each with 'text' and 'start' timestamps.
         Returns an empty list if transcription fails for a video  (e.g., no captions).

    """
    all_transcripts = []
    for url in video_urls:
        try:
            video_id = extract_video_id(url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            all_transcripts.append(transcript)
            print(f"Successfully transcribed: {url}") #useful feedback
        except Exception as e:
            print(f"Error transcribing {url}: {e}")
            all_transcripts.append([]) # Add an empty list to maintain index consistency.

    return all_transcripts


def extract_video_id(url: str) -> str:
  """Extracts the video ID from a YouTube URL."""
  if "v=" in url:
      return url.split("v=")[1].split("&")[0] #handles most common cases
  elif "youtu.be/" in url:
      return url.split("youtu.be/")[1].split("?")[0] #handles short URLs
  else:
        raise ValueError(f"Invalid YouTube URL: {url}")

def get_text_from_transcript(transcript: List[Dict[str, Any]]) -> str:
    """Extracts only the text content from a transcript."""

    text = ""
    for phrase in transcript:
      text += f"{phrase['text']} " #concatenate each phrase to a new text string with a space at the end
    return text.strip()

def load_video_urls_from_file(filename: str) -> List[str]:
    print(f"Loading video urls from file... {filename}")
    try:
        with open(filename, 'r') as f:
            video_urls = [line.strip() for line in f]
        return video_urls
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []  # Return an empty list if the file is not found
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

video_urls = load_video_urls_from_file("coaching-urls.txt")

#     "https://www.youtube.com/watch?v=UbsUXp-9wXo",
#     "https://www.youtube.com/watch?v=WCYy6f_byRc",
#     "https://www.youtube.com/watch?v=eeiceG_UIYs",
#     "https://www.youtube.com/watch?v=yYkhkcrFeZk",
#     "https://www.youtube.com/watch?v=_ZEV0dmBTzM",
#     "https://www.youtube.com/watch?v=gT6g4QjDLBg",
#     "https://www.youtube.com/watch?v=QJDjKNEeWGU"
# ]


if video_urls:
    transcripts = transcribe_youtube_videos(video_urls)

    for i, transcript in enumerate(transcripts):
        if transcript:
            text = get_text_from_transcript(transcript)  # Get just the text
            video_id = extract_video_id(video_urls[i])
            text_filename = f"{video_id}_text.txt"
            try:
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Text saved to: {text_filename}")
            except Exception as e:
                print(f"Error saving text to {text_filename}: {e}")

        else:
            print(f"No transcript found for video {video_urls[i]}")
else:
    print("No video URLs loaded. Exiting.")
