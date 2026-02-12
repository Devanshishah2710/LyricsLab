import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# ✅ correct env variable use
genai.configure(api_key=os.getenv("apikey"))

PROMPT = """
Analyze the attached 3 images.
For EACH image, identify the perfect Bollywood song (Hindi).

CRITICAL INSTRUCTION FOR LYRICS:
- You MUST quote the EXACT EXISTING lyrics from the real song.
- Do NOT write lyrics based on what you see in the image (e.g., if there is a horse, do not write lyrics about horses unless the real song has them).
- If you don't know the exact lyrics, choose a different song.

Return result as a JSON array with exactly 3 objects:
[
  {
    "image_index": 1, 
    "song_title": "Title - Movie",
    "lyrics": "Real lyrics here (Hindi/Hinglish)"
  }
]
Output ONLY raw JSON.
"""

def call_gemini_with_images(pil_images):

    content_payload = [PROMPT] + pil_images
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(content_payload)

    # ✅ robust JSON extraction
    clean_text = re.sub(r"```json|```", "", response.text).strip()
    match = re.search(r"\[.*\]", clean_text, re.DOTALL)

    if not match:
        raise ValueError("JSON not found in Gemini response")

    return json.loads(match.group(0))