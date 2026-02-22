import streamlit as st
from PIL import Image
from reel import call_gemini_for_reels
import time
import base64

st.markdown(
    """
    <h1 style='text-align:center; font-size:48px; margin:10px 0px; color:black;'>
        LyricsLab
    </h1>
    <p style='text-align:center; color:#555; margin:0px 0px 15px 0px; font-size:18px;'>
        Find Bollywood lyrics matching your emotions
    </p>
    """,
    unsafe_allow_html=True
)
# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="LyricsLab",
    page_icon=None,
    layout="centered"
)
# ---------- BACKGROUND IMAGE FUNCTION ----------
def set_bg_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* White transparent overlay */
    .main {{
        background-color: rgba(255, 255, 255, 0.75);
        padding: 20px;
        border-radius: 15px;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

# 👇 Background call
set_bg_image("background.jpg")
# ---------- TITLE ----------
st.markdown("""
<style>

/* Horizontal radio spacing reduce */
div[role="radiogroup"] > label {
    margin-right: 4px !important;   /* default karta ochhu */
}

/* Label text spacing tight */
div[role="radiogroup"] label p {
    margin: 0px !important;
}

/* Whole radio section niche no gap ochho */
.stRadio {
    margin-bottom: 0.3rem !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- KEYWORDS ----------
st.subheader("Search or Select Lyrics Keywords")

keywords = ["Birthday", "Anniversary", "Love", "Holi", "Friendship", "Baby Shower"]

if "selected_keyword" not in st.session_state:
    st.session_state.selected_keyword = ""

keyword_text = st.text_input(
    "", 
    value=st.session_state.selected_keyword,
    placeholder="Example: love, wedding, memories"
)

cols = st.columns(3)

for i, key in enumerate(keywords):
    with cols[i % 3]:
        if st.button(key, use_container_width=True):
            if keyword_text:
                st.session_state.selected_keyword = keyword_text + ", " + key
            else:
                st.session_state.selected_keyword = key
            st.rerun()

# ---------- DURATION ----------
st.markdown(
    "<h3 style='margin-bottom:0px;'>Lyrics Duration</h3>",
    unsafe_allow_html=True
)
duration = st.radio(
    "", ["10 sec", "20 sec", "30 sec"],
    horizontal=True
)

# ---------- IMAGE UPLOAD ----------
st.subheader("Upload Images (Max 5)")

uploaded_files = st.file_uploader(
    "",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# ---------- IMAGE PREVIEW ----------
if uploaded_files:
    st.markdown("Selected Images")
    cols = st.columns(len(uploaded_files))
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        cols[i].image(img, use_container_width=True)

# ---------- GENERATE BUTTON ----------
if st.button("Generate Lyrics", use_container_width=True):

    if not keyword_text:
        st.warning("Please enter at least one keyword.")

    elif not uploaded_files:
        st.warning("Please upload at least 1 image.")

    elif len(uploaded_files) > 5:
        st.error("Maximum 5 images allowed.")

    else:

        if "api_calls" not in st.session_state:
            st.session_state.api_calls = []

        current_time = time.time()

        # remove calls older than 60 seconds
        st.session_state.api_calls = [
            t for t in st.session_state.api_calls
            if current_time - t < 60
        ]

        if len(st.session_state.api_calls) >= 5:
            st.error("API limit reached. Please wait before generating again.")
            st.stop()

        pil_images = [Image.open(f) for f in uploaded_files[:5]]

        with st.spinner("Processing..."):
            try:
                results = call_gemini_for_reels(pil_images, keyword_text, duration)
            except ValueError as e:
                st.error(str(e))
                st.stop()

        st.session_state.api_calls.append(current_time)

        st.markdown(f"## {results[0]['reel_name']}")
        st.markdown(f"### {results[0]['song_title']}")
        st.markdown("Lyrics")
        st.write(results[0]["lyrics"])