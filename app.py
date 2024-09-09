import streamlit as st
import requests
from streamlit_cookies_controller import CookieController
import time

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Parking Management System", layout="wide")


st.title("Parking Management System")
controller = CookieController()
def authenticate():
    login_register = st.selectbox("Login or Register", ["Login", "Register"])

    if login_register == "Login":
        with st.form(key="login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Login")

            if submit_login:
                data = {"email": email, "password": password}
                response = requests.post(f"{BASE_URL}/login/", json=data)
                if response.status_code == 200:
                    token = response.json().get("token")

                    role = response.json().get("role")
                    controller.set('token', token)  
                    controller.set('role', role)
                    st.session_state["token"] = token
                    st.session_state["role"] = role
                    time.sleep(1)
                    return True
                else:
                    st.error("Invalid email or password")
                    return False
        return False

    elif login_register == "Register":
        with st.form(key="register_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            is_admin = st.checkbox("Is Admin")
            submit_register = st.form_submit_button("Register")

            if submit_register:
                if password != confirm_password:
                    st.error("Passwords do not match")
                    return False
                data = {"email": email, "password": password, "is_admin": is_admin}
                response = requests.post(f"{BASE_URL}/register/", json=data)
                if response.status_code == 200:
                    st.success("User created successfully")
                else:
                    st.error("Failed to create user")
                return False
        return False



cookies= controller.getAll()
if 'token' in cookies:
    st.session_state['token'] = cookies['token']
    st.session_state['role'] = cookies['role']

if 'token' not in st.session_state:
    is_authenticated = authenticate()
    if is_authenticated:
        st.rerun()

elif st.session_state["token"]:
    if st.session_state["token"] and st.button("Logout"):
        del st.session_state['token']
        del st.session_state['role']
        controller.remove('token')
        controller.remove('role')
        time.sleep(1)   
        st.rerun()
