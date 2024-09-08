import streamlit as st
import requests
from streamlit_cookies_controller import CookieController
import pandas as pd
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

    headers = {
                "Authorization": st.session_state['token']
            }
    if st.session_state['role']:
        st.subheader("Add Parking Spot")
        with st.form(key="parking_spot_form"):
            level = st.number_input("Level", min_value=1)
            section = st.text_input("Section")
            spot_number = st.number_input("Spot Number", min_value=1)
            vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Truck"])
            exit_distance = st.number_input("Exit Distance", min_value=1)
            short_term_only = st.checkbox("Short Term Only", False)
            is_occupied = st.checkbox("Is Occupied", False)
            submit_button = st.form_submit_button("Add Spot")

            if submit_button:
                if not (level and section and spot_number and vehicle_type and exit_distance ):
                    st.error("All fields must be filled in")
                else:
                    data = {
                        "level": level,
                        "section": section,
                        "spot_number": spot_number,
                        "vehicle_type": vehicle_type,
                        "exit_distance": exit_distance,
                        "is_occupied": is_occupied,
                        "short_term_only": short_term_only,
                    }
                    try:
                        response = requests.post(f"{BASE_URL}/parking_spots/", json=data, headers=headers)
                        response.raise_for_status()
                        st.success("Parking spot created successfully")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error creating parking spot: {e}")


        st.subheader("All Parking Spots")
        response = requests.get(f"{BASE_URL}/parking_spots/", headers=headers)
        parking_spots = response.json()
        df = pd.DataFrame(parking_spots)
        st.table(df)

        
        spot_id = st.number_input("Enter the ID of the parking spot to update or delete",step=1, value=None)
        
        if spot_id:
            parking_spot = next((spot for spot in parking_spots if spot['id'] == spot_id), None)
            if parking_spot:
                with st.form(key="update_spot_form"):
                    level = st.number_input("Level", value=parking_spot['level'])
                    section = st.text_input("Section", value=parking_spot['section'])
                    spot_number = st.number_input("Spot Number", value=parking_spot['spot_number'])
                    vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Truck"], index=["Car", "Motorcycle", "Truck"].index(parking_spot['vehicle_type']))
                    exit_distance = st.number_input("Exit Distance", value=parking_spot['exit_distance'])
                    short_term_only = st.checkbox("Short Term Only", value=parking_spot['short_term_only'])
                    is_occupied = st.checkbox("Is Occupied", value=parking_spot['is_occupied'])
                    submit_button = st.form_submit_button("Update Spot")

                    if submit_button:
                        if not (level and section and spot_number and vehicle_type):
                            st.error("All fields must be filled in")
                        else:
                            data = {
                                "level": level,
                                "section": section,
                                "spot_number": spot_number,
                                "vehicle_type": vehicle_type,
                                "exit_distance": exit_distance,
                                "short_term_only": short_term_only,
                                "is_occupied": is_occupied
                            }
                            try:
                                print(data)
                                response = requests.put(f"{BASE_URL}/parking_spots/{spot_id}", json=data, headers=headers)
                                st.success("Parking spot updated successfully")
                                st.rerun()
                            except requests.exceptions.RequestException as e:
                                st.error(f"Error updating parking spot: {e}")

                delete_button = st.button("Delete Spot", type='primary')

                if delete_button:
                    try:
                        response = requests.delete(f"{BASE_URL}/parking_spots/{spot_id}", headers=headers)
                        st.success("Parking spot deleted successfully")
                        st.rerun()
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error deleting parking spot: {e}")

        
