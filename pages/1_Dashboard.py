import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard")
BASE_URL = "http://127.0.0.1:8000"
if "token" in st.session_state:
	headers = {
			"Authorization": st.session_state['token']
		}
	response = requests.get(f"{BASE_URL}/parking_spots/", headers=headers)
	parking_spots = response.json()
	df = pd.DataFrame(parking_spots)
else:
	headers = {
			"Authorization": ""
		}



def dashboard():
	st.title("Dashboard")
	st.write("-----")
	col1, col2 = st.columns(2)

	with col1:
		st.subheader("Free Parking Spots")
		free_spots = df.loc[df['is_occupied'] == False]
		st.table(free_spots)
	with col2:
		st.subheader("Active Parking Spots")
		occupied_spots = df.loc[df['is_occupied'] == True]
		st.table(occupied_spots)
	col1, col2 = st.columns(2)
	with col1:
		parking_occupancy_chart()

def parking_occupancy_chart():
	import plotly.express as px

	data = [
		{'Status': 'Occupied', 'Count': len([spot for spot in parking_spots if spot['is_occupied']])},
		{'Status': 'Free', 'Count': len([spot for spot in parking_spots if not spot['is_occupied']])}
	]

	fig = px.pie(data, names='Status', values='Count', title='Occupancy Chart')
	st.plotly_chart(fig, use_container_width=True)

def main():
	if 'token' in st.session_state :
		if st.session_state['role']:
			dashboard()
		else:
			st.error("You Don't have access to this page")
	else:

		st.error("Please login to access this page")

if __name__ == '__main__':
	main()