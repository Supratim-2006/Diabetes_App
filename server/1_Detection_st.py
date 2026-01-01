import streamlit as st
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from logic_file import Diabetes

# --- Helper Functions ---

def is_valid_email(email):
    """Simple regex to check email format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def send_email_report(receiver_email, pdf_data):
    """Sends the generated PDF to the user's Gmail via SMTP."""
    sender_email = "supratimkukri19@gmail.com"  # Replace with your Gmail
    sender_password = "wqdi vogz mgdc jfxg" # Replace with your 16-digit App Password

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Diabetes Prediction Analysis Report"

        body = "Attached is your AI-generated Diabetes Prediction Report based on the provided metrics."
        msg.attach(MIMEText(body, 'plain'))

        # Attach PDF
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= Patient_Report.pdf")
        msg.attach(part)

        # SMTP Config
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# --- Main Application Logic ---

def main():
    # Session state initialization
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""

    # --- Authentication Step ---
    if not st.session_state.authenticated:
        st.set_page_config(page_title="Secure Login", page_icon="🔐")
        st.title("🔐 Secure Clinical Access")
        st.write("Please enter your email to access the Diabetes Prediction Dashboard.")
        
        email_input = st.text_input("Gmail Address:", placeholder="example@gmail.com")
        
        if st.button("Access Dashboard"):
            if is_valid_email(email_input):
                st.session_state.authenticated = True
                st.session_state.user_email = email_input
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Invalid email format. Please use a valid Gmail address.")
        st.stop()

    # --- Main Dashboard Step ---
    st.set_page_config(page_title="Diabetes Prediction Dashboard", layout="wide", page_icon="🤖")
    
    # Sidebar: User Info & Logout
    st.sidebar.title("User Profile")
    st.sidebar.write(f"Logged in as: **{st.session_state.user_email}**")
    if st.sidebar.button("🔒 Logout"):
        st.session_state.authenticated = False
        st.session_state.user_email = ""
        st.rerun()

    st.title("🤖 Diabetes Prediction AI System")
    st.markdown("---")

    db = Diabetes()
    col1, col2 = st.columns([3, 1])

    with col1:
        db.add_sidebar()
        st.session_state['user_metrics'] = db.input_data

    with col2:
        st.subheader("Results")
        status, prob = db.add_Prediction()
        report_bytes = db.generate_pdf_report(status, prob)

        # Download Option
        st.download_button(
            label="📥 Download PDF Report",
            data=report_bytes,
            file_name="Diabetes_Report.pdf",
            mime="application/pdf"
        )

        # Email Option
        if st.button("📧 Send Report to Gmail"):
            with st.spinner("Sending email..."):
                success = send_email_report(st.session_state.user_email, report_bytes)
                if success:
                    st.success(f"Report sent to {st.session_state.user_email}")

if __name__ == "__main__":
    main()