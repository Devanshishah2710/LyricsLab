import streamlit as st
import time
from PIL import Image
from reel import call_gemini_with_images   # backend import

st.title("🎵 Image to Bollywood Song Matcher")

uploaded_files = st.file_uploader(
    "Upload 9 Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if st.button("Submit"):

    if uploaded_files and len(uploaded_files) == 9:

        all_results = []

        # Convert uploaded files → PIL
        pil_images = [Image.open(file) for file in uploaded_files]

        # Process in batches of 3
        for i in range(0, 9, 3):

            batch = pil_images[i:i+3]

            st.write(f"🚀 Processing Batch {i//3 + 1}...")

            # Backend function call
            results = call_gemini_with_images(batch)

            # ✅ Replace index with filename
            for j, item in enumerate(results):
                item["filename"] = uploaded_files[i + j].name
                item.pop("image_index", None)  # remove old index
                all_results.append(item)

            # Wait between API calls (except last)
            if i < 6:
                st.write("⏳ Waiting 1 minute before next API call...")
                time.sleep(60)

        st.success("✅ All 9 Images Processed")
        st.json(all_results)

    else:
        st.error("Please upload exactly 9 images.")