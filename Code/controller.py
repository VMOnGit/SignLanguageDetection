import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import streamlit as st
from PIL import Image

# Initialize Streamlit session state
if "arr" not in st.session_state:
    st.session_state["arr"] = []

# Initialize classifier and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier(
    "G:\\Git\\Git\\SignLanguageDetection\\converted_keras\\keras_model.h5",
    "G:\\Git\\Git\\SignLanguageDetection\\converted_keras\\labels.txt"
)

offset = 20
imgSize = 300
labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Label list from A to Z

# Streamlit UI
st.title("Real-Time Sign Language Detection")
video_placeholder = st.image([])  # Placeholder for video frame
recognized_text = st.empty()       # Placeholder for displaying recognized text
final_result = st.empty()          # Placeholder for the final result

# Streamlit control buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Clear Text"):
        st.session_state["arr"] = []
with col2:
    if st.button("Undo Last Character"):
        if st.session_state["arr"]:
            st.session_state["arr"].pop()
with col3:
    if st.button("Save Character"):
        st.session_state["arr"].append(st.session_state.get("current_label", ""))

# Main loop for video processing
while cap.isOpened():
    success, img = cap.read()
    if not success:
        st.warning("Failed to capture video.")
        break

    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        try:
            imgCropShape = imgCrop.shape
            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            # Get prediction
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            st.session_state["current_label"] = labels[index]

            # Draw bounding box and label
            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                          (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset),
                          (x + w + offset, y + h + offset), (255, 0, 255), 4)

        except Exception as e:
            st.warning("Error in processing hand sign. Try adjusting hand position.")
            print("Exception:", e)

    # Display the video feed in Streamlit
    imgOutput_rgb = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for Streamlit display
    video_placeholder.image(imgOutput_rgb)

    # Update recognized text and final result
    recognized_text.text(f"Recognized Character: {st.session_state.get('current_label', '')}")
    final_result.text(f"Current Text: {''.join(st.session_state['arr'])}")

    # Break the loop if Streamlit stops
    if st.button("Stop"):
        break

cap.release()
