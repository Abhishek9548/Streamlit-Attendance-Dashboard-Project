
# SnapTend (Cloud) quick start

This repo contains a cloud-friendly Streamlit page that uses the browser camera instead of `cv2.VideoCapture(0)`.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app_cloud.py
```

## Deploy to Streamlit Community Cloud
- Set **Main file path** to `Attendance-Dashboard-main/app_cloud.py`
- Ensure the app has `requirements.txt` with at least: streamlit, opencv-python-headless, pillow, pandas, numpy
- Grant the camera permission in your browser when prompted.

## Notes
- Avoid `win32com` SAPI voice on Linux-based cloud.
- If you need continuous video, use `streamlit-webrtc` instead of `cv2.VideoCapture(0)`.
