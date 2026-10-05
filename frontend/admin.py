import streamlit as st
import requests
import datetime
# This is the address of your running FastAPI server
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Barber Admin Panel", layout="centered")
st.title("💈 Shop Control Panel")

# --- SECTION 1: ADD A NEW SERVICE ---
st.header("Add a New Service")
with st.form("add_service_form", clear_on_submit=True):
    name = st.text_input("Service Name (e.g., Beard Trim)")
    description = st.text_input("Description")
    price = st.number_input("Base Price ($)", min_value=0.0, format="%.2f")
    submit_button = st.form_submit_button("Save to Database")

    if submit_button:
        # Send the data to your FastAPI backend
        payload = {
            "name": name,
            "description": description,
            "base_price": price,
            "is_active": True
        }
        response = requests.post(f"{API_URL}/services/", json=payload)
        
        if response.status_code == 200:
            st.success(f"'{name}' added successfully!")
        else:
            st.error("Failed to add service. Check your backend terminal for errors.")

st.divider()

# --- SECTION 2: MANAGE CURRENT MENU ---
st.header("Manage Current Menu")

try:
    response = requests.get(f"{API_URL}/services/")
    if response.status_code == 200:
        services = response.json()
        
        if services:
            for svc in services:
                # Create an expandable section for each service
                with st.expander(f"💈 {svc['name']} - ${svc['base_price']:.2f}"):
                    with st.form(f"edit_form_{svc['id']}"):
                        new_name = st.text_input("Name", value=svc['name'])
                        new_desc = st.text_input("Description", value=svc['description'])
                        new_price = st.number_input("Price ($)", value=svc['base_price'], format="%.2f")
                        # Checkbox to hide the item from the public menu without deleting it
                        is_active = st.checkbox("Show on Public Menu", value=svc['is_active'])
                        
                        update_button = st.form_submit_button("Update Service")
                        
                        if update_button:
                            update_payload = {
                                "name": new_name,
                                "description": new_desc,
                                "base_price": new_price,
                                "is_active": is_active
                            }
                            # Send the PUT request to update the database
                            update_res = requests.put(f"{API_URL}/services/{svc['id']}", json=update_payload)
                            if update_res.status_code == 200:
                                st.success("Updated! Refreshing...")
                                st.rerun() # Instantly refreshes the Streamlit app
                            else:
                                st.error("Failed to update.")
        else:
            st.info("No services found. Add one above!")
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to backend. Is Uvicorn running?")



st.divider()

# --- SECTION 3: LAUNCH A PROMOTION ---
st.header("📢 Launch a Promotion")
with st.form("add_promo_form", clear_on_submit=True):
    promo_title = st.text_input("Promotion Title (e.g., Back to School Special)")
    discount = st.number_input("Discount Percentage (%)", min_value=1.0, max_value=100.0, step=1.0)
    
    col1, col2 = st.columns(2)
    today = datetime.date.today()
    start_d = col1.date_input("Start Date", today)
    end_d = col2.date_input("End Date", today + datetime.timedelta(days=7))
    
    submit_promo = st.form_submit_button("Launch Promotion")
    
    if submit_promo:
        # Convert simple dates to exact timestamps for the database
        start_dt = datetime.datetime.combine(start_d, datetime.datetime.min.time()).isoformat()
        end_dt = datetime.datetime.combine(end_d, datetime.datetime.max.time()).isoformat()
        
        promo_payload = {
            "title": promo_title,
            "discount_percentage": discount,
            "start_date": start_dt,
            "end_date": end_dt,
            "service_id": None # Applies to everything for now
        }
        promo_res = requests.post(f"{API_URL}/promotions/", json=promo_payload)
        if promo_res.status_code == 200:
            st.success(f"'{promo_title}' is now live!")
        else:
            st.error("Failed to launch promotion.")