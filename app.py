import streamlit as st
import random
from PIL import Image
from reel import call_gemini_for_reels

st.title("🎬 AI Reel Generator")

# ---------- TEMPLATE SEARCH ----------

keywords = ["Birthday", "Anniversary", "Love", "Holi", "Friendship", "Baby Shower"]

if "selected_template" not in st.session_state:
    st.session_state.selected_template = ""

cols = st.columns(len(keywords))

for i, key in enumerate(keywords):
    if cols[i].button(key):
        st.session_state.selected_template = key

template_text = st.text_input(
    "Template",
    value=st.session_state.selected_template,
    placeholder="Type custom reel idea..."
)

# ---------- IMAGE UPLOAD ----------
uploaded_files = st.file_uploader(
    "Upload Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# ---------- SUBMIT ----------
if st.button("Generate Reel"):

    if not uploaded_files or len(uploaded_files) < 4:
        st.error("Upload at least 3 images.")
        st.stop()

    # Convert to PIL
    pil_images = [Image.open(f) for f in uploaded_files]

    # Random shuffle
    # random.shuffle(pil_images)
    
    # Split → 4-5 images per reel
    reels = []
    i = 0
    while i < len(pil_images):
        reels.append(pil_images[i:i+5])
        i += 5

    st.write(f"🎞 Creating {len(reels)} reels...")

    # ---------- CALL BACKEND ----------
    results = call_gemini_for_reels([pil_images], template_text)

    st.success("✅ Reel generation completed")
    st.json(results)