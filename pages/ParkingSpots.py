import streamlit as st
import requests

st.set_page_config(page_title="Dashboard", layout="wide")
BASE_URL = "http://127.0.0.1:8000"
if "token" in st.session_state:
	headers = {
			"Authorization": st.session_state['token']
		}
	response = requests.get(f"{BASE_URL}/parking_spots/", headers=headers)
	parking_spots = response.json()
	df = [parking_spot for parking_spot in parking_spots]
else:
	headers = {
			"Authorization": ""
		}

def parkingSpots():
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
		df = [parking_spot for parking_spot in parking_spots]
		st.dataframe(df, use_container_width=True)

		
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
					submit_button = st.form_submit_button("Update Spot", key="update_spot_button")

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

		
def main():
	if 'token' in st.session_state :
		if st.session_state['role']:
			parkingSpots()
		else:
			st.error("You Don't have access to this page")
	else:

		st.error("Please login to access this page")

if __name__ == '__main__':
	main()