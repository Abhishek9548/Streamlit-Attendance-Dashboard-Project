
import streamlit as st
import pandas as pd
import numpy as np
import cv2
from datetime import datetime
from io import BytesIO
from PIL import Image
import os

st.set_page_config(page_title="SnapTend (Cloud) - Camera Attendance", page_icon="📷", layout="centered")

st.title("📷 SnapTend (Cloud) — Browser Camera Attendance")

st.info(
    "This cloud-friendly page uses your **browser camera**. "
    "It avoids `cv2.VideoCapture(0)` and Windows-only voice APIs so it works on Streamlit Community Cloud."
)

# Configuration
attendance_csv = "attendance_cloud.csv"
os.makedirs("data", exist_ok=True)

# Optional: load a face detector (pack a haarcascade in the repo at 'models/haarcascade_frontalface_default.xml')
CASCADE_PATH = "models/haarcascade_frontalface_default.xml"
face_cascade = None
if os.path.exists(CASCADE_PATH):
    try:
        face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    except Exception:
        face_cascade = None

# Utility: append to CSV
def append_attendance(name: str):
    ts = datetime.now()
    row = {"NAME": name, "DATE": ts.strftime("%d-%m-%Y"), "TIME": ts.strftime("%H:%M:%S")}
    write_header = not os.path.exists(attendance_csv)
    with open(attendance_csv, "a", encoding="utf-8") as f:
        if write_header:
            f.write("NAME,DATE,TIME\n")
        f.write(f'{row["NAME"]},{row["DATE"]},{row["TIME"]}\n')
    return row

# Simulated recognizer placeholder (replace with your embedding/KNN pipeline)
def recognize_person(img_bgr: np.ndarray) -> str:
    # TODO: integrate your face embeddings + classifier here.
    # For now, return "Unknown" if no face detected, otherwise "Person"
    if face_cascade is None:
        return "Person"
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    return "Person" if len(faces) > 0 else "Unknown"

with st.form("capture_form"):
    image_data = st.camera_input("Open your camera and take a photo")
    name_override = st.text_input("(Optional) Override recognized name", value="", help="Leave blank to use auto-recognition.")
    submitted = st.form_submit_button("Submit Attendance")

if submitted:
    if image_data is None:
        st.error("Please take a photo first.")
    else:
        # Read image bytes and convert to OpenCV BGR
        img = Image.open(image_data)
        img_rgb = np.array(img.convert("RGB"))
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

        # Recognize
        name = name_override.strip() or recognize_person(img_bgr)
        record = append_attendance(name)

        st.success(f"Attendance saved for **{record['NAME']}** at {record['TIME']} on {record['DATE']}.")
        st.dataframe(pd.read_csv(attendance_csv))
        st.image(img_rgb, caption="Captured frame", use_column_width=True)

st.divider()
st.caption("Tip: For continuous video scanning, use the `streamlit-webrtc` package on cloud, not `cv2.VideoCapture(0)`.")
