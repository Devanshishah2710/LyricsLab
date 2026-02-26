import streamlit as st
from PIL import Image
from reel import call_gemini_for_reels
import time
import base64

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="LyricsLab",
    layout="wide"
)


# ---------- TITLE ----------
st.markdown(
    "<h1 style='text-align:center; margin:0; font-size:42px;'>LyricsLab</h1>",
    unsafe_allow_html=True
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

    .main {{
        background-color: rgba(255, 255, 255, 0.75);
        padding: 20px;
        border-radius: 15px;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

set_bg_image("background.jpg")

# ---------- PAGE LAYOUT ----------
left_col, right_col = st.columns([1, 1], gap="large")

# ================= LEFT SIDE (INPUT) =================
with left_col:

    st.subheader("Search or Select Lyrics Keywords")

    keywords = ["Birthday", "Anniversary", "Love", "Holi", "Friendship", "Baby Shower"]

    if "selected_keyword" not in st.session_state:
        st.session_state.selected_keyword = ""

    keyword_text = st.text_input(
        "",
        value=st.session_state.selected_keyword,
        placeholder="love, wedding, memories"
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

    st.markdown("### Lyrics Duration")

    duration = st.radio(
        "",
        ["10 sec", "20 sec", "30 sec"],
        horizontal=True
    )

    st.subheader("Upload Images (Max 5)")

    uploaded_files = st.file_uploader(
        "",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    generate_btn = st.button("Generate Lyrics", use_container_width=True)

# ================= RIGHT SIDE (OUTPUT) =================
with right_col:

    st.markdown(
        "<h3 style='text-align:center; margin-bottom:15px;'>Generated Output</h3>",
        unsafe_allow_html=True
    )

    # 🔥 Show selected images instantly (only once)
    if uploaded_files:
        st.markdown("#### 🎬 Selected Reel Images")

        img_cols = st.columns(len(uploaded_files))
        for i, file in enumerate(uploaded_files[:5]):
            img = Image.open(file)
            img_cols[i].image(img, width=160)

    # 👇 Generate logic
    if generate_btn:

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

            # 🔥 Lyrics Output Card
            st.markdown("<div class='output-card'>", unsafe_allow_html=True)

            st.markdown(
                f"<h2 style='margin-bottom:5px;'>{results[0]['reel_name']}</h2>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<p style='color:#666; font-weight:600;'>{results[0]['song_title']}</p>",
                unsafe_allow_html=True
            )

            st.markdown("<hr style='margin:15px 0;'>", unsafe_allow_html=True)

            st.write(results[0]["lyrics"])

            st.markdown("</div>", unsafe_allow_html=True)