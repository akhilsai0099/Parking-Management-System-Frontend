import requests
import datetime
import streamlit as st
import time
BASE_URL = "http://127.0.0.1:8000"

if "token" in st.session_state:
	headers = {
			"Authorization": st.session_state['token']
		}
else:
	headers = {
			"Authorization": ""
	}
		

def parking_session_form():
	st.subheader("Book Parking Session")

	response = requests.get(f"{BASE_URL}/vehicles/", headers=headers)
	vehiclesJson = response.json()
	vehicles = {vehicle['license_plate']: vehicle['id'] for vehicle in vehiclesJson}
	if len(vehicles) == 0:
		st.write("No vehicles found")
		return
	else:
		with st.form(key="Parking Session Form"):
			options = list(vehicles.keys())
			
			col1, col2 = st.columns(2)
			selected_license_plate = st.selectbox("Vehicle", options)
			vehicle_id = vehicles[selected_license_plate] 

			with col1:
				entry_date = st.date_input("Entry Date", min_value=datetime.date.today(), max_value=datetime.date.today() + datetime.timedelta(days=30))
				entry_time = st.time_input("Entry Time")
			with col2:
				exit_date = st.date_input("Exit Date", min_value=datetime.date.today(), max_value=datetime.date.today() + datetime.timedelta(days=30))
				exit_time = st.time_input("Exit Time", value=(datetime.datetime.now() + datetime.timedelta(minutes=15)).time())
			submit_session = st.form_submit_button("Book Session")

			if submit_session:
				if not (selected_license_plate and entry_time and exit_time and entry_date and exit_date):
					st.error("All fields must be filled in")
				else:
					
					entry_datetime = datetime.datetime.combine(entry_date, entry_time)
					exit_datetime = datetime.datetime.combine(exit_date, exit_time)
					
					if exit_datetime <= entry_datetime:
						st.error("Exit time must be after entry time")
					else:
						data = {
							"vehicle_id": vehicle_id, 
							"entry_time": entry_datetime.isoformat(),
							"expected_exit_time": exit_datetime.isoformat()  
						}
						try:
							response = requests.post(f"{BASE_URL}/parking_sessions/", json=data, headers=headers)
							if response.status_code == 200: 
								st.success("Parking session booked successfully")
							elif response.status_code == 400 or response.status_code == 404:
								st.error("Error booking session: " + response.json()["message"])
						except requests.exceptions.RequestException as e:
							st.error(f"Error booking session: {e}")

def activeParkingSession(parkingSessionsJson):
	st.subheader("Active Parking Sessions")

	
	parkingSessions = [parkingSession for parkingSession in parkingSessionsJson if parkingSession['actual_exit_time'] is None]
	if len(parkingSessions)>0:
		st.dataframe(parkingSessions, use_container_width=True)
		st.subheader("Exit Parking")
		with st.form("calculate_price"):
			parking_session_id = st.selectbox("Select a parking session", [parkingSession['id'] for parkingSession in parkingSessions])
			submit_price = st.form_submit_button("Pay and Exit")
			if submit_price:
				response = requests.put(f"{BASE_URL}/parking_sessions/{parking_session_id}/price", headers=headers)
				response.raise_for_status()
				if response.status_code == 200:
					data = response.json()
					st.success(f"Price for parking session {parking_session_id}: {data['price']}")
					time.sleep(1)
					st.rerun()
					
				elif response.status_code == 404:
					st.error("Parking session not found")
	else:
		st.write("No active parking sessions")

def previousParkingSessions(parkingSessionsJson):
	st.subheader("Previous Parking Sessions")
	prev_parking_session = [parkingSession for parkingSession in parkingSessionsJson if parkingSession['actual_exit_time'] is not None]
	if len(prev_parking_session)>0:
		st.dataframe(prev_parking_session, use_container_width=True)
	else:
		st.write("No Prev parking Sessions")
def parking_sessions():
	response = requests.get(f"{BASE_URL}/parking_sessions/", headers=headers)
	parkingSessionsJson = response.json()
	activeParkingSession(parkingSessionsJson)
	previousParkingSessions(parkingSessionsJson)
	

def main():
	if "token" in st.session_state:
		parking_session_form()
		parking_sessions()
	else:
		st.error("Please login to access this page")

if __name__ == "__main__":
	main()