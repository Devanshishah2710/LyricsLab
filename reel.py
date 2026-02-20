import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")
genai.configure(api_key=api_key)

PROMPT_BASE = """
You will receive multiple images.
All images together represent ONE Instagram reel.

Your task:
Identify ONE perfect Bollywood song (Hindi) that best fits ALL images.

CRITICAL INSTRUCTION FOR LYRICS:
- You MUST quote the EXACT, REAL, existing lyrics from the original Bollywood song.
- Do NOT generate or modify lyrics.
- If unsure about exact lyrics, choose another song.
- Lyrics must match ALL provided keywords.
- Lyrics length should approximately match the requested duration.
- Do NOT include explanations.

Return ONLY valid raw JSON in this format:

[
  {
    "reel_name": "Short reel name based on keywords",
    "reel_number": 1,
    "song_title": "Song Title - Movie Name",
    "lyrics": "Exact real lyrics"
  }
]
"""

def call_gemini_for_reels(pil_images, keyword, duration):

    content = [
        PROMPT_BASE
        + f"\nReel theme keywords: {keyword}"
        + f"\nRequested reel duration: {duration}"
    ]

    content.extend(pil_images)

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(content)

    clean_text = re.sub(r"```json|```", "", response.text).strip()
    match = re.search(r"\[.*\]", clean_text, re.DOTALL)

    if not match:
        raise ValueError("JSON not found in Gemini response")

    return json.loads(match.group(0))