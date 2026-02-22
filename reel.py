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

Rules:

1. Select ONLY ONE real existing Bollywood Hindi song.
2. Song MUST strongly match the given keywords.
3. Song MUST logically match emotional tone of ALL images.
4. Return short lyrics inspired by the song mood.
5. Keep lyrics under requested duration.
6. No explanations.

Reel theme keywords: {keyword}
Requested reel duration: {duration}

Return ONLY valid raw JSON in this format:

[
  {{
    "reel_name": "Short descriptive reel name",
    "reel_number": 1,
    "song_title": "Song Title - Movie Name",
    "lyrics": "Generated short lyrics"
  }}
]
"""

def call_gemini_for_reels(pil_images, keyword, duration):

    final_prompt = PROMPT_BASE.format(
        keyword=keyword,
        duration=duration
    )

    content = [final_prompt]
    content.extend(pil_images)

    model = genai.GenerativeModel("gemini-2.5-flash")

    try:
        response = model.generate_content(content)
    except Exception as e:
        if "quota" in str(e).lower() or "limit" in str(e).lower():
            raise ValueError("Daily API limit completed.")
        else:
            raise e

    clean_text = re.sub(r"```json|```", "", response.text).strip()
    match = re.search(r"\[.*\]", clean_text, re.DOTALL)

    if not match:
        raise ValueError("Valid JSON not found in response")

    return json.loads(match.group(0))