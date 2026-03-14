from flask import Flask, request, jsonify
from transcript import get_transcript
from summarizer import summarize_text
from cache_manager import load_from_cache, save_to_cache


app = Flask(__name__)


@app.route("/")
def home():
    return "Backend running!"


@app.route("/summarize")
def summarize_route():
    video_id = request.args.get("video_id")
    length = request.args.get("length", "medium")
    if length == "short":
        max_len = 80
        min_len = 30
        top_ratio = 0.4
    elif length == "long":
        max_len = 300
        min_len = 150
        top_ratio = 0.6
    else:
        max_len = 150
        min_len = 60
        top_ratio = 0.5

    if not video_id:
        return "Missing video_id parameter", 400

    try:
        cached_result = load_from_cache(video_id, length)
        if cached_result:
            print("Cache hit!")
            return jsonify(cached_result)
        
        transcript = get_transcript(video_id)
        summary = summarize_text(transcript, max_summary_length=max_len, min_summary_length=min_len, top_ratio=top_ratio)
        save_to_cache(video_id, length, summary)
        return jsonify(summary) 
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(debug=True)