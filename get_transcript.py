from youtube_transcript_api import YouTubeTranscriptApi as scriptapi
from youtube_transcript_api.formatters import TextFormatter as format
import re
from datetime import timedelta


def get_video_id(url):
    # Handle standard watch?v= links
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]

    # Handle youtu.be short links
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]

    # Handle /live/ links
    elif "youtube.com/live/" in url:
        return url.split("youtube.com/live/")[-1].split("?")[0]

    # Regex fallback
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)

    raise ValueError("Invalid YouTube URL format")


def format_time(seconds):
    """Convert seconds to hh:mm:ss format"""
    return str(timedelta(seconds=int(seconds)))


def transcript(url):
    try:
        video_id = get_video_id(url)
        print(f"[DEBUG] Extracted Video ID: {video_id}")
        
        # Get available transcripts
        transcript_list = scriptapi.list_transcripts(video_id)

        # Try to fetch manually created English transcript
        try:
            transcript_obj = transcript_list.find_manually_created_transcript(['en'])
            print("[INFO] Using manually created English transcript.")
        except:
            # Fallback: use auto-generated English transcript
            transcript_obj = transcript_list.find_generated_transcript(['en'])
            print("[INFO] Using auto-generated English transcript.")

        transcript_data = transcript_obj.fetch()

        with open("data/transcript.txt", 'w', encoding='utf-8') as f:
            for entry in transcript_data:
                start_time = entry.start
                formatted_time = format_time(start_time)
                text = entry.text
                f.write(f"{formatted_time} : {text}\n")

        print("Transcript saved.")

    except Exception as e:
        print(f"Error: {e}")


video_url = input("Paste the YouTube video URL: ")
transcript(video_url)
