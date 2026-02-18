import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("apikey"))

PROMPT_BASE = """
You will receive multiple images.
All images together represent ONE Instagram reel.

Your task:
For EACH reel (image group), identify ONE perfect Bollywood song (Hindi) that best fits ALL images in that group.

CRITICAL INSTRUCTION FOR LYRICS:
- You MUST quote the EXACT, REAL, existing lyrics from the original Bollywood song.
- Do NOT generate or modify lyrics based on the visual content.
- If you are not 100% sure about the exact real lyrics, choose a different song.
- The selected lyrics MUST meaningfully relate to the overall mood/theme of ALL images in that reel.
- Do NOT repeat the same song for different reels.
- The selected lyrics MUST also match ALL provided reel theme keywords.
- The length of the lyrics should approximately match the requested reel duration.

Output requirements:
- Return ONLY valid raw JSON.
- Return one object per reel in a JSON array.
- Do NOT include explanations, markdown, or extra text.

JSON format:
[
  {
    "reel_name": "Short descriptive reel name based on keywords",
    "reel_number": 1,
    "song_title": "Song Title - Movie Name",
    "lyrics": "Exact real lyrics in Hindi or Hinglish"
  }
]
"""

def call_gemini_for_reels(pil_images, keyword, duration):

    content = [
        PROMPT_BASE
        + f"\nReel theme keywords: {keyword}"
        + f"\nRequested reel duration: {duration}"
    ]

    # attach images
    content.extend(pil_images)

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(content)

    clean_text = re.sub(r"```json|```", "", response.text).strip()
    match = re.search(r"\[.*\]", clean_text, re.DOTALL)

    if not match:
        raise ValueError("JSON not found in Gemini response")

    return json.loads(match.group(0))
