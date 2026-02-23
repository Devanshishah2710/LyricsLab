# import google.generativeai as genai
# import os
# import json
# import re
# from dotenv import load_dotenv

# load_dotenv(dotenv_path=".env")
# api_key = os.getenv("GOOGLE_API_KEY")

# if not api_key:
#     raise ValueError("GOOGLE_API_KEY not found")

# genai.configure(api_key=api_key)

# PROMPT_BASE = """
# You will receive multiple images.
# All images together represent ONE Instagram reel.

# Your task:
# Identify ONE perfect Bollywood song (Hindi) that best fits ALL images.

# CRITICAL INSTRUCTION FOR LYRICS:
# - You MUST quote the EXACT, REAL, existing lyrics from the original Bollywood song.
# - Do NOT generate or modify lyrics.
# - If unsure about exact lyrics, choose another song.
# - Lyrics must match ALL provided keywords.
# - Do NOT include explanations.

# Reel theme keywords: {keyword}
# Requested reel duration: {duration}

# Return ONLY valid raw JSON in this format:

# [
#   {{
#     "reel_name": "Short reel name based on keywords",
#     "reel_number": 1,
#     "song_title": "Song Title - Movie Name",
#     "lyrics": "Exact real lyrics"
#   }}
# ]
# """
# def call_gemini_for_reels(pil_images, keyword, duration):

#     final_prompt = PROMPT_BASE.format(
#         keyword=keyword,
#         duration=duration
#     )

#     content = [final_prompt]
#     content.extend(pil_images)

#     model = genai.GenerativeModel("gemini-2.5-flash")

#     try:
#         response = model.generate_content(content)
#     except Exception as e:
#         if "quota" in str(e).lower() or "limit" in str(e).lower():
#             raise ValueError("Daily API limit completed.")
#         else:
#             raise e

#     clean_text = re.sub(r"```json|```", "", response.text).strip()
#     match = re.search(r"\[.*\]", clean_text, re.DOTALL)

#     if not match:
#         raise ValueError("Valid JSON not found in response")

#     return json.loads(match.group(0)) 








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
- The lyrics can be slightly shorter than the requested duration (e.g., 28–29 seconds for a 30-second reel).
- The lyrics must feel complete and not abruptly stopped.

Output requirements:
- Return ONLY valid raw JSON.
- Return one object per reel in a JSON array.
- Do NOT include explanations, markdown, or extra text.

Reel theme keywords: {keyword}
Requested reel duration: {duration}

JSON format:
[
  {{
    "reel_name": "Short descriptive reel name based on keywords",
    "reel_number": 1,
    "song_title": "Song Title - Movie Name",
    "lyrics": "Exact real lyrics in Hindi or Hinglish"
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
