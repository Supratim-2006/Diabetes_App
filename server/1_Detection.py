import streamlit as st
import cv2
import numpy as np
import mediapipe.python.solutions.hands as hands
import mediapipe.python.solutions.drawing_utils as du
import keras
import time
from logic_file import Diabetes


####HandGesture####

def bounding_box(landmarks, w, h):
    x1, y1 = w, h
    x2 = y2 = 0
    for i in range(21):
        x1 = int(min(x1, w * landmarks[i].x))
        x2 = int(max(x2, w * landmarks[i].x))
        y1 = int(min(y1, h * landmarks[i].y))
        y2 = int(max(y2, h * landmarks[i].y))
    return (x1, y1, x2, y2)

def create_data(landmarks, w1, h1, w2, h2):
    lms = landmarks
    data = []
    x0, y0 = lms[0].x, lms[0].y
    for i in range(1, 21):
        dx = (lms[i].x - x0) * (w1 / w2)
        dy = (lms[i].y - y0) * (h1 / h2)
        data.append(dx)
        data.append(dy)
    return data



def run_lock_screen():
    st.title("🔒 App Locked")
    st.info("Show a **Thumbs Up** to unlock the Detection Dashboard.")
    
    capture_hands = hands.Hands(min_detection_confidence=0.7)
    cap = cv2.VideoCapture(0)
    gesture_model = keras.models.load_model("TrainingModel/gesturedetector.h5")
    labels = ["ThumbsUp", "ThumbsDown"]
    
    frame_placeholder = st.empty()
    success_counter = 0

    while st.session_state.app_locked:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output_hands = capture_hands.process(rgb_frame)
        
        gesture_detected = "None"
        if output_hands.multi_hand_landmarks:
            for hand_lms in output_hands.multi_hand_landmarks:
                du.draw_landmarks(frame, hand_lms, hands.HAND_CONNECTIONS)
                x1, y1, x2, y2 = bounding_box(hand_lms.landmark, w, h)
                bw, bh = x2 - x1, y2 - y1
                
                if bw > 0 and bh > 0:
                    data = create_data(hand_lms.landmark, w, h, bw, bh)
                    prediction = gesture_model.predict(np.array([data]), verbose=0)
                    gesture_detected = labels[np.argmax(prediction)]
                    cv2.putText(frame, gesture_detected, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if gesture_detected == "ThumbsUp":
            success_counter += 1
        else:
            success_counter = 0

        frame_placeholder.image(frame, channels="BGR")

        if success_counter > 15:
            st.session_state.app_locked = False
            cap.release()
            st.experimental_rerun() 
        
        time.sleep(0.01) # CPU breather

    cap.release()


def main():
    if "app_locked" not in st.session_state:
        st.session_state.app_locked = True

    if st.session_state.app_locked:
        run_lock_screen()
    else:
        # MAIN DASHBOARD CONTENT
        st.set_page_config(page_title="Health Input App", layout="wide", initial_sidebar_state="expanded",page_icon="🤖")
        
        if st.sidebar.button("🔒 Logout / Lock"):
            st.session_state.app_locked = True
            st.experimental_rerun() 

        st.title("🤖 Diabetes Prediction Web App")
        col1, col2 = st.columns([4, 1])
        db=Diabetes()
        with col1:
            db.add_sidebar()
            st.session_state['user_metrics'] = db.input_data
        with col2:
            status, prob = db.add_Prediction()
            report_bytes = db.generate_pdf_report(status, prob)
            st.download_button(
            label="📥 Download PDF Report",
            data=report_bytes,
            file_name=f"Patient_Report.pdf",
            mime="application/pdf"
            )

if __name__=="__main__":
    main()
