# main.py
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript,
)
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# -------------------------------
#  Configure Gemini API
# -------------------------------
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

# -------------------------------
#  Extract Video ID
# -------------------------------
def extract_video_id(url: str):
    """Extracts YouTube video ID from any valid YouTube URL format."""
    patterns = [
        r"(?:v=)([a-zA-Z0-9_-]{11})",
        r"(?:be/)([a-zA-Z0-9_-]{11})",
        r"(?:embed/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# -------------------------------
#  Fetch Transcript (NEW API USAGE)
# -------------------------------
def get_youtube_transcript(video_id: str):
    """
    Fetch transcript and auto-translate to English when needed.
    Returns a user-friendly error message if transcript is not available.
    """
    try:
        yt = YouTubeTranscriptApi()
        fetched = yt.fetch(video_id, languages=['en', 'hi'])  # fetch English or Hindi
        # Convert fetched transcript to full text
        full_text = " ".join([snippet.text for snippet in fetched])
        return full_text

    except TranscriptsDisabled:
        return "Transcript is disabled for this video."

    except NoTranscriptFound:
        return "No transcript available for this video."

    except CouldNotRetrieveTranscript:
        return "Could not retrieve transcript. YouTube may have blocked the request."

    except Exception as e:
        return f"Unexpected error fetching transcript: {str(e)}"

# -------------------------------
#  Summarize Text (Gemini)
# -------------------------------
def summarize_text(text: str, summary_type: str = "concise"):
    """Summarizes text using Gemini model."""
    try:
        if summary_type == "concise":
            prompt = f"Summarize this text in 3-5 sentences:\n\n{text}\n\nSummary:"
        elif summary_type == "detailed":
            prompt = f"Give a detailed bullet point summary of this text:\n\n{text}\n\nBullet Summary:"
        elif summary_type == "key_points":
            prompt = f"Extract key points from this text:\n\n{text}\n\nKey Points:"
        else:
            prompt = f"Summarize this text:\n\n{text}"

        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        raise Exception(f"Gemini summarization error: {str(e)}")

# -------------------------------
#  ROUTES
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# --------- API: Only Transcript ----------
@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    try:
        data = request.json
        url = data.get("url", "").strip()
        if not url:
            return jsonify({"error": "URL is required"}), 400

        video_id = extract_video_id(url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        transcript = get_youtube_transcript(video_id)
        return jsonify({
            "success": True,
            "video_id": video_id,
            "transcript": transcript
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------- API: Only Summary ----------
@app.route("/api/summarize", methods=["POST"])
def summarize():
    try:
        data = request.json
        text = data.get("text", "").strip()
        summary_type = data.get("type", "concise")

        if not text:
            return jsonify({"error": "Text is required"}), 400

        if len(text) > 10000:
            text = text[:10000]

        summary = summarize_text(text, summary_type)
        return jsonify({"success": True, "summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------- API: Combined Transcript + Summary ----------
@app.route("/api/transcribe-and-summarize", methods=["POST"])
def transcribe_and_summarize():
    try:
        data = request.json
        url = data.get("url", "").strip()
        summary_type = data.get("type", "concise")

        if not url:
            return jsonify({"error": "URL is required"}), 400

        video_id = extract_video_id(url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        transcript = get_youtube_transcript(video_id)
        summary = summarize_text(transcript, summary_type)

        return jsonify({
            "success": True,
            "video_id": video_id,
            "transcript": transcript,
            "summary": summary
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
#  Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
