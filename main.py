import streamlit as st
from supabase import create_client
import time

# --- Connect Supabase ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("MiniTube Upload 🚀")

# --- Upload UI ---
video_file = st.file_uploader("Choose a video", type=["mp4", "mov", "avi"])
title = st.text_input("Video title")

if st.button("Upload Video"):

    if video_file is None:
        st.warning("Please select a video first 🎥")
    elif title.strip() == "":
        st.warning("Please enter a title ✍️")
    else:
        try:
            # unique filename (prevents overwrite)
            filename = f"{int(time.time())}_{video_file.name}"

            # 1. Upload to Supabase Storage bucket "videos"
            supabase.storage.from_("videos").upload(
                filename,
                video_file.read(),
                {
                    "content-type": video_file.type
                }
            )

            # 2. Get public URL
            video_url = supabase.storage.from_("videos").get_public_url(filename)

            # 3. Save metadata in database
            supabase.table("videos").insert({
                "title": title,
                "video_url": video_url
            }).execute()

            st.success("Upload successful 🚀 Your video is now live!")

        except Exception as e:
            st.error(f"Upload failed: {e}")
