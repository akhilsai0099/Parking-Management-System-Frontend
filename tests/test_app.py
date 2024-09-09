import datetime
import pytest
from streamlit.testing.v1 import AppTest
import time

TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGdtYWlsLmNvbSIsImV4cCI6MTcyNTg3ODUxMn0.AHXPLUEYFWdobITXmpdC9IeWxhC_yqr9DWmqOWE-Bes"

def find_input_by_label(app, label):
    return next((input for input in app.text_input if input.label == label), None)

def find_button_by_label(app, label):
    return next((button for button in app.button if button.label == label), None)

def find_selectbox_by_label(app, label):
	return next((selectbox for selectbox in app.selectbox if selectbox.label == label), None)

def find_number_input_by_label(app, label):
	return next((number_input for number_input in app.number_input if number_input.label == label), None)

def find_checkbox_by_label(app, label):
	return next((checkbox for checkbox in app.checkbox if checkbox.label == label), None)


def test_register(app):
	app.run()
	assert not app.exception
	selectbox = app.selectbox[0]
	selectbox.set_value("Register").run()
	email_input = find_input_by_label(app, "Email")
	password_input = find_input_by_label(app, "Password")
	confirm_password_input = find_input_by_label(app, "Confirm Password")
	submit = find_button_by_label(app, "Register")

	assert email_input.label == "Email"
	assert password_input.label == "Password" 
	assert confirm_password_input.label == "Confirm Password"
	assert submit

	if email_input and password_input and submit:
		email_input.input("test@example.com").run()
		password_input.input("password123").run()
		confirm_password_input.input("password123").run()
		submit.click().run()
		time.sleep(1)
		assert app.success[0].value == "User created successfully"

	else:
		pytest.fail("Register form elements not found")

def test_register_already_exists(app):
	app.run()
	assert not app.exception
	selectbox = app.selectbox[0]
	selectbox.set_value("Register").run()
	email_input = find_input_by_label(app, "Email")
	password_input = find_input_by_label(app, "Password")
	confirm_password_input = find_input_by_label(app, "Confirm Password")
	submit = find_button_by_label(app, "Register")

	assert email_input.label == "Email"
	assert password_input.label == "Password" 
	assert confirm_password_input.label == "Confirm Password"
	assert submit

	if email_input and password_input and submit:
		email_input.input("test@example.com").run()
		password_input.input("password123").run()
		confirm_password_input.input("password123").run()
		submit.click().run()
		time.sleep(1)
		assert app.error[0].value == "Failed to create user"

	else:
		pytest.fail("Register form elements not found")

def test_successfull_login(app):
	app.run()
	assert not app.exception
	assert app.selectbox[0].label == "Login or Register"
      
	email_input = find_input_by_label(app, "Email")
	password_input = find_input_by_label(app, "Password")
	submit = find_button_by_label(app, "Login")

	assert email_input
	assert password_input
	assert submit
     
	if email_input and password_input and submit:
		email_input.input("test@example.com").run()
		password_input.input("password123").run()
		submit.click().run()
		time.sleep(1)
		assert "token" in app.session_state

	else:
		pytest.fail("Login form elements not found")

def test_unsuccessfull_login(app):
	app.run()
	assert not app.exception
	assert app.selectbox[0].label == "Login or Register"
      
	email_input = find_input_by_label(app, "Email")
	password_input = find_input_by_label(app, "Password")
	submit = find_button_by_label(app, "Login")

	assert email_input
	assert password_input
	assert submit
     
	if email_input and password_input and submit:
		email_input.input("test@example.com").run()
		password_input.input("password12345").run()
		submit.click().run()
		time.sleep(1)
		assert app.error[0].value == 'Invalid email or password'
	else:
		pytest.fail("Login form elements not found")

def test_parking_spot(app):
	
	app = AppTest.from_file("pages/ParkingSpots.py")
	app.session_state['token'] = TOKEN
	app.session_state['role'] = True
	app.run()
	level = find_number_input_by_label(app, "Level")
	section = find_input_by_label(app, "Section")
	spot_number = find_number_input_by_label(app, "Spot Number")
	vehicle_type = find_selectbox_by_label(app, "Vehicle Type")
	exit_distance = find_number_input_by_label(app, "Exit Distance")
	short_term_only = find_checkbox_by_label(app, "Short Term Only")
	is_occupied = find_checkbox_by_label(app, "Is Occupied")
	submit = find_button_by_label(app, "Add Spot")
	assert level
	assert section
	assert spot_number
	assert vehicle_type
	assert exit_distance
	assert short_term_only
	assert is_occupied
	assert submit

	
	level.set_value(1).run()
	section.input("A").run()
	spot_number.set_value(1).run()
	vehicle_type.set_value("Car").run()
	exit_distance.set_value(30).run()
	short_term_only.check().run()
	is_occupied.uncheck().run()
	submit.click().run()
	
	assert app.success[0].value == "Parking spot created successfully"
	

def test_create_vehicle(app):
	
	app = AppTest.from_file("pages/Vehicles.py")
	app.session_state['token'] = TOKEN
	app.session_state['role'] = True
	app.run()

	license_plate = find_input_by_label(app, "License Plate")
	vehicle_type = find_selectbox_by_label(app, "Vehicle Type")
	owner_name = find_input_by_label(app, "Owner Name")
	contact_number = find_input_by_label(app, "Contact Number")
	submit = find_button_by_label(app, "Add Vehicle")

	assert license_plate
	assert vehicle_type
	assert owner_name
	assert contact_number
	assert submit

	license_plate.input("ABC12345").run()
	vehicle_type.select("Car").run()
	owner_name.input("John Doe").run()
	contact_number.input("1234567890").run()
	submit.click().run()
	time.sleep(1)
	assert app.success[0].value == "Vehicle created successfully"


def test_create_vehicle_duplicate():
	
	app = AppTest.from_file("pages/Vehicles.py")
	app.session_state['token'] = TOKEN
	app.session_state['role'] = True
	app.run()

	license_plate = find_input_by_label(app, "License Plate")
	vehicle_type = find_selectbox_by_label(app, "Vehicle Type")
	owner_name = find_input_by_label(app, "Owner Name")
	contact_number = find_input_by_label(app, "Contact Number")
	submit = find_button_by_label(app, "Add Vehicle")

	assert license_plate
	assert vehicle_type
	assert owner_name
	assert contact_number
	assert submit

	license_plate.input("ABC12345").run()
	vehicle_type.select("Car").run()
	owner_name.input("John Doe").run()
	contact_number.input("1234567890").run()
	submit.click().run()
	time.sleep(1)
	assert app.error[0].value == "Error: Vehicle already exists"

def test_update_vehicle():
	
	app = AppTest.from_file("pages/Vehicles.py")
	app.session_state['token'] = TOKEN
	app.session_state['role'] = True
	app.run()
	id_input = find_input_by_label(app, "Enter Vehicle ID to Update/Delete")
	assert id_input
	id_input.input("1").run()
	license_plate = find_input_by_label(app, "License Plate")
	vehicle_type = find_selectbox_by_label(app, "Vehicle Type")
	owner_name = find_input_by_label(app, "Owner Name")
	contact_number = find_input_by_label(app, "Contact Number")
	submit = find_button_by_label(app, "Edit")

	assert license_plate
	assert vehicle_type
	assert owner_name
	assert contact_number
	assert submit

	license_plate.input("ABC12345").run()
	vehicle_type.select("Car").run()
	owner_name.input("John Doe").run()
	contact_number.input("1234567890").run()


# def test_create_parking():
# 	app = AppTest.from_file("pages/ParkingSession.py")
# 	app.session_state['token'] = TOKEN
# 	app.session_state['role'] = True
# 	app.run()
# 	sub = app.subheader[0]
# 	assert sub.value == "Book Parking Session"
# 	entry_date = app.date_input[0]
# 	exit_date = app.date_input[1]
# 	entry_time = app.time_input[0]
# 	exit_time = app.time_input[1]
# 	vehicle = app.selectbox[0]
# 	submit = app.button[0]

# 	assert entry_date.label == "Entry Date"
# 	assert exit_date.label == "Exit Date"
# 	assert entry_time
# 	assert exit_time
# 	assert vehicle
# 	assert submit

# 	if entry_date and exit_date and entry_time and exit_time and vehicle and submit:
# 		entry_date.set_value(datetime.date.today())
# 		exit_date.set_value(datetime.date.today()).run()
# 		entry_time.set_value(datetime.datetime.now().time()).run()
# 		exit_time.set_value(datetime.datetime.now().time() + datetime.timedelta(minutes=15)).run()
# 		vehicle.set_value("ABC12345").run()
# 		submit.click().run()
		
# 		# assert app.success[0].value == "Parking session created successfully"
# 	else:
# 		pytest.fail("Some of the elements are None")

def test_delete_vehicle():
	app = AppTest.from_file("pages/Vehicles.py")
	app.session_state['token'] = TOKEN
	app.session_state['role'] = True
	app.run()
	id_input = find_input_by_label(app, "Enter Vehicle ID to Update/Delete")
	assert id_input
	id_input.input("1").run()
	delete_button = find_button_by_label(app, "Delete Vehicle")

	assert delete_button

	delete_button.click().run()
