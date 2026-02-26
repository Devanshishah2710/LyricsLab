# 🎬 LycricsLab


An AI-powered Instagram Reel Generator that analyzes uploaded images and selects the **most suitable Bollywood song with exact real lyrics** using Google Gemini.

Built with ❤️ using Streamlit + Gemini API

---

## 📌 Project Overview

This application allows users to:

- Upload up to 5 images
- Select or enter a reel theme
- Choose reel duration
- Generate a perfectly matched Bollywood song
- Get exact original lyrics (no AI-generated fake lyrics)
- Receive clean JSON output

All images are treated as **ONE reel story**, and AI selects only **one best matching song**.

---

# ✨ Features

## 🔎 Smart Keyword System
- Predefined theme buttons:
  - Birthday
  - Anniversary
  - Love
  - Holi
  - Friendship
  - Baby Shower
- Custom keyword input option
- One-click theme selection

## ⏱ Duration Selection
- 10 seconds
- 20 seconds
- 30 seconds
- Lyrics length approximately matches duration

## 🖼 Image Handling
- Upload up to 5 images
- Live preview before submission
- All images analyzed together as one reel

## 🤖 AI Processing
- Uses `gemini-2.5-flash`
- Understands overall mood of images
- Matches song with theme + mood
- Returns exact real Bollywood lyrics
- Avoids repeating same song

## 📦 Clean Output
- Returns raw valid JSON only
- No extra explanation
- Ready for backend/video pipeline use

---

# 🛠 Tech Stack

- Python
- Streamlit
- Google Generative AI (Gemini)
- Pillow
- python-dotenv

---

# 📂 Project Structure
├── app.py # Streamlit Frontend
├── reel.py # Gemini Backend Logic
├── .env # API Key (Not pushed)
├── requirements.txt
└── README.md


## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/your-repository-name.git
cd your-repository-name
```

# Windows
```
python -m venv venv
venv\Scripts\activate
```

# Mac 

```
python3 -m venv venv
source venv/bin/activate 
```

# If requirements.txt exists:

```
pip install -r requirements.txt
```

# install manually:

```
pip install streamlit google-generativeai pillow python-dotenv
```

# create a .env file in the root directory:

```
apikey=YOUR_GEMINI_API_KEY
```

```
.env
venv/
__pycache__/
```

# Run the Application
```
python -m streamlit run app.py
```
