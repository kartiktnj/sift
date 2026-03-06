from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_id: str) -> str:
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.fetch(video_id)

    full_text = " ".join([entry.text for entry in transcript_list])

    return full_text