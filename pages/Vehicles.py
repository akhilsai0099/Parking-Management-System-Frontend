import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

if "token" in st.session_state:
	headers = {
			"Authorization": st.session_state['token']
		}
else:
	headers = {
			"Authorization": ""
		}
		
def add_vehicle():
	st.subheader("Add Vehicle")
	with st.form(key="vehicle_form"):
		license_plate = st.text_input("License Plate")
		vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Truck"])
		owner_name = st.text_input("Owner Name")
		contact_number = st.text_input("Contact Number")
		submit_vehicle = st.form_submit_button("Add Vehicle")

		if submit_vehicle:
			if not (license_plate and vehicle_type and owner_name and contact_number):
				st.error("All fields must be filled in")
			else:
				data = {
					"license_plate": license_plate,
					"vehicle_type": vehicle_type,
					"owner_name": owner_name,
					"contact_number": contact_number,
				}
				try:
					response = requests.post(f"{BASE_URL}/vehicles/", json=data, headers=headers)
					print(response.json())
					st.success("Vehicle created successfully")
				except requests.exceptions.RequestException as e:
					st.error(f"Error: Vehicle already exists")

def existing_vehicles():
	st.subheader("Existing Vehicles")
	existing_vehicles = requests.get(f"{BASE_URL}/vehicles/", headers=headers)
	existing_vehicles_json = existing_vehicles.json()
	df = pd.DataFrame(existing_vehicles_json)

	st.table(df)

	vehicle_id = st.text_input("Enter Vehicle ID to Update/Delete", help="Enter the ID of the vehicle you want to update or delete")
	if vehicle_id:
		vehicle = df.loc[df['id'] == int(vehicle_id)] if int(vehicle_id) in df['id'].values else None
		if vehicle is not None:
			with st.form(key="edit_vehicle_form"):
				license_plate = st.text_input("License Plate", key=f"{vehicle_id}_license_plate", value = vehicle['license_plate'].values[0])
				vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle", "Truck"], key=f"{vehicle_id}_vehicle_type", index = ["Car", "Motorcycle", "Truck"].index(vehicle['vehicle_type'].values[0]))
				owner_name = st.text_input("Owner Name", key=f"{vehicle_id}_owner_name", value=vehicle['owner_name'].values[0])
				contact_number = st.text_input("Contact Number", key=f"{vehicle_id}_contact_number", value=vehicle['contact_number'].values[0])
				edit_vehicle = st.form_submit_button("Edit")
				
				if edit_vehicle:
					print("inside")
					data = {
						"license_plate": license_plate,
						"vehicle_type": vehicle_type,
						"owner_name": owner_name,
						"contact_number": contact_number,
					}
					
					if not all([license_plate, vehicle_type, owner_name, contact_number]):
						st.error("All fields must be filled in")
					else:
						response = requests.put(f"{BASE_URL}/vehicles/{vehicle_id}/", json=data, headers=headers)
						print(response.json())
						st.success("Vehicle updated successfully")
						st.rerun()
			
			delete_vehicle_button = st.button("Delete Vehicle", type="primary")

			if delete_vehicle_button:
				try:
					response = requests.delete(f"{BASE_URL}/vehicles/{vehicle_id}/", headers=headers)
					st.success("Vehicle deleted successfully")
				except requests.exceptions.RequestException as e:
					st.error(f"Error: {e}")
				st.rerun()

		else:
			st.error("Vehicle not found")

def main():
	if 'token' in st.session_state:
		add_vehicle()
		existing_vehicles()
	else:
		st.error("Please login to access this page")
if __name__ == "__main__":
	main()