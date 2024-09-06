import requests
import datetime
import streamlit as st
BASE_URL = "http://127.0.0.1:8000"
if "token" in st.session_state:
	headers = {
			"Authorization": st.session_state['token']
		}
else:
	headers = {
			"Authorization": ""
		}
		
def parking_session():
	st.subheader("Book Parking Session")
	with st.form(key="Parking Session Form"):
		response = requests.get(f"{BASE_URL}/vehicles/", headers=headers)
		vehicles = response.json()
		options = ["Select a vehicle"]
		col1, col2 = st.columns(2)
		options.extend([vehicle["license_plate"] for vehicle in vehicles])

		vehicle_id = st.selectbox("Vehicle", options)
		with col1:
			entry_date = st.date_input("Entry Date", min_value=datetime.date.today(), max_value=datetime.date.today() + datetime.timedelta(days=30))
			entry_time = st.time_input("Entry Time")
		with col2:
			exit_date = st.date_input("Exit Date", min_value=datetime.date.today(), max_value=datetime.date.today() + datetime.timedelta(days=30))
			exit_time = st.time_input("Exit Time")
		submit_session = st.form_submit_button("Book Session")
		

		if submit_session:
			if not (vehicle_id != "Select a vehicle" and entry_time and exit_time and entry_date and exit_date):
				st.error("All fields must be filled in")
			
			else:
				data = {
					"vehicle_id": vehicle_id,
					"entry_time": datetime.datetime.combine(entry_date, entry_time).isoformat(),
					"exit_time": datetime.datetime.combine(exit_date, exit_time).isoformat()
				}
				
				try:
					response = requests.post(f"{BASE_URL}/parking_sessions/", json=data, headers=headers)
					
					st.success("Parking session booked successfully")
				except requests.exceptions.RequestException as e:
					st.error(f"Error booking session: {e}")


def main():
	if "token" in st.session_state:
		parking_session()
	else:
		st.error("Please login to access this page")

if __name__ == "__main__":
	main()