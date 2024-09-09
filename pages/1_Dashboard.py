import streamlit as st
import requests
import datetime

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

def upcomingExits():
	response = requests.get(f"{BASE_URL}/parking_sessions/", headers=headers)
	parking_sessions = response.json()
	upcoming_exits = [session for session in parking_sessions if session['expected_exit_time'] is not None and session['actual_exit_time'] is None and (datetime.datetime.fromisoformat(session['expected_exit_time']) - datetime.datetime.now()).total_seconds() < 3600]
	st.subheader("Upcoming Exits")
	st.write("-----")
	if len(upcoming_exits)>0:
		st.dataframe(upcoming_exits)
	else:
		st.write("No upcoming exits in the next hour")

def revenue():
	response = requests.get(f"{BASE_URL}/parking_sessions/revenue", headers=headers)
	data = response.json()
	st.subheader("Revenue")
	st.write(f"Total revenue Generated: ${data['total_revenue']:.2f}")
	st.write(f"Upcoming revenue: ${data['expected_revenue']:.2f}")

def dashboard():
	st.title("Dashboard")
	st.write("-----")
	col1, col2 = st.columns(2)
	if df is not None:
		with col1:
			st.subheader("Free Parking Spots")
			free_spots = [free_spot for free_spot in df if not free_spot['is_occupied']]
			if len(free_spots)>0:
				st.dataframe(free_spots)
			else:
				st.write("No free spots available")
		with col2:
			st.subheader("Active Parking Spots")
			occupied_spots = [free_spot for free_spot in df if free_spot['is_occupied']]
			if len(occupied_spots)>0:
				st.table(occupied_spots)
			else:
				st.write("No Occupied spots available")
		col1, col2 = st.columns(2)
		with col1:
			parking_occupancy_chart()
		with col2:
			revenue()
		upcomingExits()
		
		
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