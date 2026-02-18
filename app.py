import streamlit as st
from PIL import Image
from reel import call_gemini_for_reels

st.title("🎬 AI Reel Generator")

# ---------- KEYWORD SEARCH ----------
st.subheader("🔎 Search your keyword")

keywords = ["Birthday", "Anniversary", "Love", "Holi", "Friendship", "Baby Shower"]

if "selected_keyword" not in st.session_state:
    st.session_state.selected_keyword = ""

# ---- Search box FIRST ----
keyword_text = st.text_input(
    "Keyword",
    value=st.session_state.selected_keyword,
    placeholder="Type custom reel idea..."
)

# ---- Keyword buttons grid (equal & clean) ----
cols = st.columns(3, gap="medium")

for i, key in enumerate(keywords):
    col = cols[i % 3]
    with col:
        if st.button(key, use_container_width=True):
            st.session_state.selected_keyword = key
            st.rerun()

# ---------- DURATION ----------
st.subheader("⏱ Select Reel Duration")
duration = st.radio("Reel seconds", ["10 sec", "20 sec", "30 sec"], horizontal=True)

# ---------- IMAGE UPLOAD ----------
uploaded_files = st.file_uploader(
    "Upload MAX 5 Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# ---------- SINGLE PAGE IMAGE PREVIEW ----------
if uploaded_files:
    st.subheader("Selected Images")
    cols = st.columns(len(uploaded_files))
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        cols[i].image(img, use_container_width=True)

# ---------- SUBMIT ----------
if st.button("Generate Reel"):

    if not uploaded_files:
        st.warning("Please upload at least 1 image.")

    elif len(uploaded_files) > 5:
        st.error("You can select maximum 5 photos only for one reel.")

    else:
        st.success(f"{len(uploaded_files)} photos selected successfully!")

        # Convert to PIL
        pil_images = [Image.open(f) for f in uploaded_files[:5]]

        st.write("🎞 Creating 1 reel from all images...")

        # ---------- CALL BACKEND ----------
        results = call_gemini_for_reels(pil_images, keyword_text, duration)

        st.success("✅ Reel generation completed")
        st.subheader(f"🎵 {results[0]['reel_name']}")
        st.json(results)
