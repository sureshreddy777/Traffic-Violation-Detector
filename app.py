import streamlit as st
from aws_utils import (
    detect_license_plate,
    describe_image_violations,
    classify_violation,
    lookup_owner_info,
    store_violation_record
)
from auth import register_user, confirm_user, login_user
from redshift_utils import insert_violation
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Traffic Violation Reporter", layout="wide")

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "useremail" not in st.session_state:
    st.session_state["useremail"] = ""

# 🔐 Login Tab
def login_tab():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        success, result = login_user(email, password)
        if success and isinstance(result, dict):
            st.session_state["authenticated"] = True
            st.session_state["username"] = result.get("username", "User")
            st.session_state["useremail"] = result.get("email", email)
            st.success(f"✅ Welcome, {st.session_state['username']}")
            st.rerun()
        else:
            st.error(f"❌ Login failed: {result}")

# 📝 Registration Tab
import re
import streamlit as st
from auth import register_user, confirm_user

def register_tab():
    # If registration was successful, go to Login tab
    if st.session_state.get("registration_success"):
        st.session_state["registration_success"] = False
        st.switch_page("Login")  # Streamlit 1.25+ has st.switch_page
        st.rerun()

    st.subheader("Register")

    # Input fields
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")
    username = st.text_input("Full Name / Username", key="reg_username")
    code = st.text_input("Verification Code (Check your Email)", key="reg_code")

    # Password policy feedback
    st.markdown("**Password must contain:**")
    rules = {
        "At least 8 characters": len(password) >= 8,
        "At least one lowercase letter": bool(re.search(r"[a-z]", password)),
        "At least one uppercase letter": bool(re.search(r"[A-Z]", password)),
        "At least one number": bool(re.search(r"[0-9]", password)),
        "At least one special character (!@#$%^&*)": bool(re.search(r"[!@#$%^&*()_+=\\-{}\[\]:;\"'<>,.?/]", password))
    }

    for rule, passed in rules.items():
        icon = "✅" if passed else "❌"
        st.markdown(f"- {icon} {rule}")

    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    col1, col2 = st.columns(2)

    # Button 1: Register
    with col1:
        register_clicked = st.button("Verify")
        if register_clicked:
            if not email.strip() or not password.strip() or not username.strip():
                st.warning("⚠️ Please fill in all fields.")
            elif not is_valid_email(email.strip()):
                st.error("❌ Invalid email address format.")
            elif not all(rules.values()):
                st.error("❌ Password does not meet all requirements.")
            else:
                success, msg = register_user(email.strip(), password.strip(), username.strip())
                if success:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")

    # Button 2: Verify
    with col2:
        verify_clicked = st.button("Register")
        if verify_clicked:
            if not code.strip():
                st.warning("⚠️ Please enter the verification code.")
            elif not email.strip():
                st.warning("⚠️ Please enter your email again.")
            elif not is_valid_email(email.strip()):
                st.error("❌ Invalid email address format.")
            else:
                success, msg = confirm_user(email.strip(), code.strip())
                if success:
                    st.success("✅ User confirmed successfully. Redirecting to login...")
                    st.session_state["registration_success"] = True
                    st.rerun()
                else:
                    st.error(f"❌ Verification failed: {msg}")

# 🚪 Show login or registration if not authenticated
if not st.session_state["authenticated"]:
    st.title("🚨 Traffic Violation Reporter")
    tabs = st.tabs(["Login", "Register"])
    with tabs[0]:
        login_tab()
    with tabs[1]:
        register_tab()
    st.stop()

# ✅ Main App After Login
st.title("🚦 Report a Traffic Violation")

uploaded_file = st.file_uploader("Upload a traffic violation image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", width=400)
    if st.button("Report"):
        license_plate = detect_license_plate(uploaded_file)
        st.write("🔍 **Detected License Plate:**", license_plate)

        description = describe_image_violations(uploaded_file)
        st.write("📝 **Description Generated:**", description)

        violation_type = classify_violation(description)
        st.write("🚫 **Violation Type:**", violation_type)

        # ✅ CORRECTED: Pass label to violation_type, description to description
        store_violation_record(
            license_plate=license_plate,
            violation_type=violation_type,
            description=description,
            username=st.session_state.get("username", "unknown_user"),
            email=st.session_state.get("useremail", "unknown_email")
        )

        st.success("✅ Violation record saved in DynamoDB!")

        owner_info = lookup_owner_info(license_plate)
        if owner_info:
            phone = str(owner_info.get("contact_number", "Not Found"))
            email = owner_info.get("email", "Not Found")
            st.info(f"📇 **Owner Details:**\n- Phone: {phone}\n- Email: {email}")
        else:
            st.warning("⚠️ No owner info found for this license plate.")

        if owner_info:
            phone = str(owner_info.get("contact_number", "Not Found"))
            email = owner_info.get("email", "Not Found")
            st.info(f"📇 **Owner Details:**\n- Phone: {phone}\n- Email: {email}")

            # 🚀 Send notification email
            from email_utils import send_violation_email
            if send_violation_email(email, license_plate, violation_type, description):
                st.success("📧 Email notification sent to the vehicle owner.")
            else:
                st.warning("⚠️ Failed to send email notification.")

