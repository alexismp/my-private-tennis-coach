from typing import List, Dict, Any
import functions_framework
from google.cloud import storage
import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

@functions_framework.http
def extract_principles(request):
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

    bucket_name = "tennis-expertise-bucket"
    full_transcripts = gather_all_transcripts(bucket_name)
    # check for error before proceeding
    principles = get_principles_from_llm(full_transcripts)
    print(principles)
    return principles

def gather_all_transcripts(bucket_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        all_text = ""
        blobs = bucket.list_blobs() # No need to iterate, list_blobs fetches all
        for blob in blobs:
            if blob.name.endswith("_transcript.txt"):
                text = blob.download_as_text()
                all_text += text + "\n"
        print(all_text)
        return all_text

    except Exception as e:
        return "Error processing files: {e}"


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


def get_principles_from_llm(full_transcripts):
    key = getSecretKey()
    genai.configure(api_key=key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type = content.Type.OBJECT,
            enum = [],
            required = ["top_5_tennis_principles"],
            properties = {
            "top_5_tennis_principles": content.Schema(
                type = content.Type.ARRAY,
                items = content.Schema(
                type = content.Type.OBJECT,
                enum = [],
                required = ["principle", "description"],
                properties = {
                    "principle": content.Schema(
                    type = content.Type.STRING,
                    description = "The tennis principle itself.",
                    ),
                    "description": content.Schema(
                    type = content.Type.STRING,
                    description = "A detailed explanation of the principle.",
                    ),
                },
                ),
            ),
            },
        ),
        "response_mime_type": "application/json",
    }

    instructions = (
        "You are a tennis coach with extensive experience and are able to turn "
        "transcripts from coaching sessions into a list of 5 top principles that "
        "tennis players should follow to improve their game and get better results. "
        "These principles should be stats-related, not about how to play a "
        "specific point or how to hit the ball or anything technique-related."
        "Make sure to avoid duplicate principles such two focusing on first serves."
        "Do not suggest principles that are related to placement on the court."
        "Give each principle a really catchy name."
    )


    exp = genai.GenerativeModel(
        model_name="gemini-exp-1121",
        generation_config=generation_config,
        system_instruction=instructions,
    )

    pro = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction=instructions,
    )

    flash = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=instructions,
    )

    chat_session = exp.start_chat(
        history=[
        ]
    )

    response = chat_session.send_message(full_transcripts)

    print(response)

    return response.text
    # return '{"top_5_tennis_principles": [{"description": "Focus on hitting a high percentage of first serves in the box rather than going for aces to maintain a consistent serve and improve your chances of holding serve.", "principle": "Prioritize First Serve Percentage over Aces"}, {"description": "When returning serve, pre-plan your returns and aim them down the center of the court to increase consistency and reduce the angles available to your opponent, especially against serve-and-volley players.", "principle": "Target Center of the Court on Returns"}, {"description": "Maintain a higher net clearance on groundstrokes to reduce errors, hit deeper shots, and control rallies more effectively.  Avoid hitting too low over the net, which often results in short balls that your opponent can attack.", "principle": "Maintain a High Net Clearance on Groundstrokes"}, {"description": "When approaching the net, hit your volleys short and angled to make it difficult for your opponent to reach the ball, increasing your chances of winning the point. Avoid hitting volleys deep, which gives your opponent more time to react.", "principle": "Hit Short, Angled Volleys at the Net"}, {"description": "When your opponent approaches the net, use a two-shot passing shot strategy by first hitting a low ball down the middle to force a weak volley, and then following up with a more comfortable passing shot on the second ball.", "principle": "Utilize the Two-Shot Passing Shot Strategy"}]}'
