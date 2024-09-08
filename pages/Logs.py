import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Dashboard", layout="wide")
BASE_URL = "http://127.0.0.1:8000"
if "token" in st.session_state:
	headers = {
			"Authorization": st.session_state['token']
		}
else:
	headers = {
			"Authorization": ""
		}


def logs():
	st.title("Logs")
	st.write("-----")
	st_autorefresh(interval=2000, key="autoupdater")
	response = requests.get(f"{BASE_URL}/logs/", headers=headers)
	st.session_state['logs'] = response.text
	st.text_area("_", st.session_state['logs'], height=500, disabled=True)



def main():
	if 'token' in st.session_state :
		if st.session_state['role']:
			logs()
		else:
			st.error("You Don't have access to this page")
	else:

		st.error("Please login to access this page")

if __name__ == '__main__':
	main()