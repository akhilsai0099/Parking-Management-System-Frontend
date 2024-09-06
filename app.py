import streamlit as st
import requests
from streamlit_cookies_controller import CookieController
import time
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Parking Management System")


st.title("Parking Management System")
controller = CookieController()
def authenticate():
    if "token" in st.session_state:
        return True
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
            submit_register = st.form_submit_button("Register")

            if submit_register:
                if password != confirm_password:
                    st.error("Passwords do not match")
                    return False
                data = {"email": email, "password": password}
                response = requests.post(f"{BASE_URL}/register/", json=data)
                if response.status_code == 200:
                    st.success("User created successfully")
                else:
                    st.error("Failed to create user")
                return False
        return False

def handleLogout():
    st.session_state['token'] = None
    st.session_state['role'] = None
    controller.remove('token')
    controller.remove('role')


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

    if st.session_state['role']:
        st.subheader("Add Parking Spot")
        with st.form(key="parking_spot_form"):
            level = st.number_input("Level", min_value=1)
            section = st.text_input("Section")
            spot_number = st.number_input("Spot Number", min_value=1)
            vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Truck"])
            is_occupied = st.checkbox("Is Occupied", False)
            submit_button = st.form_submit_button("Add Spot")

            if submit_button:
                data = {
                    "level": level,
                    "section": section,
                    "spot_number": spot_number,
                    "vehicle_type": vehicle_type,
                    "is_occupied": is_occupied
                }
                response = requests.post(f"{BASE_URL}/parking_spots/", json=data)
                st.write(response.json())

    st.subheader("Add Vehicle")
    with st.form(key="vehicle_form"):
        license_plate = st.text_input("License Plate")
        vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Truck"])
        owner_name = st.text_input("Owner Name")
        contact_number = st.text_input("Contact Number")
        submit_vehicle = st.form_submit_button("Add Vehicle")

        if submit_vehicle:
            data = {
                "license_plate": license_plate,
                "vehicle_type": vehicle_type,
                "owner_name": owner_name,
                "contact_number": contact_number
            }
            response = requests.post(f"{BASE_URL}/vehicles/", json=data)
            st.write(response.json())

    st.subheader("Book Parking Session")
    with st.form(key="Parking Session Form"):
        vehicle_id = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Truck"])

        entry_time = st.time_input("Entry Time")
        exit_time = st.time_input("Exit Time")
        submit_session = st.form_submit_button("Book Session")

        if submit_vehicle:
            data = {
                "license_plate": license_plate,
                "vehicle_type": vehicle_type,
                "owner_name": owner_name,
                "contact_number": contact_number
            }
            response = requests.post(f"{BASE_URL}/vehicles/", json=data)
            st.write(response.json())
