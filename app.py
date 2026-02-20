import streamlit as st
from PIL import Image
from reel import call_gemini_for_reels

st.set_page_config(
    page_title="Visual Emotion Based Bollywood Lyrics Matching System",
    page_icon="🎬",
    layout="centered"
)

st.markdown(
    """
    <h1 style='text-align: center;'>
    🎬 Visual Emotion Based Bollywood Lyrics Matching System
    </h1>
    <p style='text-align: center; color: grey;'>
    Create one perfect Bollywood reel song from your memories 💖
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------- KEYWORDS ----------
st.subheader("🔎 Search or Select Reel Keywords")

keywords = ["Birthday", "Anniversary", "Love", "Holi", "Friendship", "Baby Shower"]

if "selected_keyword" not in st.session_state:
    st.session_state.selected_keyword = ""

keyword_text = st.text_input(
    "Enter keywords (you can type multiple separated by comma)",
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

st.divider()

# ---------- DURATION ----------
st.subheader("⏱ Reel Duration")

duration = st.radio(
    "",
    ["10 sec", "20 sec", "30 sec"],
    horizontal=True
)

st.divider()

# ---------- IMAGE UPLOAD ----------
st.subheader("📸 Upload Images (Max 5)")

uploaded_files = st.file_uploader(
    "",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# ---------- IMAGE PREVIEW ----------
if uploaded_files:
    st.markdown("### 🖼 Selected Images")
    cols = st.columns(len(uploaded_files))
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        cols[i].image(img, use_container_width=True)

st.divider()

# ---------- GENERATE BUTTON ----------
if st.button("🚀 Generate Reel", use_container_width=True):

    if not keyword_text:
        st.warning("Please enter at least one keyword.")

    elif not uploaded_files:
        st.warning("Please upload at least 1 image.")

    elif len(uploaded_files) > 5:
        st.error("Maximum 5 images allowed.")

    else:
        st.success(f"{len(uploaded_files)} images selected successfully!")

        pil_images = [Image.open(f) for f in uploaded_files[:5]]

        with st.spinner("🎵 Creating your perfect Bollywood reel..."):
            results = call_gemini_for_reels(pil_images, keyword_text, duration)

        st.success("✅ Reel generation completed")

        st.markdown(f"## 🎵 {results[0]['reel_name']}")
        st.markdown(f"### 🎬 {results[0]['song_title']}")
        st.markdown("#### 🎶 Lyrics")
        st.write(results[0]["lyrics"])